"""M-LR LightRAG 导出边界：导出包生成（REQ-MLR-F01；架构规范 §3 M-LR；ADR-008）。

产出（`out_dir/`，三份文件）：

* ``nodes.jsonl``——每行 ``{node_id, doc_id, anchor, text}``（§3 M-LR 规定的 jsonl 形状）。
  ``text`` 取 **M04 渲染口径**（:func:`~agenticdocer.render.node_block_text`，唯一节点渲染
  口径）：有 ``content.fragment`` 时逐字节直通（P4），无 fragment 时按 ``atom_type`` 合成。
* ``graph.jsonl``——**图结构上下文**（ADR-008：M05 降级后的主要用途）。每行一条关系
  ``{src_node_id, src_doc_id, dst_node_id, dst_doc_id, hops, via, origin}``，两个来源：

  1. ``origin='hierarchy'``：节点树父子（``nodes.parent_node_id``）→ ``composes_from``、1 跳；
  2. ``origin='traverse'``：M05 :func:`~agenticdocer.retrieve.traverse` 的多跳可达集合
     （``traces_to`` 上游链、``see_also``、refs 形态的 ``composes_from``），
     ``via`` 为最短路径上的 kind 序列、``hops`` 为边数。
     逐 kind 的跳数上限由 M05 ``KIND_RULES`` 截断（``hops=2`` 仅把 ``traces_to`` 扩到 2 跳）。

* ``manifest.json``——计数与口径元信息（``ExportResult`` 字段固定为
  ``{out_path, docs, nodes}``，故计数明细落此）。

**确定性**：无 LLM、无网络、不依赖 lightRAG 在线（C7/P6/REQ-MLR-F01）。同一库状态下
``nodes.jsonl`` / ``graph.jsonl`` 逐字节一致（记录按 ``doc_id → ordinal`` / 关系键排序）；
``manifest.json`` 例外（含生成时间）。

**C7（摄入暂缓）**：本模块只生成包，不导入 lightRAG、不调用其 API、不导出资产字节。
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final
from uuid import UUID

from agenticdocer.model import Doc, ExportResult, Node
from agenticdocer.observability import get_logger
from agenticdocer.render import node_block_text
from agenticdocer.retrieve import traverse
from agenticdocer.store import Storage, ValidationError, now

__all__ = [
    "DEFAULT_GRAPH_HOPS",
    "EXPORT_GRAPH_FILE",
    "EXPORT_MANIFEST_FILE",
    "EXPORT_NODES_FILE",
    "FORMAT_VERSION",
    "export_package",
    "node_record",
]

log = get_logger("mlr.export")

EXPORT_NODES_FILE: Final = "nodes.jsonl"
EXPORT_GRAPH_FILE: Final = "graph.jsonl"
EXPORT_MANIFEST_FILE: Final = "manifest.json"

FORMAT_VERSION: Final = 1
"""导出包格式版本（字段增删时递增；LightRAG 侧消费方据此判兼容）。"""

DEFAULT_GRAPH_HOPS: Final = 2
"""图结构上下文的跳数上限——透传 M05 ``traverse(hops=...)``，逐 kind 截断在 M05 内完成。

取 2 是为拿到 ``traces_to`` 上游链（A19：``hops=2`` 仅扩 ``traces_to``；``composes_from``
与 ``see_also`` 仍各按上限 1 跳截断）。
"""


def node_record(node: Node) -> dict[str, Any]:
    """``nodes.jsonl`` 单行：``{node_id, doc_id, anchor, text}``（§3 M-LR）。

    ``text`` 为 M04 渲染文本；**不做**图片 ``src`` 重写——导出包不携带资产字节（C7）。
    """
    return {
        "node_id": str(node.node_id),
        "doc_id": node.doc_id,
        "anchor": node.anchor,
        "text": node_block_text(node),
    }


async def export_package(
    doc_ids: Sequence[str],
    out_dir: str | Path,
    *,
    storage: Storage | None = None,
    hops: int = DEFAULT_GRAPH_HOPS,
) -> ExportResult:
    """生成导出包（§3 M-LR / REQ-MLR-F01）。

    :param doc_ids: 参与导出的文档。任取不到 → :class:`NotFoundError`（不静默跳过——
      静默会让对端收到不完整语料却无从察觉）。
    :param out_dir: 包目录（不存在则创建；同名文件**整体覆盖**，不留上一版残留行）。
    :param storage: 注入 `Storage`（缺省进程级单例，便于 M11 CLI 直接调用）。
    :param hops: 图结构上下文跳数（≥1）。仅 refs 图遍历深度，不影响 ``nodes.jsonl``。
    """
    if hops < 1:
        raise ValidationError(f"hops must be >= 1, got {hops}", entity="node")
    store = storage if storage is not None else Storage()
    target = Path(out_dir)
    # 先取文档（404 在计时之外：失败不是一次导出，不该进导出指标）
    docs = [await store.get_doc(doc_id) for doc_id in doc_ids]
    nodes = await store.list_nodes_for_docs(list(doc_ids))
    records = [node_record(node) for node in nodes]
    with log.timer("export_package", doc_count=len(docs), node_count=len(records), graph_hops=hops):
        relations = await _graph_relations(nodes, store, hops)
        target.mkdir(parents=True, exist_ok=True)
        _write_jsonl(target / EXPORT_NODES_FILE, records)
        _write_jsonl(target / EXPORT_GRAPH_FILE, relations)
        _write_manifest(target, docs, records, relations, hops)
    log.info(
        "export package written",
        out_dir=str(target),
        docs=len(docs),
        nodes=len(records),
        relations=len(relations),
    )
    return ExportResult(out_path=str(target), docs=len(docs), nodes=len(records))


async def _graph_relations(nodes: Sequence[Node], store: Storage, hops: int) -> list[dict[str, Any]]:
    """图结构上下文：节点树父子 + M05 多跳可达集合，按关系键排序去重。

    父子关系先入（`origin='hierarchy'`）：同一关系若也被 ``traverse`` 命中（refs 形态的
    ``composes_from``），保留先入的那条，避免同一条边在包内出现两次。
    """
    relations: dict[tuple[Any, ...], dict[str, Any]] = {}
    for node in nodes:
        parent = node.parent_node_id
        if parent is None:
            continue
        _remember(
            relations,
            src_doc_id=node.doc_id,
            src_node_id=parent,
            dst_doc_id=node.doc_id,
            dst_node_id=node.node_id,
            hops=1,
            via=("composes_from",),
            origin="hierarchy",
        )
    for node in nodes:
        hits = await traverse(node.node_id, hops, doc_id=node.doc_id, storage=store)
        for hit in hits:
            _remember(
                relations,
                src_doc_id=node.doc_id,
                src_node_id=node.node_id,
                dst_doc_id=hit.doc_id,
                dst_node_id=hit.node_id,
                hops=hit.hops,
                via=tuple(hit.via),
                origin="traverse",
            )
    return sorted(relations.values(), key=_relation_sort_key)


def _remember(
    relations: dict[tuple[Any, ...], dict[str, Any]],
    *,
    src_doc_id: str,
    src_node_id: UUID,
    dst_doc_id: str,
    dst_node_id: UUID,
    hops: int,
    via: tuple[str, ...],
    origin: str,
) -> None:
    """登记一条关系（同一 ``(src, dst, hops, via)`` 只留首次）。"""
    key = (str(src_node_id), str(dst_node_id), hops, via)
    relations.setdefault(
        key,
        {
            "src_node_id": str(src_node_id),
            "src_doc_id": src_doc_id,
            "dst_node_id": str(dst_node_id),
            "dst_doc_id": dst_doc_id,
            "hops": hops,
            "via": list(via),
            "origin": origin,
        },
    )


def _relation_sort_key(relation: dict[str, Any]) -> tuple[Any, ...]:
    return (
        relation["src_doc_id"],
        relation["src_node_id"],
        relation["hops"],
        relation["dst_doc_id"],
        relation["dst_node_id"],
        relation["via"],
    )


def _write_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    """写 JSONL（UTF-8、`\\n`、紧凑分隔符；空集合 → 空文件）。"""
    body = "".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records
    )
    _write_text(path, body)


def _write_manifest(
    target: Path,
    docs: Sequence[Doc],
    records: Sequence[dict[str, Any]],
    relations: Sequence[dict[str, Any]],
    hops: int,
) -> None:
    """计数与口径元信息（供对端判包完整性，不入 `ExportResult`）。"""
    manifest = {
        "format_version": FORMAT_VERSION,
        "generated_at": now().isoformat(),
        "graph_hops": hops,
        "doc_ids": [doc.doc_id for doc in docs],
        "counts": {
            "docs": len(docs),
            "nodes": len(records),
            "relations": len(relations),
            "relations_hierarchy": sum(1 for rel in relations if rel["origin"] == "hierarchy"),
            "relations_traverse": sum(1 for rel in relations if rel["origin"] == "traverse"),
            "text_empty": sum(1 for record in records if not record["text"]),
        },
        "files": {"nodes": EXPORT_NODES_FILE, "relations": EXPORT_GRAPH_FILE},
    }
    _write_text(target / EXPORT_MANIFEST_FILE, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
