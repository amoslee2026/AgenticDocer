"""M11 CLI 端到端集成测试（**真实 PG + 真实 HTTP 进程 + 真实 SSH 签名**；REQ-M11-F01..F04）。

为什么这样测：CLI 的验收要件是「签名 → 调用 M06/M07 API → 成功」——只有真实 uvicorn 进程
（同一鉴权/RBAC 中间件）才能证明 CLI 与 WebUI 共用同一判定口径（P5），且 `CliRunner` 无法覆盖
**进程退出码**（REQ-M11-F01b：权限不足必须非零退出）。

**隔离库**：本用例在 `agenticdocer_m11_test` 上跑（自建自 DROP），不触碰共享 `agenticdocer_test`，
故可与其它 agent 的集成测试并存（M02Store 同法）。
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
import yaml
from alembic import command
from alembic.config import Config
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from agenticdocer.auth import signing

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
ISOLATED_DB = "agenticdocer_m11_test"
APP_URL_DEFAULT = "postgresql+asyncpg://agenticdocer_app@127.0.0.1:5432/agenticdocer_test"
OWNER_URL_DEFAULT = "postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer_test"
DOC_ID = "SPEC-M11-E2E"
DOC_SLUG = "M11-E2E"
STARTUP_TIMEOUT = 40.0

SOURCE_MD = f"""---
spec_id: {DOC_ID}
title: M11 端到端样例
doc_type: standard
status: draft
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


def _app_url() -> str:
    base = os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL") or APP_URL_DEFAULT
    return make_url(base).set(database=ISOLATED_DB).render_as_string(hide_password=False)


def _owner_url() -> str:
    """属主凭据 + 隔离库名（只借用户名/口令，不借库名——那是开发库）。"""
    base = make_url(os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL") or APP_URL_DEFAULT)
    owner = make_url(os.environ.get("MIGRATION_DATABASE_URL") or OWNER_URL_DEFAULT)
    return base.set(
        database=ISOLATED_DB, username=owner.username, password=owner.password
    ).render_as_string(hide_password=False)


async def _probe(url: str) -> str | None:
    engine = create_async_engine(url, poolclass=None)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return None
    except Exception as exc:  # noqa: BLE001 - 连接问题一律降级为 skip
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
async def _admin_sql(url: str, *statements: str) -> None:
    """在维护库 `postgres` 上执行 DDL（建/删隔离库）。"""
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
    try:
        async with engine.connect() as connection:
            for statement in statements:
                await connection.execute(text(statement))
    finally:
        await engine.dispose()


def _free_port() -> int:
    with socket.socket() as sock:
def _payload(stdout: str) -> object:
    """取 stdout 的 JSON（``--json`` 输出即完整 JSON）。"""
    return json.loads(stdout[stdout.index("{") :] if "{" in stdout else stdout)
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


@dataclass
class _Service:
    """一次 e2e 会话的全部句柄。"""

    env: dict[str, str]
    work: Path
    api_url: str
    keys: dict[str, Path] = field(default_factory=dict)
    pubs: dict[str, Path] = field(default_factory=dict)
    fingerprints: dict[str, str] = field(default_factory=dict)

    def cli(self, *args: str, actor: str = "admin", stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        """以某个身份跑一条 CLI 命令（真进程、真签名）。"""
        env = {**self.env, "AGENTICDOCER_SSH_KEY": str(self.keys[actor])}
        return subprocess.run(
            [sys.executable, "-m", "agenticdocer.cli", *args],
            cwd=ROOT,
            env=env,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )

    def ok(self, *args: str, actor: str = "admin", stdin: str | None = None) -> object:
        """跑命令并断言成功，返回解析后的 JSON。"""
        done = self.cli(*args, actor=actor, stdin=stdin)
        assert done.returncode == 0, f"{args} 退出码 {done.returncode}\nstdout={done.stdout}\nstderr={done.stderr}"
        return _payload(done.stdout)

    def fails(self, *args: str, actor: str = "admin", stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        """跑命令并断言**非零退出**（REQ-M11-F01b）。"""
        done = self.cli(*args, actor=actor, stdin=stdin)
        assert done.returncode != 0, f"{args} 竟然成功了：{done.stdout}"
        return done


def _payload(stdout: str) -> object:
    """取 stdout 里的 JSON（`--json` 输出即完整 JSON）。"""
    return json.loads(stdout[stdout.index("{") :] if stdout.lstrip().startswith("{") else stdout)


@pytest.fixture(scope="module")
def service(tmp_path_factory: pytest.TempPathFactory) -> Iterator[_Service]:
    """建隔离库 → 迁移 → 起 uvicorn → 自举 admin → 登记三个角色用户 → 跑完 DROP。"""
    app_url, owner_url = _app_url(), _owner_url()
    error = asyncio.run(_probe(app_url)) or asyncio.run(_probe(owner_url))
    if error is not None:
        pytest.skip(f"PostgreSQL 不可用：{error}")

    maintenance = make_url(owner_url).set(database="postgres").render_as_string(hide_password=False)
    asyncio.run(
        _admin_sql(
            maintenance,
            f'DROP DATABASE IF EXISTS "{ISOLATED_DB}" WITH (FORCE)',
            f'CREATE DATABASE "{ISOLATED_DB}"',
        )
    )
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", owner_url)
    command.upgrade(config, "head")

    work = tmp_path_factory.mktemp("m11-e2e")
    env = {
        **os.environ,
        "DATABASE_URL": app_url,
        "ASSET_STORE_DIR": str(work / "assets"),
        "IMPORT_WORK_DIR": str(work / "import_work"),
        "RENDER_OUT_DIR": str(work / "rendered"),
        "LOG_DIR": str(work / "logs"),
        "ADMIN_SSH_PUBKEY_FILE": str(work / "admin.pub"),
        "IMPORT_SOURCE_ROOT": str(work),
    }
    keys: dict[str, Path] = {}
    pubs: dict[str, Path] = {}
    fingerprints: dict[str, str] = {}
    for actor in ("admin", "editor", "reviewer", "reader"):
        private, public = _write_key(work, f"{actor}_ed25519")
        keys[actor], pubs[actor] = private, public
        fingerprints[actor] = signing.fingerprint(public.read_text(encoding="utf-8").strip())

    port = _free_port()
    api_url = f"http://127.0.0.1:{port}"
    env["AGENTICDOCER_API_URL"] = api_url
    env["API_HOST"] = "127.0.0.1"
    env["API_PORT"] = str(port)

    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "agenticdocer.app:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    service = _Service(env=env, work=work, api_url=api_url, keys=keys, pubs=pubs, fingerprints=fingerprints)
    try:
        _wait_ready(api_url, server)
        boot = service.ok("auth", "bootstrap", "--json")
        assert isinstance(boot, dict) and boot["username"] == "admin", boot
        for actor, role in (("editor", "editor"), ("reviewer", "reviewer"), ("reader", "reader")):
            service.ok("user", "add", "--username", actor, "--role", role, "--json")
            service.ok("user", "key", "add", "--username", actor, "--key", str(pubs[actor]), "--json")
        yield service
    finally:
        server.terminate()
        try:
            server.wait(timeout=20)
        except subprocess.TimeoutExpired:  # pragma: no cover - 兜底
            server.kill()
        asyncio.run(_admin_sql(maintenance, f'DROP DATABASE IF EXISTS "{ISOLATED_DB}" WITH (FORCE)'))


def _wait_ready(api_url: str, server: subprocess.Popen[str]) -> None:
    """等 ``/healthz``（S4 豁免探针）就绪；失败则带进程输出报错。"""
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        if server.poll() is not None:  # pragma: no cover - 启动失败路径
            raise AssertionError(f"uvicorn 提前退出：{server.stdout.read() if server.stdout else ''}")
        try:
            with urllib.request.urlopen(f"{api_url}/healthz", timeout=1) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.25)
    raise AssertionError(f"{STARTUP_TIMEOUT}s 内未就绪：{api_url}/healthz")  # pragma: no cover


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


# ----------------------------------------------------------------------
# REQ-M11-F01：导入 / 读取 / 渲染 / diff / 批注 / 统计
# ----------------------------------------------------------------------


@pytest.fixture(scope="module")
def imported(service: _Service, tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    """跑完整导入闭环（parse → review → commit），返回 doc_id 与节点 id。"""
    src = service.work / "spec.md"
    src.write_text(SOURCE_MD, encoding="utf-8")
    parsed = service.ok("import", "parse", str(src), "--doc-slug", DOC_SLUG, "--json", actor="editor")
    assert isinstance(parsed, dict) and parsed["docMeta"]["spec_id"] == DOC_ID

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
    return {"doc_id": DOC_ID, "node_id": node_ids[0], "node_ids": node_ids, "commit": committed}


def test_doc_list_and_get(service: _Service, imported: dict[str, object]) -> None:
    docs = service.ok("doc", "list", "--json", actor="reader")
    assert isinstance(docs, list)
    assert [doc["docId"] for doc in docs] == [imported["doc_id"]]

    doc = service.ok("doc", "get", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(doc, dict)
    assert doc["title"] == "M11 端到端样例"
    assert doc["status"] == "draft"


def test_node_get_by_id_and_anchor(service: _Service, imported: dict[str, object]) -> None:
    node = service.ok(
        "node", "get", str(imported["node_id"]), "--doc", str(imported["doc_id"]), "--json", actor="reader"
    )
    assert isinstance(node, dict)
    assert node["nodeId"] == imported["node_id"]
    assert node["version"] >= 1
    assert node["anchor"].startswith(DOC_ID)


def test_render_document_and_section(service: _Service, imported: dict[str, object]) -> None:
    rendered = service.ok("render", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(rendered, dict)
    assert "M11 端到端样例" in rendered["markdown"]
    assert Path(rendered["outPath"]).name.endswith(".md")

    section = service.ok("render", str(imported["doc_id"]), "--section", "1", "--json", actor="reader")
    assert isinstance(section, dict)
    assert section["section"] == "1"

    local = service.work / "local.md"
    saved = service.ok(
        "render", str(imported["doc_id"]), "--out", str(local), "--json", actor="reader"
    )
    assert isinstance(saved, dict) and local.read_text(encoding="utf-8")


def test_stats_import_coverage_and_health(service: _Service) -> None:
    coverage = service.ok("stats", DOC_SLUG, "--json", actor="editor")
    assert isinstance(coverage, dict)
    assert "coverage" in coverage

    health = service.ok("stats", "--health", "--json", actor="admin")
    assert isinstance(health, dict)
    assert health["verdict"] in ("ok", "degraded", "fail")

    denied = service.fails("stats", "--health", "--json", actor="editor")
    assert "admin" in denied.stderr


# ----------------------------------------------------------------------
# REQ-M11-F02：diff；写入与乐观锁
# ----------------------------------------------------------------------


def test_node_write_round_trip_with_optimistic_lock(service: _Service, imported: dict[str, object]) -> None:
    node = service.ok("node", "get", str(imported["node_id"]), "--doc", str(imported["doc_id"]), "--json", actor="editor")
    assert isinstance(node, dict)
    patch = service.work / "patch.json"
    patch.write_text(
        json.dumps(
            {
                "docId": node["docId"],
                "nodeId": node["nodeId"],
                "atomType": node["atomType"],
                "anchor": node["anchor"],
                "format": node["format"],
                "ordinal": node["ordinal"],
                "content": {**node["content"], "text": "传输在时钟上升沿采样（M11 e2e 修订）"},
                "expectedVersion": node["version"],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    updated = service.ok("node", "put", "--file", str(patch), "--json", actor="editor")
    assert isinstance(updated, dict)
    assert updated["version"] == node["version"] + 1

    stale = service.work / "stale.json"
    stale.write_text(
        json.dumps({**json.loads(patch.read_text(encoding="utf-8")), "expectedVersion": node["version"]}),
        encoding="utf-8",
    )
    denied = service.fails("node", "put", "--file", str(stale), "--json", actor="editor")
    assert "乐观锁" in denied.stderr  # 409 → 重读后重试的指引

    diff = service.ok("doc", "diff", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(diff, dict)
    assert any(change["op"] == "modified" for change in diff["changes"]), diff


def test_reader_cannot_write_and_gets_actionable_hint(service: _Service, imported: dict[str, object]) -> None:
    node = service.ok("node", "get", str(imported["node_id"]), "--doc", str(imported["doc_id"]), "--json", actor="reader")
    assert isinstance(node, dict)
    patch = service.work / "reader-patch.json"
    patch.write_text(
        json.dumps(
            {
                "docId": node["docId"],
                "nodeId": node["nodeId"],
                "atomType": node["atomType"],
                "anchor": node["anchor"],
                "format": node["format"],
                "ordinal": node["ordinal"],
                "content": node["content"],
                "expectedVersion": node["version"],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    denied = service.fails("node", "put", "--file", str(patch), "--json", actor="reader")
    assert "editor" in denied.stderr
    assert "agenticdocer grant add" in denied.stderr
    assert "--permission write" in denied.stderr


# ----------------------------------------------------------------------
# REQ-M11-F06：人类标注调取（含锚定版本上下文）
# ----------------------------------------------------------------------


def test_annotation_flow_including_anchor_context(service: _Service, imported: dict[str, object]) -> None:
    created = service.ok(
        "comment",
        "add",
        "--node",
        str(imported["node_id"]),
        "--body",
        "人类评审：请补一张时序图",
        "--json",
        actor="reviewer",
    )
    assert isinstance(created, dict)
    assert created["state"] == "open"
    assert created["targetEventId"]

    listed = service.ok(
        "comment", "list", "--doc", str(imported["doc_id"]), "--state", "open", "--with-context", "--json", actor="reader"
    )
    assert isinstance(listed, list) and listed
    comment = listed[0]
    assert comment["commentId"] == created["commentId"]
    assert comment["body"] == "人类评审：请补一张时序图"
    context = comment["context"]
    assert context["anchorEventId"] == created["targetEventId"]
    assert context["nodeMissing"] is False
    assert context["node"]["nodeId"] == imported["node_id"]

    resolved = service.ok(
        "comment",
        "resolve",
        str(created["commentId"]),
        "--expected-version",
        str(created["version"]),
        "--json",
        actor="reviewer",
    )
    assert isinstance(resolved, dict) and resolved["state"] == "resolved"

    open_now = service.ok("comment", "list", "--doc", str(imported["doc_id"]), "--state", "open", "--json", actor="reader")
    assert isinstance(open_now, list)

    reader_denied = service.fails(
        "comment", "add", "--node", str(imported["node_id"]), "--body", "reader 不应能批注", "--json", actor="reader"
    )
    assert "reviewer" in reader_denied.stderr


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
        "grant",
        "add",
        "--username",
        "reader",
        "--scope",
        "doc",
        "--value",
        str(imported["doc_id"]),
        "--permission",
        "read",
        "--json",
    )
    assert isinstance(grant, dict) and grant["scope"] == "doc"

    grants = service.ok("grant", "list", "--username", "reader", "--json")
    assert isinstance(grants, list) and grants[0]["grantId"] == grant["grantId"]

    removed = service.ok("grant", "rm", "--grant-id", str(grant["grantId"]), "--json")
    assert isinstance(removed, dict) and removed["removed"] is True
    service.ok("grant", "list", "--json")

    service.ok("user", "disable", "--username", "reader", "--json")
    disabled = service.fails("doc", "list", "--json", actor="reader")
    assert disabled.returncode != 0  # S8：禁用即失效
    service.ok("user", "role", "--username", "reader", "--role", "reader", "--json")


def test_non_admin_cannot_manage_users(service: _Service) -> None:
    denied = service.fails("user", "list", "--json", actor="editor")
    assert "admin" in denied.stderr
    assert "agenticdocer user role --username" in denied.stderr


def test_logs_subcommand_reaches_agentic_logger(service: _Service) -> None:
    """`logs` 是 agentic-logger 的薄封装：真实调用（服务进程已写日志）。"""
    done = service.cli("logs", "list-files")
    assert done.returncode == 0, done.stderr
    assert "jsonl" in done.stdout or "No log files" in done.stdout


def test_generated_documents_are_clean_yaml(service: _Service) -> None:
    """防回归：skills frontmatter 必须能被 YAML 解析（机检入口与运行期同源）。"""
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text.split("\n---\n", 1)[0][4:])
        assert set(data) == {"name", "description", "role", "command"}, path
