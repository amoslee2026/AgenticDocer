"""M06 Agent 接口（§3 M06；REQ-M06-F01/F02）——面向 coding agent 的结构化读写 HTTP 面。

| 方法/路径 | 语义 |
|---|---|
| `GET /api/v1/nodes/{node_id}?doc_id=` | 节点点查（`doc_id` 可选：传入裁到单分区，缺失则全分区扫，ADR-009 V16） |
| `POST /api/v1/nodes` | 结构化写入（`NodeIn` + `expectedVersion` 乐观锁；写前经校验门） |
| `DELETE /api/v1/nodes/{node_id}?expected_version=` | **软删**（A2；同事务孤立化批注 + 写 delete 事件） |
| `POST` / `DELETE /api/v1/refs` | 引用边增删（每次变更写 ref 事件，REQ-M02-F02） |
| `GET /api/v1/docs/{doc_id}/nodes` | 文档节点树（默认 `status='active'`） |
| `GET /api/v1/docs/{doc_id}/sections` | 章节清单（B10 分章节渲染入口） |
| `GET /api/v1/docs/{doc_id}/render?section=` | 章节渲染（省略 `section` → 整档，B10） |
| `POST /api/v1/docs/{doc_id}/render` | 触发整档渲染（M04） |
| `GET /api/v1/assets/{asset_id}` | 资产字节流（A6；sha256 寻址，可强缓存） |
| ~~`GET /nodes/{id}/traverse`~~ / ~~`GET /search`~~ | **刻意缺席**（B5/ADR-008：图遍历与全文检索属 LightRAG 业务，M05 降级为内部实现） |

**鉴权（S4/S5/S14）**：本模块端点全部需凭据（无凭据 401）；涉及文档的端点另按
「角色硬上限 + 文档集级 grant 收窄」判定（`deps.authorize_doc`）。身份一律取自验签结果
（`X-Actor` 已删除）；`source` 由凭据类型判定（签名 → `agent`，Cookie → `webui`）。

**写入门（REQ-M06-F01/F02）**：`validate_write` 在写入前做「atom_type 已注册 → 该 doc_type
允许该原子 → `content` 合 JSON Schema → `content.text` 非空（A10 派生）」四步判定，失败抛
`ValidationRejected`（422 + `violations[]`，每条含 `fix_hint`），agent 据以修正后重试。
判定口径全部取自 M01（`ATOM_SCHEMAS` / `is_atom_allowed` / `derive_text`，P5 单一口径）——
M09A 交付后同一判定由 `m09.validate_write` 暴露，届时本函数退化为其调用点。
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Query, Response
from fastapi.responses import FileResponse
from jsonschema import validators
from pydantic import Field

from agenticdocer.auth import write_context
from agenticdocer.model import (
    ATOM_SCHEMAS,
    Doc,
    Model,
    Node,
    NodeIn,
    Ref,
    RefKind,
    RenderResult,
    Violation,
    derive_text,
    get_atom_schema,
    is_atom_allowed,
)
from agenticdocer.observability import get_logger
from agenticdocer.render import (
    SectionInfo,
    find_section,
    list_sections,
    render_document,
    render_section,
)
from agenticdocer.store import NotFoundError, Storage

from .deps import (
    AuthDep,
    DatabaseDep,
    ReadAuth,
    StorageDep,
    ValidationRejected,
    WriteAuth,
    authorize_doc,
)

__all__ = [
    "NodeUpsert",
    "RefWrite",
    "RenderOutput",
    "router",
    "validate_write",
]

log = get_logger("m06.api")

router = APIRouter(prefix="/api/v1", tags=["agent"])

_MISSING_FIELD_RE = re.compile(r"'([^']+)' is a required property")


# ── 请求/响应 DTO（camelCase 序列化由 `Model` 基类保证，§6 横切 A11）──────


class NodeUpsert(NodeIn):
    """`POST /api/v1/nodes` 请求体：§3.0 `NodeIn` + `expectedVersion`（乐观锁）。

    `expectedVersion` 省略 → 新建或无条件覆盖；给定 → 行必须存在且版本相等（否则 409）。
    """

    expected_version: int | None = None


class RefWrite(Model):
    """`POST`/`DELETE /api/v1/refs` 请求体（§3 M06：`src, dst_doc, dst_node, kind`）。"""

    src: UUID
    dst_doc: str = Field(min_length=1)
    dst_node: UUID | None = None
    kind: RefKind


class RenderOutput(RenderResult):
    """渲染响应：M04 `RenderResult` + 命中章节锚与渲染文本（M08 前端按章节取文本，B10）。"""

    section: str | None = None
    markdown: str


# ── 写入门（REQ-M06-F01/F02）────────────────────────────────────────────


def _schema_violations(atom_type: str, content: dict[str, Any]) -> list[Violation]:
    """`content` 对 `atom_type` 的 JSON Schema 校验（口径 = M01 注册表）。"""
    schema = get_atom_schema(atom_type)
    validator = validators.validator_for(schema)(schema)
    return [
        Violation(
            rule_id=f"m01.schema.{error.validator}",
            path="content/" + "/".join(str(part) for part in error.absolute_path),
            message=error.message,
            fix_hint=_fix_hint(error),
        )
        for error in validator.iter_errors(content)
    ]


def _fix_hint(error: Any) -> str | None:
    """违规 → 可操作修复建议（REQ-M06-F02：agent 据此自修复重试）。"""
    if error.validator == "required":
        match = _MISSING_FIELD_RE.search(error.message)
        return f"补齐必填字段 content.{match.group(1)}" if match else "补齐 schema 要求的必填字段"
    if error.validator == "type":
        return f"字段类型应为 {error.validator_value}"
    if error.validator == "additionalProperties":
        return "移除 schema 未声明的字段"
    if error.validator == "enum":
        return f"取值应为 {error.validator_value} 之一"
    return None


def validate_write(node: NodeIn, doc: Doc) -> NodeIn:
    """写入门：校验并补全 `content.text`（A10），返回可写入的 `NodeIn`。

    :raises ValidationRejected: 任一判定失败（422；`violations[]` 含 `fix_hint`）。
    """
    if node.atom_type not in ATOM_SCHEMAS:
        raise ValidationRejected(
            [
                Violation(
                    rule_id="m01.atom_type.unregistered",
                    path="atomType",
                    message=f"未注册的 atom_type：{node.atom_type!r}（无 schema 的类型不得写入）",
                    fix_hint=f"改用已注册原子：{', '.join(sorted(ATOM_SCHEMAS))}",
                )
            ],
            entity="node",
            entity_id=node.node_id,
        )
    if not is_atom_allowed(doc.doc_type, node.atom_type):
        raise ValidationRejected(
            [
                Violation(
                    rule_id="m01.doc_type.atom_not_allowed",
                    path="atomType",
                    message=f"doc_type {doc.doc_type!r} 不允许原子 {node.atom_type!r}",
                    fix_hint=f"改用 {doc.doc_type!r} 允许的原子（M01 doc_type 组合规则）",
                )
            ],
            entity="node",
            entity_id=node.node_id,
        )
    content = dict(node.content)
    violations = _schema_violations(node.atom_type, content)
    if violations:
        raise ValidationRejected(violations, entity="node", entity_id=node.node_id)
    if not str(content.get("text") or "").strip():
        try:
            content["text"] = derive_text(node.atom_type, content)
        except ValueError as exc:
            raise ValidationRejected(
                [
                    Violation(
                        rule_id="m01.content.text.empty",
                        path="content/text",
                        message=str(exc),
                        fix_hint="提供 content.text 或 content.fragment（A10：一切节点 content.text 非空）",
                    )
                ],
                entity="node",
                entity_id=node.node_id,
            ) from exc
    return node.model_copy(update={"content": content})


# ── 端点 ────────────────────────────────────────────────────────────────


@router.get("/nodes/{node_id}", response_model=Node)
async def get_node(
    node_id: UUID,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
    doc_id: str | None = Query(
        default=None, description="文档 id：给定则点查裁到单分区（ADR-009 V16），省略则全分区扫"
    ),
) -> Node:
    """节点点查（含 `version`/`status`）；默认过滤软删节点（A2）。"""
    with log.timer("query", table="nodes", doc_id=doc_id):
        node = await storage.get_node(node_id, doc_id=doc_id)
    await authorize_doc(context, "read", node.doc_id, storage=storage, db=db)
    return node


@router.post("/nodes", response_model=Node)
async def post_node(
    payload: NodeUpsert,
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Node:
    """结构化写入（新建或按 `expectedVersion` 更新）；`nodeId` 缺省则新建。"""
    incoming = NodeIn(**payload.model_dump(exclude={"expected_version"}))
    doc = await authorize_doc(context, "write", incoming.doc_id, storage=storage, db=db)
    node = validate_write(incoming, doc)
    with log.timer("query", table="nodes", doc_id=node.doc_id):
        written = await storage.upsert_node(node, payload.expected_version, write_context(context))
    log.info(
        "node written",
        op="upsert_node",
        node_id=str(written.node_id),
        doc_id=written.doc_id,
        version=written.version,
    )
    return written

@router.delete("/nodes/{node_id}", status_code=204)
async def delete_node(
    node_id: UUID,
    expected_version: int = Query(description="乐观锁版本（`nodes.version`；不匹配 → 409）"),
    *,
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Response:
        await storage.delete_node(node_id, expected_version, write_context(context))
    log.info("node softly deleted", op="delete_node", node_id=str(node_id), doc_id=node.doc_id)
    return Response(status_code=204)


@router.post("/refs", response_model=Ref, status_code=201)
async def post_ref(
    payload: RefWrite,
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Ref:
    """新增引用边（重复边 → 409；源节点不存在/已软删 → 404）。"""
    source = await storage.get_node(payload.src)
    await authorize_doc(context, "write", source.doc_id, storage=storage, db=db)
    await storage.add_ref(
        payload.src, payload.dst_doc, payload.dst_node, payload.kind, write_context(context)
    )
    edges = await storage.list_refs(payload.src)
    created = _find_ref(edges, payload)
    if created is None:  # 写入成功后回读不到 → 状态异常，向上暴露而非静默
        raise NotFoundError(
            f"ref {payload.kind} {payload.src} → {payload.dst_doc} 写入后回读失败",
            entity="ref",
            entity_id=payload.src,
        )
    return created


@router.delete("/refs", status_code=204)
async def delete_ref(
    payload: RefWrite,
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Response:
    """删除引用边（边不存在 → 404）。"""
    source = await storage.get_node(payload.src)
    await authorize_doc(context, "write", source.doc_id, storage=storage, db=db)
    await storage.remove_ref(
        payload.src, payload.dst_doc, payload.dst_node, payload.kind, write_context(context)
    )
    return Response(status_code=204)


def _find_ref(edges: list[Ref], payload: RefWrite) -> Ref | None:
    """从源节点出边里定位刚写入的那条（`add_ref` 无返回值）。"""
    for edge in edges:
        if (
            edge.dst_doc_id == payload.dst_doc
            and edge.dst_node_id == payload.dst_node
            and edge.kind == payload.kind
        ):
            return edge
    return None


@router.get("/docs/{doc_id}/nodes", response_model=list[Node])
async def list_doc_nodes(
    doc_id: str,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
    include_deleted: bool = Query(default=False, description="是否包含软删节点（A2）"),
) -> list[Node]:
    """文档节点树（`ordinal` 序；默认仅 `active`）。"""
    await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    with log.timer("query", table="nodes", doc_id=doc_id):
        return await storage.get_doc_nodes(doc_id, include_deleted=include_deleted)


@router.get("/docs/{doc_id}/sections", response_model=list[SectionInfo])
async def list_doc_sections(
    doc_id: str,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> list[SectionInfo]:
    """章节清单（level ≤ 2 的节点 + 子树节点数；M08 分章节加载入口，B10）。"""
    await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    with log.timer("query", table="nodes", doc_id=doc_id):
        nodes = await storage.get_doc_nodes(doc_id)
    return list_sections(nodes)


@router.get("/docs/{doc_id}/render", response_model=RenderOutput)
async def render_doc_section(
    doc_id: str,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
    section: str | None = Query(
        default=None, description="章节锚（M04 `find_section`）或章节 node_id；省略 → 整档渲染"
    ),
) -> RenderOutput:
    """渲染整档或单章节（M04；HTML 片段零改写直通，P4）。"""
    await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    if section is None:
        return await _render(doc_id, None, storage)
    node = await _resolve_section(section, doc_id, storage)
    return await _render(doc_id, node, storage)


@router.post("/docs/{doc_id}/render", response_model=RenderOutput)
async def render_doc(
    doc_id: str,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> RenderOutput:
    """触发整档渲染（产物落 `RENDER_OUT_DIR`，§5）。"""
    await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    return await _render(doc_id, None, storage)


@router.get("/assets/{asset_id}")
async def get_asset(asset_id: str, context: AuthDep, storage: StorageDep) -> FileResponse:
    """资产字节流（A6：sha256 内容寻址）。

    资产表无文档关联列（§4 DDL），故判定为**凭据 + `read` 角色**级；`Cache-Control`
    取 `immutable`（内容寻址 → 同 id 内容恒等）。
    """
    record = await storage.get_asset(asset_id)
    path = await storage.get_asset_path(asset_id)
async def get_asset(asset_id: str, context: ReadAuth, storage: StorageDep) -> FileResponse:
    return FileResponse(
        path,
        media_type=record.mime,
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


# ── 内部：渲染与章节定位 ────────────────────────────────────────────────


async def _render(doc_id: str, section: Any, storage: Storage) -> RenderOutput:
    """调用 M04 渲染入口并回读产物文本（M08 直接消费文本，无需二次取件）。"""
    if section is None:
        result = await render_document(doc_id, storage=storage)
        anchor = None
    else:
        result = await render_section(doc_id, section.node_id, storage=storage)
        anchor = section.anchor
    markdown = await asyncio.to_thread(Path(result.out_path).read_text, "utf-8")
    return RenderOutput(
        doc_id=result.doc_id,
        out_path=result.out_path,
        assets_exported=result.assets_exported,
        section=anchor,
        markdown=markdown,
    )


async def _resolve_section(section: str, doc_id: str, storage: Storage) -> Node:
    """`?section=` → 章节节点：先按锚（M04 `find_section`，P5 单一口径），再按 node_id。"""
    with log.timer("query", table="nodes", doc_id=doc_id):
        nodes = await storage.get_doc_nodes(doc_id)
    found = find_section(nodes, section)
    if found is None:
        try:
            wanted: UUID | None = UUID(section)
        except ValueError:
            wanted = None
        found = next((node for node in nodes if node.node_id == wanted), None)
    if found is None:
        raise NotFoundError(
            f"section {section!r} not found in doc {doc_id}", entity="node", entity_id=section
        )
    return found
