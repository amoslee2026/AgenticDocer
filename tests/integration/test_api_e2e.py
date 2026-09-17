"""M06/M07 端到端集成（**真实 PG + 真实 HTTP 面**；REQ-M06-F01/F02、REQ-M07-F01..F06）。

链路：无凭据 401（S4 fail-closed）→ SSH 签名读写（agent 路径）→ 挑战-响应登录与会话 Cookie
（WebUI 路径）→ 节点写入/乐观锁/软删 → 章节清单 → 渲染（整档 + 章节）→ 文档 diff（B11）→
批注/状态流转/表格回写 → schema/术语 → 事件重放 → admin 指标与健康（admin 专属）→
用户/密钥/授权管理 → RBAC 403 与 grant 收窄。

装配与运行方式同生产：`create_app(db=…, storage=…)` + `httpx.ASGITransport`，生命周期
（管理员自举 + 过期清理）用 `app.router.lifespan_context` 显式驱动（等价 uvicorn 的 startup/shutdown）。

**用例隔离（可共存、可重跑）**：所有 doc_id / 用户名 / 术语 / schema 类型均带**本次运行令牌**
（`_TOKEN`），且断言**不依赖任何表为空**（只做「我的数据」作用域内的成员/计数断言）。
故本模块与 `conftest.migrated_schema` 的**默认模式**（仅幂等 `alembic upgrade head`，不清库）
兼容：`uv run pytest tests/integration/test_api_e2e.py -q` 即可，无需独占库；只有需要
「干净空库」时才另带 `AGENTICSPEC_TEST_DROP_SCHEMA=1` 并广播申请独占。
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from agenticspec.app import create_app
from agenticspec.auth import sessions, signing
from agenticspec.auth import users as auth_users
from agenticspec.model import DocIn, WriteContext
from agenticspec.store import Database, Storage

pytestmark = pytest.mark.integration

ACTOR_SYSTEM = WriteContext(actor="system", source="system")

_TOKEN = uuid4().hex[:8]
"""本次运行的唯一令牌：与其它 agent / 先前运行的数据互不干扰。"""

DOC_AGENT = f"SPEC-E2E-AGENT-{_TOKEN}"
DOC_RBAC_STD = f"SPEC-E2E-RBAC-STD-{_TOKEN}"
DOC_RBAC_PRD = f"SPEC-E2E-RBAC-PRD-{_TOKEN}"
DOC_SESSION = f"SPEC-E2E-SESSION-{_TOKEN}"
DOC_EDGES = f"SPEC-E2E-EDGES-{_TOKEN}"
DOC_MISSING = f"SPEC-MISSING-{_TOKEN}"
ADMIN_USERNAME = f"e2e-admin-{_TOKEN}"
USER_READER = f"e2e-reader-{_TOKEN}"
USER_EDITOR = f"e2e-editor-{_TOKEN}"
TERM = f"APB-{_TOKEN}"
SCHEMA_TYPE = f"clause.test-{_TOKEN}"
"""测试专用 schema 类型（`schemas.type_name` 无取值域约束；不占用内建原子的版本位）。"""


# ------------------------------------------------------------------ 夹具


@pytest.fixture(scope="module")
def keys(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """四把**本次运行唯一**的测试私钥（`bootstrap` / `admin` / `editor` / `reader`）。

    `bootstrap` 专供 `ADMIN_SSH_PUBKEY_FILE`（M10 自举用），**不与任何测试身份共用**：
    用户公钥在库里**全局唯一**（防身份冒用），若自举键与本模块自有 admin 键相同，则
    「干净库」下自举先把它登记给 `admin`，随后本模块登记同一公钥给 `e2e-admin-…` 会 409
    （全量验收实测的隔离缺陷）。
    """
    directory = tmp_path_factory.mktemp("api_keys")
    paths: dict[str, Path] = {}
    for name in ("bootstrap", "admin", "editor", "reader"):
        key = ed25519.Ed25519PrivateKey.generate()
        private = directory / name
        private.write_bytes(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.OpenSSH,
                serialization.NoEncryption(),
            )
        )
        private.with_suffix(".pub").write_text(signing.public_key_line(key) + "\n")
        paths[name] = private
    return paths


@pytest.fixture(autouse=True)
def auth_env(keys: dict[str, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """自举公钥指向**专用 bootstrap 键**；放开限流并隔离渲染产物目录。"""
    public = tmp_path / "bootstrap.pub"
    public.write_text(keys["bootstrap"].with_suffix(".pub").read_text())
    monkeypatch.setenv("ADMIN_SSH_PUBKEY_FILE", str(public))
    monkeypatch.setenv("AUTH_RATE_LIMIT_PER_MIN", "1000")
    monkeypatch.setenv("RENDER_OUT_DIR", str(tmp_path / "rendered"))
    sessions.reset_rate_limits()
    auth_users.reset_failure_aggregates()


@pytest.fixture
async def client(database: Database, storage: Storage) -> AsyncIterator[AsyncClient]:
    """装配真实应用（注入测试库与存储），并跑一次生命周期。"""
    application = create_app(db=database, storage=storage)
    transport = ASGITransport(app=application)
    async with application.router.lifespan_context(application):
        async with AsyncClient(transport=transport, base_url="http://testserver") as http_client:
            yield http_client


class Signer:
    """逐请求 SSHSIG 签名客户端（§3 M06 载荷规范；每次新 `X-Nonce`/`X-Timestamp`）。

    `path` 必须是**线上形态**（query 已百分号编码）——签名覆盖 RAW_PATH 原样字节（S2）。
    """

    def __init__(self, client: AsyncClient, private_key: Path) -> None:
        self.client = client
        self.key = signing.load_private_key(private_key)
        self.key_id = signing.fingerprint(private_key.with_suffix(".pub").read_text())

    async def request(self, method: str, path: str, body: Any = None, **extra: Any) -> Any:
        payload = None if body is None else json.dumps(body).encode("utf-8")
        headers = signing.sign_request_headers(self.key, method, path, payload)
        if payload is not None:
            headers["Content-Type"] = "application/json"
        headers.update(extra.pop("headers", {}))
        return await self.client.request(method, path, content=payload, headers=headers, **extra)

    async def get(self, path: str, **extra: Any) -> Any:
        return await self.request("GET", path, **extra)

    async def post(self, path: str, body: Any = None, **extra: Any) -> Any:
        return await self.request("POST", path, body, **extra)


@pytest.fixture
async def admin_id(database: Database, keys: dict[str, Path]) -> UUID:
    """本模块**自己的** admin 用户（唯一用户名）+ 公钥，幂等登记。

    不复用 M10 的 `bootstrap_admin`：那条路径以「是否存在 active admin」为幂等条件
    （REQ-M10-F05/S9），遇到其它模块/先前运行留下的 admin 就会跳过，从而**无法**登记本次
    运行的随机测试密钥。自带唯一 admin 用户则与任何既有数据共存、且可重复运行。
    """
    user = await auth_users.find_user_by_username(ADMIN_USERNAME, db=database)
    if user is None:
        user = await auth_users.create_user(ADMIN_USERNAME, "admin", actor="system", db=database)
    fingerprint = signing.fingerprint(keys["admin"].with_suffix(".pub").read_text())
    registered = {key.key_id for key in await auth_users.list_ssh_keys(user.user_id, db=database)}
    if fingerprint not in registered:
        await auth_users.add_ssh_key(
            user.user_id,
            keys["admin"].with_suffix(".pub").read_text().strip(),
            actor="system",
            db=database,
        )
    return user.user_id


@pytest.fixture
def admin(client: AsyncClient, keys: dict[str, Path], admin_id: UUID) -> Signer:
    """以本模块自有 admin 身份签名的客户端。"""
    return Signer(client, keys["admin"])


async def _seed_doc(
    storage: Storage, doc_id: str, *, doc_type: str = "standard", **meta: Any
) -> None:
    """文档由 M03 导入器创建（M06/M07 无文档创建端点，§3 端点表）；此处直接经 M02 播种。"""
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type=doc_type,
            title=f"Test {doc_id}",
            meta={"editable_tables": True, **meta},
            source_ref=None,
        ),
        None,
        ACTOR_SYSTEM,
    )


def _node_body(
    doc_id: str,
    anchor: str,
    *,
    ordinal: int,
    content: dict[str, Any],
    atom_type: str = "clause",
    level: int | None = 1,
    parent_node_id: UUID | None = None,
    node_id: UUID | None = None,
    expected_version: int | None = None,
    format: str = "md",  # noqa: A002 —— 与 §3.0 `NodeIn.format` 同名（HTTP 契约字段）
) -> dict[str, Any]:
    """§3.0 `NodeIn` 的完整请求体（可选字段按 §3.0 口径**显式给 null**）。"""
    return {
        "nodeId": None if node_id is None else str(node_id),
        "docId": doc_id,
        "atomType": atom_type,
        "format": format,
        "ordinal": ordinal,
        "parentNodeId": None if parent_node_id is None else str(parent_node_id),
        "level": level,
        "anchor": f"{doc_id}#{anchor}",  # M01 锚口径 `<doc_id>#…`（M09A `M09A.anchor.doc_id` 强校验）
        "content": content,
        "expectedVersion": expected_version,
    }


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ------------------------------------------------------------ 主链路（agent 路径）


async def test_agent_flow_read_write_render_diff(
    admin: Signer, storage: Storage, database: Database, admin_id: UUID
) -> None:
    """REQ-M06-F01/F02 + REQ-M07-F06：鉴权 → 读写 → 章节 → 渲染 → diff → 批注 → 管理端点。"""
    doc_id = DOC_AGENT
    await _seed_doc(storage, doc_id)

    # ── 无凭据：豁免清单外一律 401（S4 fail-closed）
    assert (await admin.client.get("/api/v1/docs")).status_code == 401
    assert (await admin.client.get(f"/api/v1/docs/{doc_id}")).status_code == 401
    assert (await admin.client.post("/api/v1/nodes", json={})).status_code == 401
    assert (await admin.client.get("/healthz")).status_code == 200
    assert (await admin.client.post("/api/v1/auth/challenge")).status_code == 200

    before_writes = _utc_now()

    # ── 结构化写入（S14：伪造 X-Actor 不改变身份）
    chapter = await admin.post(
        "/api/v1/nodes",
        _node_body(doc_id, "1 Scope", ordinal=0, content={"text": "Scope of the document"}),
        headers={"X-Actor": "someone-else"},
    )
    assert chapter.status_code == 200, chapter.text
    chapter_node = chapter.json()
    assert chapter_node["nodeId"] and chapter_node["version"] == 1
    assert chapter_node["docId"] == doc_id and chapter_node["atomType"] == "clause"
    assert chapter_node["status"] == "active" and chapter_node["anchor"] == f"{doc_id}#1 Scope"

    section = await admin.post(
        "/api/v1/nodes",
        _node_body(
            doc_id,
            "1.1 Purpose",
            ordinal=1,
            level=2,
            parent_node_id=UUID(chapter_node["nodeId"]),
            content={"text": "Purpose of this section"},
        ),
    )
    assert section.status_code == 200, section.text

    table = await admin.post(
        "/api/v1/nodes",
        _node_body(
            doc_id,
            "1.2 Registers",
            ordinal=2,
            level=2,
            parent_node_id=UUID(chapter_node["nodeId"]),
            atom_type="table",
            format="html",  # E1-a：HTML `<table>` 片段 → format 必须为 html（M09A `M09A.table.format`）
            content={
                "fragment": "<table><tr><th>Name</th></tr><tr><td>A</td></tr></table>",
                "meta": {"rows": 2, "cols": 1, "cells": 2, "max_colspan": 1},
            },
        ),
    )
    assert table.status_code == 200, table.text
    table_node = table.json()

    after_nodes = _utc_now()  # 三个节点已创建、尚未更新（用于「修改」窗口的下界）

    # ── 写入门（REQ-M06-F01/F02）：缺 text 的 clause → 422 + violations（含 fixHint）
    invalid = await admin.post(
        "/api/v1/nodes", _node_body(doc_id, "1.3 Bad", ordinal=3, content={})
    )
    assert invalid.status_code == 422, invalid.text
    body = invalid.json()
    assert body["error"] == "validation"
    assert {item["ruleId"] for item in body["violations"]}
    assert any(item.get("fixHint") for item in body["violations"])

    unknown = await admin.post(
        "/api/v1/nodes",
        _node_body(doc_id, "1.3 Bad", ordinal=3, atom_type="nonsense", content={"text": "x"}),
    )
    assert unknown.status_code == 422
    unknown_ids = {item["ruleId"] for item in unknown.json()["violations"]}
    assert {"M09A.atom.unknown", "M01.doc_type.atom"} <= unknown_ids  # 判据归属（顺序无关）

    # 判据归属（P5）：锚形态由 M09A `M09A.anchor.doc_id` 负责——本模块不再自带第二套判定
    bad_anchor = _node_body(doc_id, "1 Bad", ordinal=3, content={"text": "x"})
    bad_anchor["anchor"] = "1 Bad"  # 缺 `<doc_id>#` 前缀
    rejected = await admin.post("/api/v1/nodes", bad_anchor)
    assert rejected.status_code == 422, rejected.text
    assert rejected.json()["violations"][0]["ruleId"] == "M09A.anchor.doc_id"

    # ── 点查（doc_id 可选 → 分区裁剪；ADR-009 V16）与乐观锁
    node_id = chapter_node["nodeId"]
    fetched = await admin.get(f"/api/v1/nodes/{node_id}?doc_id={doc_id}")
    assert fetched.status_code == 200 and fetched.json()["version"] == 1
    assert (await admin.get(f"/api/v1/nodes/{node_id}")).status_code == 200

    updated = await admin.post(
        "/api/v1/nodes",
        _node_body(
            doc_id,
            "1 Scope",
            ordinal=0,
            node_id=UUID(node_id),
            expected_version=1,
            content={"text": "Scope of the document (revised)"},
        ),
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["version"] == 2

    conflict = await admin.post(
        "/api/v1/nodes",
        _node_body(
            doc_id,
            "1 Scope",
            ordinal=0,
            node_id=UUID(node_id),
            expected_version=1,
            content={"text": "stale write"},
        ),
    )
    assert conflict.status_code == 409, conflict.text
    assert conflict.json()["error"] == "conflict"

    # ── 文档节点树与章节清单（B10）
    nodes = await admin.get(f"/api/v1/docs/{doc_id}/nodes")
    assert nodes.status_code == 200
    assert {node["nodeId"] for node in nodes.json()} >= {
        node_id,
        section.json()["nodeId"],
        table_node["nodeId"],
    }

    sections = await admin.get(f"/api/v1/docs/{doc_id}/sections")
    assert sections.status_code == 200
    listing = sections.json()
    assert listing and {"nodeId", "anchor", "title", "level", "ordinal", "childCount"} <= set(
        listing[0]
    )
    assert any(
        item["anchor"] == f"{doc_id}#1 Scope" and item["childCount"] >= 3 for item in listing
    )

    # ── 渲染（整档 + 单章节，B10）
    rendered = await admin.get(f"/api/v1/docs/{doc_id}/render")
    assert rendered.status_code == 200, rendered.text
    whole = rendered.json()
    assert {"docId", "outPath", "assetsExported", "markdown", "section"} <= set(whole)
    # 渲染口径由 M04 决定：标题层级来自 `level`、正文来自原子文本（锚不进正文）
    assert "Scope of the document (revised)" in whole["markdown"]
    assert "Purpose of this section" in whole["markdown"]
    assert "<table>" in whole["markdown"]  # HTML 片段零改写直通（P4）
    assert Path(whole["outPath"]).is_file()

    # 锚含 `#` 与空格：签名覆盖 RAW_PATH（S2），故按**线上形态**编码（`#`→%23、空格→%20）
    anchor = f"{doc_id}#1.1 Purpose"
    encoded = anchor.replace("#", "%23").replace(" ", "%20")
    section_render = await admin.get(f"/api/v1/docs/{doc_id}/render?section={encoded}")
    assert section_render.status_code == 200, section_render.text
    assert section_render.json()["section"] == anchor
    assert "Purpose of this section" in section_render.json()["markdown"]
    assert "<table>" not in section_render.json()["markdown"]  # 同级表格不在该章节子树内

    triggered = await admin.post(f"/api/v1/docs/{doc_id}/render")
    assert triggered.status_code == 200 and triggered.json()["markdown"]

    # ── 事件（身份取自验签，不取 X-Actor）与版本重放
    events = await admin.get(f"/api/v1/events?entity=node&entity_id={node_id}")
    assert events.status_code == 200
    history = events.json()
    assert len(history) >= 2 and history[0]["op"] == "create"
    assert {item["actor"] for item in history} == {str(admin_id)}  # 伪造的 X-Actor 未被采信
    event_id = history[0]["eventId"]

    replay = await admin.get(f"/api/v1/events/replay?node_id={node_id}&upto={event_id}")
    assert replay.status_code == 200, replay.text
    snapshot = replay.json()
    assert snapshot["node"]["content"]["text"] == "Scope of the document"
    assert len(snapshot["history"]) == 1

    current = await admin.get(f"/api/v1/events/replay?node_id={node_id}")
    assert current.status_code == 200
    assert current.json()["node"]["content"]["text"] == "Scope of the document (revised)"

    # ── 文档 diff（B11/REQ-M07-F06）
    # ① 下界早于建节点 → 三个节点都记「新增」（节点级条目：field="node"，before/after 为节点视图）
    diff = await admin.get(
        f"/api/v1/docs/{doc_id}/diff?from={before_writes.isoformat()}&to={_utc_now().isoformat()}"
    )
    assert diff.status_code == 200, diff.text
    payload = diff.json()
    assert {"docId", "fromTs", "toTs", "changes", "summary"} <= set(payload)
    added_nodes = {
        entry["nodeId"]
        for entry in payload["changes"]
        if entry["op"] == "added" and entry["field"] == "node"
    }
    assert {node_id, section.json()["nodeId"], table_node["nodeId"]} <= added_nodes
    assert payload["summary"]["added"] >= 3

    # ② 下界在「建节点之后、更新之前」→ 同一节点逐字段给出 before/after
    edits = await admin.get(
        f"/api/v1/docs/{doc_id}/diff?from={after_nodes.isoformat()}&to={_utc_now().isoformat()}"
    )
    assert edits.status_code == 200, edits.text
    edited = [
        entry
        for entry in edits.json()["changes"]
        if entry["nodeId"] == node_id and entry["op"] == "modified"
    ]
    assert {"content", "version"} <= {entry["field"] for entry in edited}
    content_change = next(entry for entry in edited if entry["field"] == "content")
    assert content_change["before"]["text"] == "Scope of the document"
    assert content_change["after"]["text"] == "Scope of the document (revised)"
    assert content_change["anchor"] == f"{doc_id}#1 Scope"

    empty = await admin.get(f"/api/v1/docs/{doc_id}/diff?from=1&to=1")
    assert empty.status_code == 200
    assert empty.json()["changes"] == []  # 无变更时返回空 diff（非 404）

    default_range = await admin.get(f"/api/v1/docs/{doc_id}/diff")
    assert default_range.status_code == 200
    assert {"added", "modified", "deleted", "refs"} == set(default_range.json()["summary"])

    # ── 引用边（增/删各写 ref 事件；diff 标注引用变化）
    ref_body = {
        "src": node_id,
        "dstDoc": doc_id,
        "dstNode": section.json()["nodeId"],
        "kind": "see_also",
    }
    created_ref = await admin.post("/api/v1/refs", ref_body)
    assert created_ref.status_code == 201, created_ref.text
    assert created_ref.json()["kind"] == "see_also"

    # 上界 = 「此刻」之后无新事件 → 该窗口内无引用变化
    with_ref = await admin.get(f"/api/v1/docs/{doc_id}/diff?from={_utc_now().isoformat()}")
    assert with_ref.status_code == 200
    assert with_ref.json()["summary"]["refs"] == 0

    ref_window = await admin.get(
        f"/api/v1/docs/{doc_id}/diff?from={before_writes.isoformat()}&to={_utc_now().isoformat()}"
    )
    assert ref_window.status_code == 200
    ref_changes = [entry for entry in ref_window.json()["changes"] if entry["field"] == "ref"]
    assert len(ref_changes) == 1 and ref_changes[0]["op"] == "added"
    assert ref_changes[0]["after"]["kind"] == "see_also"

    assert (await admin.request("DELETE", "/api/v1/refs", ref_body)).status_code == 204
    assert (await admin.request("DELETE", "/api/v1/refs", ref_body)).status_code == 404

    # ── 批注（A4）与列表过滤
    comment = await admin.post(
        "/api/v1/comments", {"nodeId": node_id, "body": "请补时序图", "expectedVersion": 2}
    )
    assert comment.status_code == 201, comment.text
    comment_dto = comment.json()
    assert {
        "commentId",
        "nodeId",
        "body",
        "state",
        "author",
        "version",
        "ts",
        "targetEventId",
    } <= set(comment_dto)
    assert comment_dto["state"] == "open"

    by_node = await admin.get(f"/api/v1/comments?node_id={node_id}")
    assert by_node.status_code == 200 and len(by_node.json()) == 1
    by_doc = await admin.get(f"/api/v1/comments?doc_id={doc_id}")
    assert by_doc.status_code == 200 and len(by_doc.json()) == 1
    assert (await admin.get("/api/v1/comments")).status_code == 400
    assert (
        await admin.get(f"/api/v1/comments?node_id={node_id}&doc_id={doc_id}")
    ).status_code == 400

    resolved = await admin.request(
        "PATCH",
        f"/api/v1/comments/{comment_dto['commentId']}",
        {"state": "resolved", "expectedVersion": 1},
    )
    assert resolved.status_code == 200 and resolved.json()["state"] == "resolved"
    stale = await admin.request(
        "PATCH",
        f"/api/v1/comments/{comment_dto['commentId']}",
        {"state": "open", "expectedVersion": 1},
    )
    assert stale.status_code == 409

    # ── 状态流转（A17）
    doc = await admin.get(f"/api/v1/docs/{doc_id}")
    assert doc.status_code == 200 and doc.json()["status"] == "draft"
    version = doc.json()["version"]
    assert (
        await admin.post(
            f"/api/v1/docs/{doc_id}/status", {"status": "reviewed", "expectedVersion": 999}
        )
    ).status_code == 409
    reviewed = await admin.post(
        f"/api/v1/docs/{doc_id}/status", {"status": "reviewed", "expectedVersion": version}
    )
    assert reviewed.status_code == 200 and reviewed.json()["status"] == "reviewed"

    # ── 表格回写（B6/V8）：`<table>` HTML 片段恒**不可编辑**（P4 零改写直通，B6(d)）
    html_edit = await admin.request(
        "PATCH",
        f"/api/v1/nodes/{table_node['nodeId']}/table",
        {"rows": [["Name"], ["A"]], "expectedVersion": 1, "headerNames": ["Name"]},
    )
    assert html_edit.status_code == 403, html_edit.text

    # md 管道表（format=md）才走可编辑控件：行列 JSON → content，expectedVersion 乐观锁
    pipe_table = await admin.post(
        "/api/v1/nodes",
        _node_body(
            doc_id,
            "1.3 Pipe Registers",
            ordinal=3,
            level=2,
            parent_node_id=UUID(chapter_node["nodeId"]),
            atom_type="table",
            content={
                "fragment": "| Name | Bits |\n| --- | --- |\n| CTRL | 7:0 |",
                "meta": {"rows": 2, "cols": 2, "cells": 4, "max_colspan": 1},
            },
        ),
    )
    assert pipe_table.status_code == 200, pipe_table.text
    pipe_node = pipe_table.json()

    table_write = await admin.request(
        "PATCH",
        f"/api/v1/nodes/{pipe_node['nodeId']}/table",
        {
            "rows": [["Name", "Bits"], ["CTRL", "7:0"], ["STATUS", "15:8"]],
            "expectedVersion": 1,
            "headerNames": ["Name", "Bits"],
        },
    )
    assert table_write.status_code == 200, table_write.text
    assert table_write.json()["content"]["meta"]["rows"] == 3
    assert table_write.json()["version"] == 2
    assert (
        await admin.request(
            "PATCH",
            f"/api/v1/nodes/{pipe_node['nodeId']}/table",
            {"rows": [["X"]], "expectedVersion": 1},
        )
    ).status_code == 409
    # 非表格原子的行列编辑 → 422（M04 判定）
    assert (
        await admin.request(
            "PATCH", f"/api/v1/nodes/{node_id}/table", {"rows": [["X"]], "expectedVersion": 2}
        )
    ).status_code == 422

    # ── 节点软删（A2）：写 delete 事件并把该节点 open 批注置 orphaned
    second = await admin.post("/api/v1/comments", {"nodeId": node_id, "body": "再看一眼"})
    assert second.status_code == 201
    assert (
        await admin.request("DELETE", f"/api/v1/nodes/{node_id}?expected_version=1")
    ).status_code == 409
    deleted = await admin.request("DELETE", f"/api/v1/nodes/{node_id}?expected_version=2")
    assert deleted.status_code == 204, deleted.text
    assert (await admin.get(f"/api/v1/nodes/{node_id}")).status_code == 404
    orphaned = await admin.get(f"/api/v1/comments?node_id={node_id}")
    assert orphaned.status_code == 200
    assert {item["state"] for item in orphaned.json()} == {"resolved", "orphaned"}
    with_deleted = await admin.get(f"/api/v1/docs/{doc_id}/nodes?include_deleted=true")
    assert with_deleted.status_code == 200
    assert node_id in {node["nodeId"] for node in with_deleted.json()}
    assert node_id not in {
        node["nodeId"] for node in (await admin.get(f"/api/v1/docs/{doc_id}/nodes")).json()
    }

    # ── schema（A8/A16）与术语（R10）
    schemas = await admin.get("/api/v1/schemas")
    assert schemas.status_code == 200
    names = {item["typeName"] for item in schemas.json()}
    assert {
        "clause",
        "definition",
        "table",
        "figure",
        "code",
        "example",
        "note",
        "cross_ref",
    } <= names

    clause_schema = await admin.get("/api/v1/schemas/clause")
    assert clause_schema.status_code == 200
    assert {"typeName", "version", "jsonSchema"} <= set(clause_schema.json())

    custom = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}
    registered = await admin.post(
        "/api/v1/schemas", {"typeName": SCHEMA_TYPE, "jsonSchema": custom, "version": 1}
    )
    assert registered.status_code == 200, registered.text
    assert registered.json()["typeName"] == SCHEMA_TYPE
    assert (
        await admin.post(
            "/api/v1/schemas", {"typeName": SCHEMA_TYPE, "jsonSchema": custom, "version": 1}
        )
    ).status_code == 409  # 同 (type_name, version) 重复
    fetched_schema = await admin.get(f"/api/v1/schemas/{SCHEMA_TYPE}")
    assert fetched_schema.status_code == 200 and fetched_schema.json()["version"] == 1
    assert SCHEMA_TYPE in {
        item["typeName"] for item in (await admin.get("/api/v1/schemas")).json()
    }
    assert (await admin.get(f"/api/v1/schemas/nonsense-{_TOKEN}")).status_code == 404

    # 启动时幂等载入的规范用语种子（§5 `TERMS_SEED` → `data/terms_seed.yaml`，R10 第三条写入路径）
    terms = await admin.get("/api/v1/terms")
    assert terms.status_code == 200
    listed = {item["term"]: item["kind"] for item in terms.json()}
    assert {"MUST", "MUST NOT", "SHALL", "SHOULD NOT", "REQUIRED"} <= set(listed)
    assert listed["MUST"] == "normative-keyword"
    assert TERM not in listed
    created_term = await admin.post(
        "/api/v1/terms", {"term": TERM, "definitionNodeId": None, "kind": "normative-keyword"}
    )
    assert created_term.status_code == 200 and created_term.json()["kind"] == "normative-keyword"
    assert TERM in {item["term"] for item in (await admin.get("/api/v1/terms")).json()}
    keywords = {
        item["term"] for item in (await admin.get("/api/v1/terms?kind=normative-keyword")).json()
    }
    glossaries = {item["term"] for item in (await admin.get("/api/v1/terms?kind=glossary")).json()}
    assert TERM in keywords and TERM not in glossaries

    # 自清理：`terms` 无删除端点，经 M02 直连删掉本次令牌写入的测试术语（不留库内污染）
    async with database.transaction() as session:
        await session.execute(text("DELETE FROM terms WHERE term = :term"), {"term": TERM})
    assert TERM not in {item["term"] for item in (await admin.get("/api/v1/terms")).json()}

    assert (await admin.get("/api/v1/assets/" + "0" * 64)).status_code == 404

    # ── 管理端点（admin 专属，ADR-010）
    metrics = await admin.get("/api/v1/admin/metrics?window=3600")
    assert metrics.status_code == 200
    assert {"windowSeconds", "endpoints", "slowQueries", "authFailures", "render"} <= set(
        metrics.json()
    )
    assert metrics.json()["endpoints"]  # 中间件确实记了端点耗时
    health = await admin.get("/api/v1/admin/health")
    assert health.status_code == 200
    assert health.json()["verdict"] in {"ok", "degraded", "fail"}

    # ── 用户清单（含公钥指纹，§3 M07 `UserDTO`）
    users = await admin.get("/api/v1/users")
    assert users.status_code == 200
    admin_entry = next(item for item in users.json() if item["username"] == ADMIN_USERNAME)
    assert admin_entry["keyFingerprints"] and admin_entry["role"] == "admin"

    roles = await admin.get("/api/v1/roles")
    assert roles.status_code == 200
    assert {item["role"] for item in roles.json()} == {"admin", "editor", "reviewer", "reader"}


# ------------------------------------------------------------------ RBAC 与授权


async def test_rbac_and_grant_narrowing(
    admin: Signer,
    admin_id: UUID,
    client: AsyncClient,
    keys: dict[str, Path],
    storage: Storage,
    database: Database,
) -> None:
    """REQ-M10-F04 + §3 M06：角色硬上限（403）与 grant **收窄**（不扩权）。"""
    await _seed_doc(storage, DOC_RBAC_STD)
    await _seed_doc(storage, DOC_RBAC_PRD, doc_type="product")

    reader = await admin.post("/api/v1/users", {"username": USER_READER, "role": "reader"})
    assert reader.status_code == 201, reader.text
    reader_id = reader.json()["userId"]
    registered = await admin.post(
        f"/api/v1/users/{reader_id}/keys",
        {"publicKey": keys["reader"].with_suffix(".pub").read_text().strip()},
    )
    assert registered.status_code == 201, registered.text
    assert registered.json()["fingerprint"].startswith("SHA256:")

    editor = await admin.post("/api/v1/users", {"username": USER_EDITOR, "role": "editor"})
    assert editor.status_code == 201, editor.text
    editor_id = editor.json()["userId"]
    assert (
        await admin.post(
            f"/api/v1/users/{editor_id}/keys",
            {"publicKey": keys["editor"].with_suffix(".pub").read_text().strip()},
        )
    ).status_code == 201

    reader_client = Signer(client, keys["reader"])
    editor_client = Signer(client, keys["editor"])

    # reader：可读元数据，不可写/审/管理
    assert (await reader_client.get("/api/v1/docs")).status_code == 200
    write = await reader_client.post(
        "/api/v1/nodes",
        _node_body(DOC_RBAC_STD, "1 x", ordinal=0, content={"text": "reader write"}),
    )
    assert write.status_code == 403, write.text
    assert (
        await reader_client.post("/api/v1/comments", {"nodeId": str(UUID(int=1)), "body": "x"})
    ).status_code == 403
    assert (await reader_client.get("/api/v1/admin/metrics")).status_code == 403
    assert (await reader_client.get("/api/v1/admin/health")).status_code == 403
    assert (await reader_client.get("/api/v1/users")).status_code == 403
    # AUD-7：角色清单与鉴权审计均 admin 专属（后者含来源 IP / claimed_*，S10）
    assert (await reader_client.get("/api/v1/roles")).status_code == 403
    assert (await reader_client.get("/api/v1/events?entity=auth")).status_code == 403
    assert (await reader_client.get("/api/v1/events?limit=1000")).status_code == 200
    assert "auth" not in {
        item["entity"] for item in (await reader_client.get("/api/v1/events?limit=1000")).json()
    }
    assert (await admin.get("/api/v1/events?entity=auth&limit=5")).status_code == 200

    # grant 收窄：editor 仅在 product 类型上可写
    created_grant = await admin.post(
        "/api/v1/grants",
        {"userId": editor_id, "scope": "doc_type", "value": "product", "permission": "write"},
    )
    assert created_grant.status_code == 201, created_grant.text
    grants = await admin.get(f"/api/v1/grants?user_id={editor_id}")
    assert grants.status_code == 200 and len(grants.json()) == 1

    assert (
        await editor_client.post(
            "/api/v1/nodes",
            _node_body(DOC_RBAC_PRD, "1 ok", ordinal=0, content={"text": "product write"}),
        )
    ).status_code == 200
    denied = await editor_client.post(
        "/api/v1/nodes",
        _node_body(DOC_RBAC_STD, "1 denied", ordinal=0, content={"text": "standard write"}),
    )
    assert denied.status_code == 403, denied.text

    # 授予侧越权即拒（S5）：给 reader 授 write → 422
    assert (
        await admin.post(
            "/api/v1/grants",
            {"userId": reader_id, "scope": "doc", "value": DOC_RBAC_STD, "permission": "write"},
        )
    ).status_code == 422

    # 撤销收窄 grant → editor 回到**角色基线**（S5：grant 只收窄、不扩权；无收窄 grant 时角色说了算）
    grant_id = created_grant.json()["grantId"]
    assert (await admin.request("DELETE", f"/api/v1/grants/{grant_id}")).status_code == 204
    assert (
        await editor_client.post(
            "/api/v1/nodes",
            _node_body(DOC_RBAC_PRD, "1 after", ordinal=1, content={"text": "product write again"}),
        )
    ).status_code == 200
    assert (
        await editor_client.post(
            "/api/v1/nodes",
            _node_body(DOC_RBAC_STD, "1 baseline", ordinal=0, content={"text": "standard write"}),
        )
    ).status_code == 200

    # 用户状态与密钥管理（S8/S9）
    disabled = await admin.request("PATCH", f"/api/v1/users/{reader_id}", {"status": "disabled"})
    assert disabled.status_code == 200 and disabled.json()["status"] == "disabled"
    assert (await reader_client.get("/api/v1/docs")).status_code == 403  # 属主禁用 → 密钥失效

    # 自我保护（S9）：不可禁用自身
    me = await auth_users.get_user(admin_id, db=database)
    assert (
        await admin.request("PATCH", f"/api/v1/users/{me.user_id}", {"status": "disabled"})
    ).status_code == 409

    assert (await admin.request("DELETE", f"/api/v1/users/{editor_id}")).status_code == 204
    listed = await admin.get("/api/v1/users?status=disabled")
    assert listed.status_code == 200
    assert USER_READER in {item["username"] for item in listed.json()}


# ------------------------------------------------------------------ WebUI 会话路径


async def test_webui_session_login_and_identity(
    admin: Signer,
    admin_id: UUID,
    client: AsyncClient,
    keys: dict[str, Path],
    storage: Storage,
    database: Database,
) -> None:
    """REQ-M10-F02 + S14：挑战-响应换 Cookie，业务请求身份取自会话（`source='webui'`）。"""
    doc_id = DOC_SESSION
    await _seed_doc(storage, doc_id)

    challenge = (await client.post("/api/v1/auth/challenge")).json()
    key = signing.load_private_key(keys["admin"])
    signature = signing.sign_message(key, signing.login_payload(challenge["nonce"]))
    login = await client.post(
        "/api/v1/auth/login",
        json={
            "keyFingerprint": signing.fingerprint(keys["admin"].with_suffix(".pub").read_text()),
            "nonce": challenge["nonce"],
            "signature": signature,
        },
    )
    assert login.status_code == 200, login.text
    assert client.cookies.get(sessions.SESSION_COOKIE_NAME) is not None

    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 200 and me.json()["username"] == ADMIN_USERNAME

    assert (await client.get("/api/v1/docs")).status_code == 200
    written = await client.post(
        "/api/v1/nodes",
        json=_node_body(doc_id, "1 via webui", ordinal=0, content={"text": "webui write"}),
    )
    assert written.status_code == 200, written.text

    events = await admin.get(f"/api/v1/events?entity=node&entity_id={written.json()['nodeId']}")
    assert events.status_code == 200
    assert events.json()[0]["actor"] == str(admin_id)  # 会话身份 = 验签所得 user_id

    # logout 删行后，同一 Cookie 再用即 401（S15）
    assert (await client.post("/api/v1/auth/logout")).status_code == 204
    assert (await client.get("/api/v1/docs")).status_code == 401


# ------------------------------------------------------------------ 查询口径与边界


async def test_query_guards_and_boundaries(admin: Signer, storage: Storage) -> None:
    """边界：未知文档/节点 404、diff 参数非法 422、分页上限 422、渲染章节缺失 404。"""
    doc_id = DOC_EDGES
    await _seed_doc(storage, doc_id)

    assert (await admin.get(f"/api/v1/docs/{DOC_MISSING}")).status_code == 404
    assert (await admin.get(f"/api/v1/nodes/{UUID(int=7)}")).status_code == 404
    assert (await admin.get(f"/api/v1/docs/{doc_id}/sections")).json() == []
    assert (await admin.get(f"/api/v1/docs/{doc_id}/diff?from=3")).status_code == 422
    assert (await admin.get(f"/api/v1/docs/{doc_id}/diff?from=yesterday")).status_code == 422
    assert (await admin.get("/api/v1/events?limit=0")).status_code == 422
    assert (await admin.get("/api/v1/events?limit=100000")).status_code == 422
    assert (await admin.get("/api/v1/schemas/clause?extra=1")).status_code == 200
    assert (await admin.get(f"/api/v1/docs/{doc_id}/render?section=missing")).status_code == 404
    # atom_type=table 但 content 缺 fragment/meta → 422（M01 schema 校验）
    assert (
        await admin.post(
            "/api/v1/nodes",
            _node_body(doc_id, "1 x", ordinal=0, content={"text": "x"}, atom_type="table"),
        )
    ).status_code == 422
    # 不存在的文档上写节点 → 404
    assert (
        await admin.post(
            "/api/v1/nodes",
            _node_body(DOC_MISSING, "1 x", ordinal=0, content={"text": "x"}),
        )
    ).status_code == 404
    # 术语：定义节点不存在 → 404
    assert (
        await admin.post(
            "/api/v1/terms",
            {"term": f"GHOST-{_TOKEN}", "definitionNodeId": str(UUID(int=9)), "kind": "glossary"},
        )
    ).status_code == 404
