"""M11 CLI 端到端集成测试（**真实 PG + 真实 HTTP 进程 + 真实 SSH 签名**；REQ-M11-F01..F04）。

为什么这样测：CLI 的验收要件是「签名 → 调用 M06/M07 API → 成功」——只有真实 uvicorn 进程
（同一鉴权/RBAC 中间件）才能证明 CLI 与 WebUI 共用同一判定口径（P5）；`CliRunner` 也无法覆盖
**进程退出码**（REQ-M11-F01b：权限不足必须非零退出）。

**隔离库**：本用例在 `agenticdocer_m11_test` 上跑（自建自 DROP），不触碰共享 `agenticdocer_test`。
"""

from __future__ import annotations

import asyncio
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from agenticdocer.auth import signing

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
ISOLATED_DB = "agenticdocer_m11_test"
APP_URL_DEFAULT = "postgresql+asyncpg://agenticdocer_app@127.0.0.1:5432/agenticdocer_test"
OWNER_URL_DEFAULT = "postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer_test"
SUPER_URL_DEFAULT = "postgresql+asyncpg://postgres@127.0.0.1:5432/postgres"
OWNER_ROLE = "agenticdocer"
APP_ROLE = "agenticdocer_app"
DOC_ID = "SPEC-M11-E2E"
DOC_SLUG = "M11-E2E"
STARTUP_TIMEOUT = 40.0

SOURCE_MD = f"""---
title: M11 CLI 端到端样例
type: composite
purpose: spec
audience: both
direction: input
status: draft
version: "1.0.0"
section_meta: "@meta"
spec_id: {DOC_ID}
spec_type: standard
spec_org: TEST
spec_revision: "1.0"
source: corpus/01_raw/specifications/test/m11.pdf
converted_by: mineru
converted_at: 2026-09-16
reviewed_by: tester
reviewed_at: 2026-09-16
---

# 1 概述

本章说明 M11 CLI 的端到端验收范围。

## 1.1 时序

传输在时钟上升沿采样。

# 2 术语

- 断言：驱动到被测器件的一段激励。
"""

# ----------------------------------------------------------------------
# 隔离库 + 进程夹具
# ----------------------------------------------------------------------


def _base_app_url() -> str:
    return os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL") or APP_URL_DEFAULT


def _app_url() -> str:
    """应用角色 + 隔离库名（口令沿用 `.env` 里已验证可用的那份）。"""
    return make_url(_base_app_url()).set(database=ISOLATED_DB).render_as_string(hide_password=False)


def _owner_url() -> str:
    """属主凭据 + 隔离库名（只借用户名/口令，不借库名——那是开发库）。"""
    owner = make_url(os.environ.get("MIGRATION_DATABASE_URL") or OWNER_URL_DEFAULT)
    return make_url(_base_app_url()).set(
        database=ISOLATED_DB, username=owner.username, password=owner.password
    ).render_as_string(hide_password=False)


async def _probe(url: str) -> str | None:
    engine = create_async_engine(url, poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return None
    except Exception as exc:  # noqa: BLE001 - 连接问题一律降级为 skip
        return f"{type(exc).__name__}: {exc}"
    finally:
        await engine.dispose()


async def _maintenance_sql(url: str, *statements: str) -> None:
    """在维护库 `postgres` 上执行 DDL（建/删隔离库）。"""
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT", poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            for statement in statements:
                await connection.execute(text(statement))
    finally:
        await engine.dispose()


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _write_key(work: Path, name: str) -> tuple[Path, Path]:
    """生成 Ed25519 私钥（OpenSSH PEM）+ 公钥文件；返回 ``(私钥, 公钥)``。"""
    key = ed25519.Ed25519PrivateKey.generate()
    private = work / name
    public = work / f"{name}.pub"
    private.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.OpenSSH,
            serialization.NoEncryption(),
        )
    )
    public.write_text(signing.public_key_line(key) + "\n", encoding="utf-8")
    return private, public


def _payload(stdout: str) -> object:
    """取 stdout 的 JSON（``--json`` 输出即完整 JSON）。"""
    return json.loads(stdout[stdout.index("{") :] if "{" in stdout else stdout)


@dataclass
class _Service:
    """一次 e2e 会话的句柄：环境、密钥、CLI 调用器。"""

    env: dict[str, str]
    work: Path
    api_url: str
    keys: dict[str, Path] = field(default_factory=dict)
    fingerprints: dict[str, str] = field(default_factory=dict)

    def cli(
        self, *args: str, actor: str = "admin", stdin: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        """以某个身份跑一条 CLI 命令（**真进程、真签名**）。"""
        env = {**self.env, "AGENTICDOCER_SSH_KEY": str(self.keys[actor])}
        return subprocess.run(
            [sys.executable, "-m", "agenticdocer.cli", *args],
            cwd=ROOT,
            env=env,
            input=stdin,
            stdin=None if stdin is not None else subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )

    def ok(self, *args: str, actor: str = "admin", stdin: str | None = None) -> object:
        """跑命令并断言成功 → 返回 JSON。"""
        done = self.cli(*args, actor=actor, stdin=stdin)
        assert done.returncode == 0, f"{args} 退出码 {done.returncode}\nstdout={done.stdout}\nstderr={done.stderr}"
        return _payload(done.stdout)

    def fails(self, *args: str, actor: str = "admin", stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        """跑命令并断言**非零退出**（REQ-M11-F01b）。"""
        done = self.cli(*args, actor=actor, stdin=stdin)
        assert done.returncode != 0, f"{args} 竟然成功了：{done.stdout}"
        return done


def _wait_ready(api_url: str, server: subprocess.Popen[str]) -> None:
    """等 ``/healthz``（S4 豁免探针）就绪；进程提前退出则带输出报错。"""
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        if server.poll() is not None:
            output = server.stdout.read() if server.stdout else ""
            raise AssertionError(f"uvicorn 提前退出（code={server.returncode}）：\n{output}")
        try:
            with urllib.request.urlopen(f"{api_url}/healthz", timeout=1) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, ConnectionError, OSError):
            time.sleep(0.25)
    raise AssertionError(f"{STARTUP_TIMEOUT}s 内未就绪：{api_url}/healthz")


@pytest.fixture(scope="module")
def service(tmp_path_factory: pytest.TempPathFactory) -> Iterator[_Service]:
    """建隔离库 → alembic 迁移 → 起 uvicorn → 自举 admin → 登记三角色用户 → 跑完 DROP。"""
    app_url, owner_url = _app_url(), _owner_url()
    super_url = os.environ.get("PG_SUPER_URL") or SUPER_URL_DEFAULT
    error = asyncio.run(_probe(super_url))
    if error is not None:
        pytest.skip(f"PostgreSQL 不可用（{SUPER_URL_DEFAULT}）：{error}")

    # 建库需要超级用户（`agenticdocer` 无 CREATEDB）；OWNER 交给属主角色，迁移由其执行。
    asyncio.run(
        _maintenance_sql(
            super_url,
            f'DROP DATABASE IF EXISTS "{ISOLATED_DB}" WITH (FORCE)',
            f'CREATE DATABASE "{ISOLATED_DB}" OWNER {OWNER_ROLE}',
            f'GRANT CONNECT ON DATABASE "{ISOLATED_DB}" TO {APP_ROLE}',
        )
    )
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", owner_url)
    command.upgrade(config, "head")  # 迁移内含 §4.3 的 GRANT（含 schema USAGE / CONNECT）

    unreachable = asyncio.run(_probe(app_url))
    if unreachable is not None:
        pytest.skip(f"隔离库应用角色不可用：{unreachable}")

    work = tmp_path_factory.mktemp("m11-e2e")
    env = {
        **os.environ,
        "DATABASE_URL": app_url,
        "ASSET_STORE_DIR": str(work / "assets"),
        "IMPORT_WORK_DIR": str(work / "import_work"),
        "RENDER_OUT_DIR": str(work / "rendered"),
        "ADMIN_SSH_PUBKEY_FILE": str(work / "admin_ed25519.pub"),
        "LOG_DIR": str(work / "logs"),
        "IMPORT_SOURCE_ROOT": str(work),
    }
    keys: dict[str, Path] = {}
    fingerprints: dict[str, str] = {}
    for actor in ("admin", "editor", "reviewer", "reader"):
        private, public = _write_key(work, f"{actor}_ed25519")
        keys[actor] = private
        fingerprints[actor] = signing.fingerprint(public.read_text(encoding="utf-8").strip())

    port = _free_port()
    api_url = f"http://127.0.0.1:{port}"
    env.update({"AGENTICDOCER_API_URL": api_url, "API_HOST": "127.0.0.1", "API_PORT": str(port)})

    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "agenticdocer.app:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    handle = _Service(env=env, work=work, api_url=api_url, keys=keys, fingerprints=fingerprints)
    try:
        _wait_ready(api_url, server)
        boot = handle.ok("auth", "bootstrap", "--json")
        assert isinstance(boot, dict) and boot["username"] == "admin", boot
        for actor in ("editor", "reviewer", "reader"):
            handle.ok("user", "add", "--username", actor, "--role", actor, "--json")
            handle.ok("user", "key", "add", "--username", actor, "--key", str(work / f"{actor}_ed25519.pub"), "--json")
        yield handle
    finally:
        server.terminate()
        try:
            server.wait(timeout=20)
        except subprocess.TimeoutExpired:  # pragma: no cover - 兜底
            server.kill()
        asyncio.run(_maintenance_sql(super_url, f'DROP DATABASE IF EXISTS "{ISOLATED_DB}" WITH (FORCE)'))


# ----------------------------------------------------------------------
# REQ-M11-F04：身份自检与签名
# ----------------------------------------------------------------------


def test_whoami_reports_signed_identity(service: _Service) -> None:
    payload = service.ok("auth", "whoami", "--json", actor="editor")
    assert isinstance(payload, dict)
    assert payload["username"] == "editor"
    assert payload["role"] == "editor"
    assert payload["keyFingerprint"] == service.fingerprints["editor"]
    assert payload["apiUrl"] == service.api_url


def test_unregistered_key_is_rejected_with_actionable_hint(service: _Service) -> None:
    outsider, _ = _write_key(service.work, "outsider_ed25519")
    service.keys["outsider"] = outsider
    done = service.fails("doc", "list", "--json", actor="outsider")
    assert "user key add" in done.stderr


def test_dry_run_has_no_server_side_effect(service: _Service) -> None:
    """干跑只回放请求（V17b：固定 prompt 演练零副作用）。"""
    payload = service.ok(
        "node", "put", "--doc", DOC_ID, "--atom-type", "note", "--anchor", "x#1",
        "--content", '{"text":"dry"}', "--dry-run", actor="reader",
    )
    assert isinstance(payload, dict) and payload["dryRun"] is True
    assert payload["method"] == "POST"
    assert "parentNodeId" in payload["body"]  # 可选项显式 null（写入契约）


# ----------------------------------------------------------------------
# REQ-M11-F01：导入闭环 → 读取 / 渲染 / diff / 批注 / 统计
# ----------------------------------------------------------------------


@pytest.fixture(scope="module")
def imported(service: _Service) -> dict[str, object]:
    """跑完整导入闭环（parse → review → commit），返回 doc_id 与节点 id。"""
    src = service.work / "spec.md"
    src.write_text(SOURCE_MD, encoding="utf-8")
    parsed = service.ok("import", "parse", str(src), "--doc-slug", DOC_SLUG, "--json", actor="editor")
    assert isinstance(parsed, dict) and parsed["docMeta"]["doc_id"] == DOC_ID

    reviewed = service.ok(
        "import", "review", DOC_SLUG, "--accept-confident", "--json", actor="editor", stdin="a\n" * 64
    )
    assert isinstance(reviewed, dict)
    committed = service.ok("import", "commit", DOC_SLUG, "--json", actor="editor")
    assert isinstance(committed, dict)
    assert committed["docId"] == DOC_ID
    assert committed["violations"] == []
    assert committed["accepted"] >= 1

    diff = service.ok("doc", "diff", DOC_ID, "--json", actor="reader")
    assert isinstance(diff, dict)
    node_ids = [change["nodeId"] for change in diff["changes"] if change["op"] in ("added", "modified")]
    assert node_ids, diff
    return {"doc_id": DOC_ID, "node_id": node_ids[0], "node_ids": node_ids}


def test_doc_list_and_get(service: _Service, imported: dict[str, object]) -> None:
    docs = service.ok("doc", "list", "--json", actor="reader")
    assert isinstance(docs, list)
    assert [doc["docId"] for doc in docs] == [imported["doc_id"]]

    doc = service.ok("doc", "get", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(doc, dict)
    assert doc["title"] == "M11 端到端样例"
    assert doc["status"] == "draft"


def test_node_get_and_render(service: _Service, imported: dict[str, object]) -> None:
    node = service.ok(
        "node", "get", str(imported["node_id"]), "--doc", str(imported["doc_id"]), "--json", actor="reader"
    )
    assert isinstance(node, dict)
    assert node["version"] >= 1
    assert node["anchor"].startswith(DOC_ID)

    rendered = service.ok("render", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(rendered, dict)
    assert "M11 端到端样例" in rendered["markdown"]

    local = service.work / "local.md"
    saved = service.ok("render", str(imported["doc_id"]), "--out", str(local), "--json", actor="reader")
    assert isinstance(saved, dict) and local.read_text(encoding="utf-8")


def test_stats_import_coverage_and_health_gate(service: _Service) -> None:
    coverage = service.ok("stats", DOC_SLUG, "--json", actor="editor")
    assert isinstance(coverage, dict) and "coverage" in coverage

    health = service.ok("stats", "--health", "--json", actor="admin")
    assert isinstance(health, dict)
    assert health["verdict"] in ("ok", "degraded", "fail")

    denied = service.fails("stats", "--health", "--json", actor="editor")
    assert "admin" in denied.stderr


# ----------------------------------------------------------------------
# REQ-M11-F02：写入 + 乐观锁 + diff
# ----------------------------------------------------------------------


def _node_payload(node: dict, version: int, text: str | None = None) -> dict:
    """NodeIn 全字段（可选项显式 null——M01 写入契约 `extra=forbid` 要求）。"""
    content = dict(node["content"])
    if text is not None:
        content["text"] = text
    return {
        "nodeId": node["nodeId"],
        "docId": node["docId"],
        "atomType": node["atomType"],
        "format": node["format"],
        "ordinal": node["ordinal"],
        "parentNodeId": node["parentNodeId"],
        "level": node["level"],
        "anchor": node["anchor"],
        "content": content,
        "expectedVersion": version,
    }


def _write_patch(service: _Service, name: str, payload: dict) -> Path:
    path = service.work / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def test_write_round_trip_with_optimistic_lock(service: _Service, imported: dict[str, object]) -> None:
    node = service.ok(
        "node", "get", str(imported["node_id"]), "--doc", str(imported["doc_id"]), "--json", actor="editor"
    )
    assert isinstance(node, dict)
    patch = _write_patch(
        service, "patch.json", _node_payload(node, node["version"], "传输在时钟上升沿采样（e2e 修订）")
    )
    updated = service.ok("node", "put", "--file", str(patch), "--json", actor="editor")
    assert isinstance(updated, dict)
    assert updated["version"] == node["version"] + 1

    stale = _write_patch(service, "stale.json", _node_payload(node, node["version"], "过期版本"))
    denied = service.fails("node", "put", "--file", str(stale), "--json", actor="editor")
    assert "乐观锁" in denied.stderr  # 409 → 重读后重试的指引

    diff = service.ok("doc", "diff", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(diff, dict)
    assert any(change["op"] == "modified" for change in diff["changes"]), diff


def test_reader_cannot_write_and_gets_actionable_hint(service: _Service, imported: dict[str, object]) -> None:
    node = service.ok(
        "node", "get", str(imported["node_id"]), "--doc", str(imported["doc_id"]), "--json", actor="reader"
    )
    assert isinstance(node, dict)
    patch = _write_patch(service, "reader-patch.json", _node_payload(node, node["version"]))
    denied = service.fails("node", "put", "--file", str(patch), "--json", actor="reader")
    assert "editor" in denied.stderr  # 所需角色名
    assert "agenticdocer grant add" in denied.stderr  # 授权命令原文
    assert "--permission write" in denied.stderr


# ----------------------------------------------------------------------
# REQ-M11-F06：人类标注调取（含锚定版本上下文）
# ----------------------------------------------------------------------


def test_annotation_flow_including_anchor_context(service: _Service, imported: dict[str, object]) -> None:
    created = service.ok(
        "comment", "add", "--node", str(imported["node_id"]), "--body", "人类评审：请补一张时序图",
        "--json", actor="reviewer",
    )
    assert isinstance(created, dict)
    assert created["state"] == "open"
    assert created["targetEventId"]  # 服务端按节点最近事件自动回填

    listed = service.ok(
        "comment", "list", "--doc", str(imported["doc_id"]), "--state", "open", "--with-context", "--json",
        actor="reader",
    )
    assert isinstance(listed, list) and listed
    comment = listed[0]
    assert comment["commentId"] == created["commentId"]
    assert comment["body"] == "人类评审：请补一张时序图"
    assert comment["context"]["anchorEventId"] == created["targetEventId"]
    assert comment["context"]["nodeMissing"] is False
    assert comment["context"]["node"]["nodeId"] == imported["node_id"]

    resolved = service.ok(
        "comment", "resolve", str(created["commentId"]), "--expected-version", str(created["version"]),
        "--json", actor="reviewer",
    )
    assert isinstance(resolved, dict) and resolved["state"] == "resolved"

    open_now = service.ok(
        "comment", "list", "--doc", str(imported["doc_id"]), "--state", "open", "--json", actor="reader"
    )
    assert isinstance(open_now, list) and all(item["state"] == "open" for item in open_now)

    denied = service.fails(
        "comment", "add", "--node", str(imported["node_id"]), "--body", "reader 不应能批注", "--json", actor="reader"
    )
    assert "reviewer" in denied.stderr


# ----------------------------------------------------------------------
# REQ-M11-F03：用户与授权管理（admin）
# ----------------------------------------------------------------------


def test_admin_user_and_grant_lifecycle(service: _Service, imported: dict[str, object]) -> None:
    users = service.ok("user", "list", "--json")
    assert isinstance(users, list)
    assert {user["username"] for user in users} >= {"admin", "editor", "reviewer", "reader"}

    promoted = service.ok("user", "role", "--username", "reviewer", "--role", "editor", "--json")
    assert isinstance(promoted, dict) and promoted["role"] == "editor"
    service.ok("user", "role", "--username", "reviewer", "--role", "reviewer", "--json")

    grant = service.ok(
        "grant", "add", "--username", "reader", "--scope", "doc", "--value", str(imported["doc_id"]),
        "--permission", "read", "--json",
    )
    assert isinstance(grant, dict) and grant["scope"] == "doc"

    grants = service.ok("grant", "list", "--username", "reader", "--json")
    assert isinstance(grants, list) and grants[0]["grantId"] == grant["grantId"]

    removed = service.ok("grant", "rm", "--grant-id", str(grant["grantId"]), "--json")
    assert isinstance(removed, dict) and removed["removed"] is True
    assert isinstance(service.ok("grant", "list", "--json"), list)

    service.ok("user", "disable", "--username", "reader", "--json")
    assert service.fails("doc", "list", "--json", actor="reader").returncode != 0  # S8：禁用即失效
    service.ok("user", "role", "--username", "reader", "--role", "reader", "--json")


def test_key_revocation_is_effective(service: _Service) -> None:
    """公钥吊销走请求体（指纹含 `/`、`+`，不能进路径）。"""
    revoked = service.ok(
        "user", "key", "revoke", "--username", "reviewer", "--fingerprint", service.fingerprints["editor"], "--json"
    )
    assert isinstance(revoked, dict) and revoked["revoked"] is True
    # editor 的密钥被吊销后其请求必须失败（对照组：reviewer 自己仍可用）
    assert service.fails("doc", "list", "--json", actor="editor").returncode != 0
    assert isinstance(service.ok("doc", "list", "--json", actor="reviewer"), list)


def test_non_admin_cannot_manage_users(service: _Service) -> None:
    denied = service.fails("user", "list", "--json", actor="reviewer")
    assert "admin" in denied.stderr
    assert "agenticdocer user role --username" in denied.stderr


def test_logs_wrapper_reaches_agentic_logger(service: _Service) -> None:
    """``logs`` 是 agentic-logger 的薄封装：真调用（服务进程已写日志到 LOG_DIR）。"""
    done = service.cli("logs", "stats", "--since", "1h")
    assert done.returncode == 0, done.stderr
