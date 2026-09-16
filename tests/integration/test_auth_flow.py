"""M10 集成测试（**真实 PG**；REQ-M10-F01..F05 的 11 项安全验收 S1–S15）。

覆盖：自举（幂等 + 救援 + fail-closed）、agent 请求签名（S2 query/body 篡改、S3 时间窗与
重放、S7 失败不写 nonce、S4 豁免清单、S11 与真实 ``ssh-keygen -Y sign`` 的端到端互操作）、
会话登录（S13 token 哈希、S8 禁用即失效、S15 清理、S6 Cookie 标志）、RBAC（S5 角色上限 +
grant 收窄、**授予与判定两处均拒**）、用户/密钥管理（S9 自身与最后管理员）、审计
（S1 ``entity='auth'``、S10 ``actor='anonymous'`` + ``claimed_*``）。

HTTP 面用真实 FastAPI 应用（``include_router`` + ``require_auth`` 依赖），经
``httpx.ASGITransport`` 直连，不启进程。
"""

from __future__ import annotations

import base64
import hashlib
import shutil
import subprocess
from collections.abc import AsyncIterator
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from fastapi import Depends, FastAPI, Request
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from agenticdocer.auth import bootstrap, middleware, rbac, sessions, signing, sshsig
from agenticdocer.auth import users as auth_users
from agenticdocer.auth.errors import AuthenticationError, BootstrapError
from agenticdocer.auth.router import router as auth_router
from agenticdocer.model import DocTarget, DocTypeTarget, WriteContext, new_uuid7
from agenticdocer.store import (
    ConflictError,
    Database,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)

pytestmark = pytest.mark.integration

SSH_KEYGEN = shutil.which("ssh-keygen")
needs_ssh_keygen = pytest.mark.skipif(SSH_KEYGEN is None, reason="需要本机 ssh-keygen")

SYSTEM_ACTOR = "system"


# ------------------------------------------------------------------------ 夹具


@pytest.fixture(scope="module")
def key_material(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """密码学库生成的两把私钥（不需要外部命令；CLI 互操作用例另用 ssh-keygen 现生成）。"""
    directory = tmp_path_factory.mktemp("authkeys")
    paths: dict[str, Path] = {}
    for name, key in (
        ("admin_ed25519", ed25519.Ed25519PrivateKey.generate()),
        ("editor_ed25519", ed25519.Ed25519PrivateKey.generate()),
        ("outsider_ed25519", ed25519.Ed25519PrivateKey.generate()),
        ("rsa_3072", rsa.generate_private_key(public_exponent=65537, key_size=3072)),
    ):
        target = directory / name
        target.write_bytes(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.OpenSSH,
                serialization.NoEncryption(),
            )
        )
        target.with_suffix(".pub").write_text(signing.public_key_line(key) + "\n")
        paths[name] = target
    return paths


@pytest.fixture
def admin_pub_path(key_material: dict[str, Path], tmp_path: Path, monkeypatch) -> Path:
    """``ADMIN_SSH_PUBKEY_FILE`` 指向 admin 公钥（自举入口）。"""
    target = tmp_path / "admin.pub"
    target.write_text(key_material["admin_ed25519"].with_suffix(".pub").read_text())
    monkeypatch.setenv("ADMIN_SSH_PUBKEY_FILE", str(target))
    monkeypatch.setenv("AUTH_RATE_LIMIT_PER_MIN", "1000")
    return target


@pytest.fixture(autouse=True)
def _reset_auth_windows() -> None:
    sessions.reset_rate_limits()
    auth_users.reset_failure_aggregates()


@pytest.fixture(autouse=True)
async def _clean_auth_tables(database: Database) -> AsyncIterator[None]:
    """每个用例从空鉴权状态开始（``users`` 级联清 keys/grants/sessions）。

    ``grants.granted_by`` 无级联动作，故先置空再删用户（与 ``users.delete_user`` 同口径）。
    """
    async def _wipe() -> None:
        async with database.transaction() as session:
            await session.execute(text("UPDATE grants SET granted_by = NULL"))
            await session.execute(text("DELETE FROM users"))
            await session.execute(text("DELETE FROM nonces"))

    await _wipe()
    yield
    await _wipe()


@pytest.fixture
def app(database: Database) -> FastAPI:
    """最小 FastAPI 应用：M10 依赖项 + 一个受保护端点（M06/M07 的装配形态）。"""
    application = FastAPI()
    application.state.auth_db = database
    application.include_router(auth_router)

    @application.get("/healthz")
    async def healthz() -> dict[str, str]:  # S4 豁免
        return {"status": "ok"}

    @application.get("/")
    async def index() -> dict[str, bool]:  # 登录页（S4 豁免）
        return {"login": True}

    @application.get("/api/v1/docs")
    async def list_docs(ctx: middleware.AuthContext = Depends(middleware.require_auth)) -> dict:
        return {"actor": ctx.actor, "source": ctx.source, "username": ctx.user.username}

    @application.get("/api/v1/docs/{doc_id}")
    async def get_doc(
        doc_id: str, ctx: middleware.AuthContext = Depends(middleware.require_auth)
    ) -> dict:
        return {"docId": doc_id, "actor": ctx.actor}

    @application.post("/api/v1/docs")
    async def create_doc(
        payload: dict, ctx: middleware.AuthContext = Depends(middleware.require_permission("write"))
    ) -> dict:
        return {"actor": ctx.actor, "received": payload}

    return application


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as http_client:
        yield http_client


async def _scalar(database: Database, sql: str, **params: object) -> object:
    async with database.session() as session:
        return (await session.execute(text(sql), params)).scalar_one()


async def _rows(database: Database, sql: str, **params: object) -> list[tuple]:
    async with database.session() as session:
        return list((await session.execute(text(sql), params)).all())


# -------------------------------------------------------------------- 自举（F05）


async def test_bootstrap_creates_admin_and_is_idempotent(
    database: Database, admin_pub_path: Path, key_material: dict[str, Path]
) -> None:
    admin = await bootstrap.bootstrap_admin(db=database)
    assert admin.role == "admin" and admin.status == "active"
    assert admin.username == "admin"

    keys = await auth_users.list_ssh_keys(admin.user_id, db=database)
    assert len(keys) == 1
    assert keys[0].key_type == "ssh-ed25519"
    assert keys[0].fingerprint == signing.fingerprint(
        key_material["admin_ed25519"].with_suffix(".pub").read_text()
    )

    # 幂等：第二次仍是同一 admin，不重复建号/建键
    again = await bootstrap.bootstrap_admin(db=database)
    assert again.user_id == admin.user_id
    assert len(await auth_users.list_ssh_keys(admin.user_id, db=database)) == 1
    assert len(await auth_users.list_users(db=database)) == 1

    # 「以 DB 为准」：键文件换成别的公钥也不改写现有 admin
    admin_pub_path.write_text(key_material["outsider_ed25519"].with_suffix(".pub").read_text())
    unchanged = await bootstrap.bootstrap_admin(db=database)
    assert unchanged.user_id == admin.user_id
    assert len(await auth_users.list_ssh_keys(admin.user_id, db=database)) == 1


async def test_bootstrap_rescues_when_no_active_admin(
    database: Database, admin_pub_path: Path
) -> None:
    admin = await bootstrap.bootstrap_admin(db=database)
    async with database.transaction() as session:  # 模拟「无 active admin」（S9 救援场景）
        await session.execute(
            text("UPDATE users SET status = 'disabled' WHERE user_id = :uid"), {"uid": admin.user_id}
        )
    assert await bootstrap.has_active_admin(db=database) is False

    rescued = await bootstrap.bootstrap_admin(db=database)
    assert rescued.user_id == admin.user_id
    assert rescued.status == "active" and rescued.role == "admin"
    assert await bootstrap.has_active_admin(db=database) is True


async def test_bootstrap_fails_closed_without_key_file(
    database: Database, tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("ADMIN_SSH_PUBKEY_FILE", str(tmp_path / "absent.pub"))
    with pytest.raises(BootstrapError) as excinfo:
        await bootstrap.bootstrap_admin(db=database)
    assert "auth bootstrap" in str(excinfo.value)

    empty = tmp_path / "empty.pub"
    empty.write_text("   \n")
    with pytest.raises(BootstrapError):
        await bootstrap.bootstrap_admin(empty, db=database)


async def test_no_users_means_all_requests_401_with_bootstrap_hint(
    client: AsyncClient, database: Database
) -> None:
    for path in ("/api/v1/docs", "/api/v1/auth/me"):
        response = await client.get(path)
        assert response.status_code == 401, path
        assert "auth bootstrap" in response.json()["detail"]["message"]
    # 无 active admin 时的 401 也落审计（S1/S10）
    events = await _rows(
        database,
        "SELECT actor, payload FROM events WHERE entity = 'auth' AND op = 'fail'",
    )
    assert events and all(actor == "anonymous" for actor, _ in events)


# ------------------------------------------------------- agent 签名路径（F01）


async def _make_user(database: Database, username: str, role: str, key_path: Path):
    user = await auth_users.create_user(username, role, actor=SYSTEM_ACTOR, db=database)
    key = await auth_users.add_ssh_key(
        user.user_id, key_path.with_suffix(".pub").read_text(), actor=SYSTEM_ACTOR, db=database
    )
    return user, key


async def test_signed_request_authenticates_and_attributes_actor(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    user, _ = await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])

    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs")
    response = await client.get("/api/v1/docs", headers=headers)
    assert response.status_code == 200, response.text
    assert response.json() == {"actor": str(user.user_id), "source": "agent", "username": "alice"}


async def test_query_tampering_is_rejected(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """**S2**：query 原样参与签名，改任一参数即 401。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])
    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs?expected_version=3")

    ok = await client.get("/api/v1/docs?expected_version=3", headers=headers)
    assert ok.status_code == 200
    # nonce 已消费，换一个 nonce 重签后再篡改 query
    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs?expected_version=3")
    tampered = await client.get("/api/v1/docs?expected_version=4", headers=headers)
    assert tampered.status_code == 401
    assert tampered.json()["detail"]["reason"] == "bad_signature"


async def test_body_and_path_tampering_is_rejected(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])

    body = b'{"title":"A"}'
    # Content-Type 不参与签名载荷（S2 只绑 METHOD/RAW_PATH/body 摘要/TS/nonce）
    json_headers = {"Content-Type": "application/json"}
    headers = signing.sign_request_headers(key, "POST", "/api/v1/docs", body)
    assert (
        await client.post("/api/v1/docs", content=body, headers={**headers, **json_headers})
    ).status_code == 200

    headers = signing.sign_request_headers(key, "POST", "/api/v1/docs", b'{"title":"B"}')
    assert (
        await client.post("/api/v1/docs", content=b'{"title":"A"}', headers={**headers, **json_headers})
    ).status_code == 401

    tampered_path = signing.sign_request_headers(key, "GET", "/api/v1/docs/SPEC-A")
    response = await client.get("/api/v1/docs/SPEC-B", headers=tampered_path)
    assert response.status_code == 401


async def test_time_window_bounds(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """**S3**：偏移 ∈ [−30s, +300s]。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])
    now = datetime.now(timezone.utc)

    def stamp(offset_seconds: int) -> str:
        return signing.timestamp_now(now + timedelta(seconds=offset_seconds))

    stale = signing.sign_request_headers(
        key, "GET", "/api/v1/docs", timestamp=stamp(-301)
    )
    response = await client.get("/api/v1/docs", headers=stale)
    assert response.status_code == 401
    assert response.json()["detail"]["reason"] == "timestamp_expired"

    future = signing.sign_request_headers(
        key, "GET", "/api/v1/docs", timestamp=stamp(31)
    )
    response = await client.get("/api/v1/docs", headers=future)
    assert response.status_code == 401
    assert response.json()["detail"]["reason"] == "timestamp_future"

    inside = signing.sign_request_headers(
        key, "GET", "/api/v1/docs", timestamp=stamp(-299)
    )
    assert (await client.get("/api/v1/docs", headers=inside)).status_code == 200

    malformed = dict(inside)
    malformed["X-Timestamp"] = "not-a-timestamp"
    response = await client.get("/api/v1/docs", headers=malformed)
    assert response.status_code == 401
    assert response.json()["detail"]["reason"] == "bad_timestamp"


async def test_nonce_replay_is_rejected(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])
    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs")

    assert (await client.get("/api/v1/docs", headers=headers)).status_code == 200
    replay = await client.get("/api/v1/docs", headers=headers)
    assert replay.status_code == 401
    assert replay.json()["detail"]["reason"] == "nonce_replay"


async def test_failed_verification_writes_no_nonce(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """**S7**：验签未通过 → ``nonces`` 表零写入（未认证请求不写库）。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])
    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs")
    headers["X-SSH-Signature"] = base64.b64encode(b"\x00" * 64).decode()

    before = await _scalar(database, "SELECT count(*) FROM nonces")
    response = await client.get("/api/v1/docs", headers=headers)
    assert response.status_code == 401
    after = await _scalar(database, "SELECT count(*) FROM nonces")
    assert before == after == 0
    assert (
        await _scalar(database, "SELECT count(*) FROM nonces WHERE nonce = :n", n=headers["X-Nonce"])
        == 0
    )


async def test_unregistered_key_is_forbidden_and_audited(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """未注册公钥 → 403；审计事件记 ``claimed_key_id`` 且不写身份列（S10）。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    outsider = signing.load_private_key(key_material["outsider_ed25519"])
    headers = signing.sign_request_headers(outsider, "GET", "/api/v1/docs")

    response = await client.get("/api/v1/docs", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"]["error"] == "DTO_AUTH_REJECTED"

    events = await _rows(
        database,
        "SELECT actor, payload FROM events WHERE entity = 'auth' AND op = 'fail' "
        "ORDER BY ts DESC LIMIT 1",
    )
    actor, payload = events[0]
    assert actor == "anonymous"
    assert payload["claimed_key_id"] == headers["X-SSH-Key-Id"]
    assert "user_id" not in payload and "key_fingerprint" not in payload


async def test_role_insufficient_is_403(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """签名有效但角色不足 → 403（REQ-M10-F01f）。"""
    await _make_user(database, "bob", "reader", key_material["outsider_ed25519"])
    key = signing.load_private_key(key_material["outsider_ed25519"])
    headers = signing.sign_request_headers(key, "POST", "/api/v1/docs", b"{}")
    response = await client.post("/api/v1/docs", content=b"{}", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"]["reason"] == "forbidden"


async def test_missing_credentials_is_401_and_exemptions_work(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """**S4**：豁免清单外无凭据必 401；清单内端点无需凭据。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])

    missing = await client.get("/api/v1/docs")
    assert missing.status_code == 401
    assert missing.json()["detail"]["reason"] == "missing_credentials"
    assert missing.headers["WWW-Authenticate"].startswith("SSHSIG")

    assert (await client.get("/healthz")).status_code == 200
    assert (await client.get("/")).status_code == 200
    assert (await client.post("/api/v1/auth/challenge")).status_code == 200

    assert middleware.is_exempt("/healthz") is True
    assert middleware.is_exempt("/api/v1/auth/login") is True
    assert middleware.is_exempt("/assets/login-app.js") is True
    assert middleware.is_exempt("/api/v1/docs") is False
    assert middleware.is_exempt("/docs") is False
    assert middleware.is_exempt("/openapi.json") is False
    assert middleware.is_exempt("/", "POST") is False


@needs_ssh_keygen
async def test_end_to_end_with_real_ssh_keygen_signature(
    client: AsyncClient, database: Database, tmp_path: Path
) -> None:
    """**S11 端到端互操作**：用真实 ``ssh-keygen -Y sign`` 签 HTTP 载荷 → 200。

    模拟 M11 CLI：从私钥生成签名头（签名由 openssh 产出，服务端验签器接受）。
    """
    private = tmp_path / "cli_ed25519"
    subprocess.run(
        [SSH_KEYGEN, "-q", "-N", "", "-t", "ed25519", "-f", str(private)],
        check=True,
        capture_output=True,
    )
    await _make_user(database, "cli", "editor", private)

    timestamp = signing.timestamp_now()
    nonce = signing.new_nonce()
    path = "/api/v1/docs?limit=1"
    payload = signing.request_payload("GET", path, None, timestamp, nonce)
    (tmp_path / "payload").write_bytes(payload)
    subprocess.run(
        [
            SSH_KEYGEN, "-Y", "sign", "-n", sshsig.NAMESPACE,
            "-f", str(private), str(tmp_path / "payload"),
        ],
        check=True,
        capture_output=True,
    )
    signature = Path(f"{tmp_path / 'payload'}.sig").read_text()
    headers = {
        "X-SSH-Key-Id": signing.fingerprint(private.with_suffix(".pub").read_text()),
        "X-SSH-Signature": signature,
        "X-Timestamp": timestamp,
        "X-Nonce": nonce,
    }
    response = await client.get(path, headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["source"] == "agent"


# ------------------------------------------------------ 会话登录路径（F02）


async def _login_with_ssh_key(
    client: AsyncClient, database: Database, key_path: Path
) -> tuple[dict, str]:
    """挑战-响应登录（客户端用私钥签 nonce）→ ``(响应体, token)``。"""
    challenge = (await client.post("/api/v1/auth/challenge")).json()
    key = signing.load_private_key(key_path)
    signature = signing.sign_message(key, signing.login_payload(challenge["nonce"]))
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "keyFingerprint": signing.fingerprint(key_path.with_suffix(".pub").read_text()),
            "nonce": challenge["nonce"],
            "signature": signature,
        },
    )
    assert response.status_code == 200, response.text
    token = response.cookies.get(sessions.SESSION_COOKIE_NAME)
    assert token is not None
    return response.json(), token


async def test_challenge_login_session_and_token_hashing(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """REQ-M10-F02 a/e/f + **S13**：token 只存 SHA256、熵 32 字节、Cookie 标志正确。"""
    user, _ = await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    body, token = await _login_with_ssh_key(client, database, key_material["editor_ed25519"])

    assert body["userId"] == str(user.user_id)
    assert body["username"] == "alice" and body["role"] == "editor"
    assert len(token) >= 43  # token_urlsafe(32) ≈ 43 字符
    rows = await _rows(database, "SELECT token_hash FROM sessions")
    assert rows == [(hashlib.sha256(token.encode()).hexdigest(),)]
    assert await _scalar(database, "SELECT count(*) FROM sessions WHERE token_hash = :t", t=token) == 0

    # 再登录一次，专门检查 Set-Cookie 标志（S6）
    challenge = (await client.post("/api/v1/auth/challenge")).json()
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "keyFingerprint": signing.fingerprint(
                key_material["editor_ed25519"].with_suffix(".pub").read_text()
            ),
            "nonce": challenge["nonce"],
            "signature": signing.sign_message(
                signing.load_private_key(key_material["editor_ed25519"]),
                signing.login_payload(challenge["nonce"]),
            ),
        },
    )
    set_cookie = response.headers["set-cookie"]
    assert "httponly" in set_cookie.lower() and "samesite=lax" in set_cookie.lower()

    me = await client.get("/api/v1/auth/me", cookies={sessions.SESSION_COOKIE_NAME: token})
    assert me.status_code == 200
    assert me.json()["userId"] == str(user.user_id)
    assert me.json()["permissions"] == []


async def test_login_nonce_replay_and_expiry(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    challenge = (await client.post("/api/v1/auth/challenge")).json()
    key = signing.load_private_key(key_material["editor_ed25519"])
    payload = {
        "keyFingerprint": signing.fingerprint(
            key_material["editor_ed25519"].with_suffix(".pub").read_text()
        ),
        "nonce": challenge["nonce"],
        "signature": signing.sign_message(key, signing.login_payload(challenge["nonce"])),
    }
    assert (await client.post("/api/v1/auth/login", json=payload)).status_code == 200

    replay = await client.post("/api/v1/auth/login", json=payload)
    assert replay.status_code == 401
    assert replay.json()["detail"]["reason"] == "unknown_challenge"

    expired = (await client.post("/api/v1/auth/challenge")).json()
    async with database.transaction() as session:
        await session.execute(
            text("UPDATE nonces SET seen_at = :ts WHERE nonce = :n"),
            {"ts": datetime.now(timezone.utc) - timedelta(seconds=121), "n": expired["nonce"]},
        )
    stale = await client.post(
        "/api/v1/auth/login",
        json={
            **payload,
            "nonce": expired["nonce"],
            "signature": signing.sign_message(key, signing.login_payload(expired["nonce"])),
        },
    )
    assert stale.status_code == 401
    assert stale.json()["detail"]["reason"] == "challenge_expired"

    # 坏签名：401 且不消费挑战（S7：验签失败不写库）
    pending = (await client.post("/api/v1/auth/challenge")).json()
    before = await _scalar(database, "SELECT count(*) FROM nonces")
    bad = await client.post(
        "/api/v1/auth/login",
        json={**payload, "nonce": pending["nonce"], "signature": "AAAA"},
    )
    assert bad.status_code == 401
    assert await _scalar(database, "SELECT count(*) FROM nonces") == before
    assert (
        await _scalar(database, "SELECT count(*) FROM nonces WHERE nonce = :n", n=pending["nonce"])
        == 1
    )


async def test_logout_invalidates_cookie(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    _, token = await _login_with_ssh_key(client, database, key_material["editor_ed25519"])
    cookies = {sessions.SESSION_COOKIE_NAME: token}

    assert (await client.get("/api/v1/auth/me", cookies=cookies)).status_code == 200
    logged_out = await client.post("/api/v1/auth/logout", cookies=cookies)
    assert logged_out.status_code == 204
    assert (await client.get("/api/v1/auth/me", cookies=cookies)).status_code == 401
    assert await _scalar(database, "SELECT count(*) FROM sessions") == 0

    # 无凭据的 logout 也在豁免清单外 → 401（S4）
    assert (await client.post("/api/v1/auth/logout")).status_code == 401


async def test_disabling_user_kills_keys_and_live_sessions(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    user, _ = await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    _, token = await _login_with_ssh_key(client, database, key_material["editor_ed25519"])
    cookies = {sessions.SESSION_COOKIE_NAME: token}
    key = signing.load_private_key(key_material["editor_ed25519"])
    # Cookie 优先于签名头（浏览器路径）；清空 cookie jar 以专测 **agent 签名路径**
    client.cookies.clear()
    assert (
        await client.get(
            "/api/v1/docs", headers=signing.sign_request_headers(key, "GET", "/api/v1/docs")
        )
    ).status_code == 200

    # 由另一 admin 禁用（S9：不能禁用最后一个 active admin，故先建第二个 admin）
    other_admin = await auth_users.create_user("root2", "admin", actor=SYSTEM_ACTOR, db=database)
    await auth_users.update_user(
        user.user_id,
        status="disabled",
        actor=str(other_admin.user_id),
        actor_id=other_admin.user_id,
        db=database,
    )
    assert await auth_users.find_active_key(
        signing.fingerprint(key_material["editor_ed25519"].with_suffix(".pub").read_text()),
        db=database,
    ) is None
    assert (await client.get("/api/v1/auth/me", cookies=cookies)).status_code == 401
    signed = await client.get(
        "/api/v1/docs", headers=signing.sign_request_headers(key, "GET", "/api/v1/docs")
    )
    assert signed.status_code == 403
    # 该用户的会话被立即清除（S8 + S15 清理口径）
    assert await _scalar(database, "SELECT count(*) FROM sessions WHERE user_id = :u", u=user.user_id) == 0


async def test_rate_limit_on_challenge(
    client: AsyncClient, monkeypatch, database: Database, key_material: dict[str, Path]
) -> None:
    """**S7**：``/auth/challenge`` 按 IP 限流（``AUTH_RATE_LIMIT_PER_MIN``）。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    monkeypatch.setenv("AUTH_RATE_LIMIT_PER_MIN", "2")
    sessions.reset_rate_limits()

    assert (await client.post("/api/v1/auth/challenge")).status_code == 200
    assert (await client.post("/api/v1/auth/challenge")).status_code == 200
    limited = await client.post("/api/v1/auth/challenge")
    assert limited.status_code == 429
    assert limited.json()["detail"]["reason"] == "rate_limited"


async def test_purge_expired_removes_sessions_and_nonces(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """**S15**：过期会话与非ce 同一任务清理（清理后该会话立即 401）。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    _, token = await _login_with_ssh_key(client, database, key_material["editor_ed25519"])
    stale_seconds = sessions.nonce_ttl_seconds() + 5
    async with database.transaction() as session:
        await session.execute(
            text("UPDATE sessions SET expires_at = :ts"),
            {"ts": datetime.now(timezone.utc) - timedelta(seconds=1)},
        )
        await session.execute(
            text("INSERT INTO nonces (nonce, user_id, seen_at) VALUES ('stale-nonce', NULL, :ts)"),
            {"ts": datetime.now(timezone.utc) - timedelta(seconds=stale_seconds)},
        )

    report = await sessions.purge_expired(db=database)
    assert report.sessions == 1 and report.nonces >= 1
    assert await _scalar(database, "SELECT count(*) FROM sessions") == 0
    assert await _scalar(database, "SELECT count(*) FROM nonces WHERE nonce = 'stale-nonce'") == 0
    assert (
        await client.get("/api/v1/auth/me", cookies={sessions.SESSION_COOKIE_NAME: token})
    ).status_code == 401


def test_cookie_secure_follows_deployment(monkeypatch) -> None:
    """**S6**：非 loopback 部署（TLS 代理终止）→ Cookie 带 ``Secure``。"""
    monkeypatch.delenv("AUTH_COOKIE_SECURE", raising=False)
    monkeypatch.setenv("API_HOST", "127.0.0.1")
    assert middleware.cookie_secure() is False
    assert middleware.session_cookie_kwargs()["secure"] is False

    monkeypatch.setenv("API_HOST", "0.0.0.0")
    assert middleware.cookie_secure() is True
    assert middleware.session_cookie_kwargs()["httponly"] is True
    assert middleware.session_cookie_kwargs()["samesite"] == "lax"

    monkeypatch.setenv("AUTH_COOKIE_SECURE", "0")
    assert middleware.cookie_secure() is False
    monkeypatch.setenv("AUTH_COOKIE_SECURE", "1")
    monkeypatch.setenv("API_HOST", "127.0.0.1")
    assert middleware.cookie_secure() is True


# ------------------------------------------------- 用户 / 密钥 / 授权（F03/F04）


async def test_username_unique_conflict(database: Database) -> None:
    await auth_users.create_user("dup", "editor", actor=SYSTEM_ACTOR, db=database)
    with pytest.raises(ConflictError) as excinfo:
        await auth_users.create_user("dup", "reader", actor=SYSTEM_ACTOR, db=database)
    assert excinfo.value.status_code == 409
    with pytest.raises(ValidationError):
        await auth_users.create_user("bad", "root", actor=SYSTEM_ACTOR, db=database)


async def test_key_registration_rules(
    database: Database, key_material: dict[str, Path]
) -> None:
    alice = await auth_users.create_user("alice", "editor", actor=SYSTEM_ACTOR, db=database)
    bob = await auth_users.create_user("bob", "editor", actor=SYSTEM_ACTOR, db=database)
    admin_line = key_material["admin_ed25519"].with_suffix(".pub").read_text()
    rsa_line = key_material["rsa_3072"].with_suffix(".pub").read_text()

    first = await auth_users.add_ssh_key(alice.user_id, admin_line, actor=SYSTEM_ACTOR, db=database)
    second = await auth_users.add_ssh_key(alice.user_id, rsa_line, actor=SYSTEM_ACTOR, db=database)
    assert {first.key_type, second.key_type} == {"ssh-ed25519", "rsa-sha2-512"}

    with pytest.raises(ConflictError):  # 同一用户重复登记
        await auth_users.add_ssh_key(alice.user_id, admin_line, actor=SYSTEM_ACTOR, db=database)
    with pytest.raises(ConflictError):  # 同一公钥属于他人（身份归属唯一）
        await auth_users.add_ssh_key(bob.user_id, admin_line, actor=SYSTEM_ACTOR, db=database)
    with pytest.raises(ValidationError):  # 公钥不合规 → 422
        await auth_users.add_ssh_key(bob.user_id, "ssh-ed25519 not-base64!!", actor=SYSTEM_ACTOR, db=database)
    with pytest.raises(NotFoundError):
        await auth_users.add_ssh_key(new_uuid7(), admin_line, actor=SYSTEM_ACTOR, db=database)

    # 吊销单个密钥不影响同用户其他密钥（F03c）
    await auth_users.revoke_ssh_key(alice.user_id, first.key_id, actor=SYSTEM_ACTOR, db=database)
    active = await auth_users.list_ssh_keys(alice.user_id, db=database)
    assert [key.key_id for key in active] == [second.key_id]
    revoked = await auth_users.list_ssh_keys(alice.user_id, include_revoked=True, db=database)
    assert len(revoked) == 2
    # 吊销后重新登记复用该行
    readded = await auth_users.add_ssh_key(alice.user_id, admin_line, actor=SYSTEM_ACTOR, db=database)
    assert readded.revoked_at is None
    assert len(await auth_users.list_ssh_keys(alice.user_id, db=database)) == 2


async def test_last_admin_and_self_protection(
    database: Database, admin_pub_path: Path
) -> None:
    """**S9**：不可 disable/demote/delete 自身，也不可操作最后一个 active admin（409）。"""
    admin = await bootstrap.bootstrap_admin(db=database)
    with pytest.raises(ConflictError) as excinfo:
        await auth_users.update_user(
            admin.user_id, role="editor", actor=str(admin.user_id), actor_id=admin.user_id, db=database
        )
    assert excinfo.value.status_code == 409
    with pytest.raises(ConflictError):
        await auth_users.update_user(
            admin.user_id,
            status="disabled",
            actor=str(admin.user_id),
            actor_id=admin.user_id,
            db=database,
        )
    with pytest.raises(ConflictError):  # 最后一个 active admin（由他人操作也不行）
        await auth_users.update_user(
            admin.user_id, role="editor", actor=str(new_uuid7()), actor_id=new_uuid7(), db=database
        )
    with pytest.raises(ConflictError):
        await auth_users.delete_user(
            admin.user_id, actor=str(new_uuid7()), actor_id=new_uuid7(), db=database
        )

    second = await auth_users.create_user("root2", "admin", actor=SYSTEM_ACTOR, db=database)
    demoted = await auth_users.update_user(
        admin.user_id,
        role="editor",
        actor=str(second.user_id),
        actor_id=second.user_id,
        db=database,
    )
    assert demoted.role == "editor"  # 有继任者后允许降级
    assert (await auth_users.get_user(admin.user_id, db=database)).role == "editor"
    # 自身删除仍被拒（即使不是最后一个 admin）
    with pytest.raises(ConflictError):
        await auth_users.delete_user(
            second.user_id, actor=str(second.user_id), actor_id=second.user_id, db=database
        )


async def test_grant_denied_at_grant_time_and_decision_time(
    database: Database, key_material: dict[str, Path]
) -> None:
    """**S5 两处均拒**（REQ-M10-F04e）：授予时 422 + 判定时 403。"""
    reader = await auth_users.create_user("reader1", "reader", actor=SYSTEM_ACTOR, db=database)

    with pytest.raises(ValidationError) as excinfo:
        await auth_users.create_grant(
            reader.user_id, "doc", "SPEC-A", "write", actor=SYSTEM_ACTOR, db=database
        )
    assert excinfo.value.status_code == 422
    with pytest.raises(ValidationError):
        await auth_users.create_grant(
            reader.user_id, "repo", "org/x", "read", actor=SYSTEM_ACTOR, db=database
        )
    with pytest.raises(ValidationError):
        await auth_users.create_grant(
            reader.user_id, "doc", "SPEC-A", "admin", actor=SYSTEM_ACTOR, db=database
        )

    # 绕过服务层直接落库（模拟历史脏数据）→ 判定时仍 403
    async with database.transaction() as session:
        await session.execute(
            text(
                "INSERT INTO grants (grant_id, user_id, scope, value, permission, granted_at) "
                "VALUES (:gid, :uid, 'doc', 'SPEC-A', 'write', now())"
            ),
            {"gid": new_uuid7(), "uid": reader.user_id},
        )
    with pytest.raises(ForbiddenError):
        await auth_users.authorize_user(reader, "write", DocTarget(value="SPEC-A"), db=database)
    # 只读仍可用
    await auth_users.authorize_user(reader, "read", DocTarget(value="SPEC-A"), db=database)


async def test_grant_narrowing_and_revocation(
    database: Database, admin_pub_path: Path
) -> None:
    """REQ-M10-F04 d：收窄范围精确；撤销后恢复角色作用域。"""
    await bootstrap.bootstrap_admin(db=database)
    editor = await auth_users.create_user("ed", "editor", actor=SYSTEM_ACTOR, db=database)
    grant = await auth_users.create_grant(
        editor.user_id, "doc_type", "product", "write", actor=SYSTEM_ACTOR, db=database
    )
    assert grant.scope == "doc_type" and grant.permission == "write"

    await auth_users.authorize_user(
        editor, "write", DocTarget(value="SPEC-P"), doc_type="product", db=database
    )
    with pytest.raises(ForbiddenError):
        await auth_users.authorize_user(
            editor, "write", DocTarget(value="SPEC-S"), doc_type="standard", db=database
        )
    with pytest.raises(ForbiddenError):
        await auth_users.authorize_user(editor, "write", DocTypeTarget(value="standard"), db=database)

    # 重复授予 → 409（唯一约束）
    with pytest.raises(ConflictError):
        await auth_users.create_grant(
            editor.user_id, "doc_type", "product", "write", actor=SYSTEM_ACTOR, db=database
        )

    await auth_users.delete_grant(grant.grant_id, actor=SYSTEM_ACTOR, db=database)
    await auth_users.authorize_user(
        editor, "write", DocTarget(value="SPEC-S"), doc_type="standard", db=database
    )
    with pytest.raises(NotFoundError):
        await auth_users.delete_grant(grant.grant_id, actor=SYSTEM_ACTOR, db=database)


async def test_auth_audit_events_cover_all_mutations(
    database: Database, admin_pub_path: Path, key_material: dict[str, Path]
) -> None:
    """**S1**：``entity='auth'`` 事件可写入且覆盖用户/密钥/授权/登录/失败。"""
    admin = await bootstrap.bootstrap_admin(db=database)
    alice = await auth_users.create_user("alice", "editor", actor=str(admin.user_id), db=database)
    line = key_material["editor_ed25519"].with_suffix(".pub").read_text()
    key = await auth_users.add_ssh_key(alice.user_id, line, actor=str(admin.user_id), db=database)
    await auth_users.revoke_ssh_key(alice.user_id, key.key_id, actor=str(admin.user_id), db=database)
    await auth_users.create_grant(
        alice.user_id, "doc", "SPEC-A", "read", actor=str(admin.user_id), db=database
    )
    await auth_users.update_user(
        alice.user_id, role="reviewer", actor=str(admin.user_id), actor_id=admin.user_id, db=database
    )

    events = await _rows(
        database,
        "SELECT op, actor, payload FROM events WHERE entity = 'auth' ORDER BY ts, event_id",
    )
    ops = [op for op, _, _ in events]
    assert "user_change" in ops and "key_change" in ops and "grant_change" in ops
    assert all(actor for _, actor, _ in events)
    actions = {payload["action"] for _, _, payload in events if "action" in payload}
    assert {"bootstrap_create", "create_user", "add_key", "revoke_key", "add_grant", "update_user"} <= actions
    # 折叠接口可重放 auth 审计（§3.5：仅审计，不参与实体折叠）
    replayed = await auth_users.log_auth_event(
        "fail", "anonymous", {"reason": "manual"}, db=database
    )
    assert replayed.entity == "auth" and replayed.op == "fail"


async def test_session_resolution_slides_expiry(
    database: Database, key_material: dict[str, Path]
) -> None:
    """会话 TTL 8h 滑动续期；未知/过期 token → ``None``（并清行）。"""
    user = await auth_users.create_user("alice", "editor", actor=SYSTEM_ACTOR, db=database)
    session, token = await sessions.create_session(user.user_id, db=database)

    resolved = await sessions.resolve_session(token, db=database)
    assert resolved is not None and resolved.user_id == user.user_id
    expires = await _scalar(
        database, "SELECT expires_at FROM sessions WHERE session_id = :sid", sid=session.session_id
    )
    assert expires > session.expires_at - timedelta(seconds=1)

    assert await sessions.resolve_session("bogus-token", db=database) is None
    async with database.transaction() as db_session:
        await db_session.execute(
            text("UPDATE sessions SET expires_at = :ts"),
            {"ts": datetime.now(timezone.utc) - timedelta(seconds=1)},
        )
    assert await sessions.resolve_session(token, db=database) is None
    assert await _scalar(database, "SELECT count(*) FROM sessions") == 0


async def test_authenticate_rejects_bad_nonce_header(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """``X-Nonce`` 熵不足 / 非法字符 → 401（§3 M06：≥128 位随机）。"""
    await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])
    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs")
    headers["X-Nonce"] = "短"
    response = await client.get("/api/v1/docs", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"]["reason"] == "bad_nonce"


async def test_write_context_uses_verified_identity(
    client: AsyncClient, database: Database, key_material: dict[str, Path]
) -> None:
    """S14：身份取自验签结果；``source`` 由凭据类型判定（签名 → ``agent``，Cookie → ``webui``）。"""
    user, _ = await _make_user(database, "alice", "editor", key_material["editor_ed25519"])
    key = signing.load_private_key(key_material["editor_ed25519"])
    headers = signing.sign_request_headers(key, "GET", "/api/v1/docs")
    # 客户端自述头不再存在：X-Actor 被忽略（S14）
    headers["X-Actor"] = "someone-else"
    response = await client.get("/api/v1/docs", headers=headers)
    assert response.status_code == 200
    assert response.json()["actor"] == str(user.user_id)

    ctx = middleware.AuthContext(user=user, source="webui", session_hash="h")
    assert middleware.write_context(ctx) == WriteContext(actor=str(user.user_id), source="webui")
