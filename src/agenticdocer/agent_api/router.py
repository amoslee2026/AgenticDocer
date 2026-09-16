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

from pydantic import Field

from agenticdocer.auth import write_context
from agenticdocer.model import (
    Doc,
    Model,
    Node,
    NodeIn,
    Ref,
    RefKind,
    RenderResult,
    UUID7,
    derive_text,
)
from agenticdocer.observability import get_logger
from agenticdocer.m09 import validate_write as validate_node
from agenticdocer.render import (
    SectionInfo,
    find_section,
    list_sections,
    render_document,
    render_section,
)
from agenticdocer.store import NotFoundError, Storage

from .deps import (
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
    "SectionDTO",
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



class SectionDTO(Model):
    """`GET /api/v1/docs/{id}/sections` 条目（§3 M07 TS 契约 `SectionDTO`）。

    M04 的领域类型 `SectionInfo` 把子树规模命名为 `node_count`，而 §3 M07 的前端契约要求
    `childCount`（`architecture_specification.md` §3 M07 TS 块）——故在 API 层按**契约口径**
    投影（A11），字段语义与 `SectionInfo.node_count` 一一对应。
    """

    node_id: UUID7
    parent_node_id: UUID7 | None = None
    anchor: str
    title: str
    level: int
    ordinal: int
    child_count: int

    @classmethod
    def of(cls, info: SectionInfo) -> "SectionDTO":
        return cls(
            node_id=info.node_id,
            parent_node_id=info.parent_node_id,
            anchor=info.anchor,
            title=info.title,
            level=info.level,
            ordinal=info.ordinal,
            child_count=info.node_count,
        )

# ── 写入门（REQ-M06-F01/F02）────────────────────────────────────────────




def validate_write(node: NodeIn, doc: Doc) -> NodeIn:
    """写入门（REQ-M06-F01/F02）：**判据全部由 M09A 承担**（P5 单点），本函数只做两件 HTTP 层的事。

    1. **补全 `content.text`**（A10 的写入职责，非校验职责）：缺失/空白时按 M01 `derive_text`
       生成——派生失败不在此报错，交由 M09A 的 `A10.content.text*` 判据统一报告（避免第二套文案）；
    2. 调 `m09.validate_write(node, doc_type=…)`，把 `Violation[]` 交给
       `ValidationRejected` → `422 + violations[]`（`fix_hint` 原样透传，agent 据此自修复重试）。

    判据集合（M09A，含本模块此前缺失者）：atom 注册、JSON Schema、`content.text` 存在性/空白/
    派生漂移、锚 `<doc_id>#` 前缀（M01 锚构造口径）、自指父、表格 `format ↔ fragment`、
    外部叶引用带 node、`doc_type` 组合规则。

    :raises ValidationRejected: 任一判据失败（422）。
    """
    content = dict(node.content)
    if not str(content.get("text") or "").strip():
        try:
            content["text"] = derive_text(node.atom_type, content)
        except ValueError:
            pass  # 派生失败：留空交 M09A 报 `A10.content.text*`（rule_id 单点）
    candidate = node.model_copy(update={"content": content})
    violations = validate_node(candidate, doc_type=doc.doc_type)
    if violations:
        raise ValidationRejected(violations, entity="node", entity_id=node.node_id)
    return candidate


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
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
    expected_version: int = Query(description="乐观锁版本（`nodes.version`；不匹配 → 409）"),
) -> Response:
    """软删节点（A2）：写 delete 事件、同事务把该节点 open 批注置 `orphaned`。"""
    node = await storage.get_node(node_id)
    await authorize_doc(context, "write", node.doc_id, storage=storage, db=db)
    with log.timer("query", table="nodes", doc_id=node.doc_id):
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


@router.get("/docs/{doc_id}/sections", response_model=list[SectionDTO])
async def list_doc_sections(
    doc_id: str,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> list[SectionDTO]:
    """章节清单（level ≤ 2 的节点 + 子树节点数；M08 分章节加载入口，B10）。"""
    await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    with log.timer("query", table="nodes", doc_id=doc_id):
        nodes = await storage.get_doc_nodes(doc_id)
    return [SectionDTO.of(info) for info in list_sections(nodes)]


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
async def get_asset(asset_id: str, context: ReadAuth, storage: StorageDep) -> FileResponse:
    """资产字节流（A6：sha256 内容寻址）。

    资产表无文档关联列（§4 DDL），故判定为**凭据 + `read` 角色**级；`Cache-Control`
    取 `immutable`（内容寻址 → 同 id 内容恒等）。
    """
    record = await storage.get_asset(asset_id)
    path = await storage.get_asset_path(asset_id)
    log.info("asset served", op="get_asset", asset_id=asset_id, bytes=record.bytes)
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
