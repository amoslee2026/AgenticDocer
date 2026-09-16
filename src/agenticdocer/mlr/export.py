"""M-LR LightRAG 导出边界：导出包生成（REQ-MLR-F01；架构规范 §3 M-LR；ADR-008）。

产出（`out_dir/`，三份文件）：

* ``nodes.jsonl``——每行 ``{node_id, doc_id, anchor, text}``（§3 M-LR 规定的 jsonl 形状）。
  ``text`` 取 **M04 渲染口径**（:func:`~agenticdocer.render.node_block_text`，唯一节点渲染
  口径）：有 ``content.fragment`` 时逐字节直通（P4），无 fragment 时按 ``atom_type`` 合成。
* ``graph.jsonl``——**图结构上下文**（ADR-008：M05 降级后的主要用途）。两个来源
  （``origin`` 区分），字段与方向语义见下。
* ``manifest.json``——计数与口径元信息（``ExportResult`` 字段固定为
  ``{out_path, docs, nodes}``，故计数明细落此）。

**``graph.jsonl`` 字段语义**（勿按 ``src``/``dst`` 读——那是有向边口径，本文件是「可达关系」
口径）：

```json
{"node_id": …, "doc_id": …, "related_node_id": …, "related_doc_id": …,
 "hops": 1, "kinds": ["composes_from"], "direction": "out", "origin": "hierarchy"}
```

* ``node_id`` → ``related_node_id``：自起点出发、经 ``kinds``（最短路径上每跳一个 kind 的
  序列）在 ``hops`` 跳内可达；
* ``direction`` 仅在 ``hops == 1`` 时非 ``null``（``null`` = 多跳路径，不是单条边）：

  - ``"out"``——存在有向边 ``node_id → related_node_id``；
  - ``"in"``——存在有向边 ``related_node_id → node_id``（``traces_to`` 上游链即此：命中节点
    追溯到起点）；
  - ``"both"``——``see_also``（双向语义）。

  方向表取自 M05 ``KIND_RULES``（``down`` → out、``up`` → in、``both`` → both），本模块不复制
  这份知识。
* ``origin='hierarchy'``：节点树父子（``nodes.parent_node_id``）——``node_id`` 为父（整体）、
  ``related_node_id`` 为子（部分）、``kinds=['composes_from']``、``hops=1``、``direction='out'``。
  **该关系可能只有节点树而无对应 refs 行**（``parent_node_id`` 是权威父子口径）。
* ``origin='traverse'``：M05 :func:`~agenticdocer.retrieve.traverse` 的多跳可达集合
  （``traces_to`` 上游链、``see_also``、refs 形态的 ``composes_from``）。逐 kind 的跳数上限
  由 M05 ``KIND_RULES`` 截断（``hops=2`` 仅把 ``traces_to`` 扩到 2 跳）。

同一 ``(node_id, related_node_id, hops, kinds)`` 只保留首次（节点树先入，故 refs 形态的
``composes_from`` 不会与节点树父子重复出现）。

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
from agenticdocer.retrieve import KIND_RULES, traverse
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
"""导出包格式版本（字段增删时递增；lightRAG 侧消费方据此判兼容）。"""

DEFAULT_GRAPH_HOPS: Final = 2
"""图结构上下文的跳数上限——透传 M05 ``traverse(hops=...)``，逐 kind 截断在 M05 内完成。

取 2 是为拿到 ``traces_to`` 上游链（A19：``hops=2`` 仅扩 ``traces_to``；``composes_from``
与 ``see_also`` 仍各按上限 1 跳截断）。
"""

#: M05 的 `KIND_RULES` 方向 → `graph.jsonl` 的 `direction`（`down` = 有向边 src→dst）。
_DIRECTIONS: Final[dict[str, str]] = {"down": "out", "up": "in", "both": "both"}


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

    :param doc_ids: 参与导出的文档（重复项按首次出现去重）。任取不到 →
      :class:`NotFoundError`（不静默跳过——静默会让对端收到不完整语料却无从察觉）。
    :param out_dir: 包目录（不存在则创建；同名文件**整体覆盖**，不留上一版残留行）。
    :param storage: 注入 `Storage`（缺省进程级单例，便于 M11 CLI 直接调用）。
    :param hops: 图结构上下文跳数（≥1）。只影响 refs 图遍历深度，不影响 ``nodes.jsonl``。
    """
    if hops < 1:
        raise ValidationError(f"hops must be >= 1, got {hops}", entity="node")
    store = storage if storage is not None else Storage()
    # 去重保序：重复项会让 `docs` 计数与包内容不符
    ordered = list(dict.fromkeys(doc_ids))
    # 文档先取（404 在计时之外：失败不是一次导出，不该进导出指标）
    docs = [await store.get_doc(doc_id) for doc_id in ordered]
    nodes = await store.list_nodes_for_docs(ordered)
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
    """图结构上下文：节点树父子 + M05 多跳可达集合，按关系键排序去重。"""
    relations: dict[tuple[Any, ...], dict[str, Any]] = {}
    for node in nodes:
        parent = node.parent_node_id
        if parent is None:
            continue
        _remember(
            relations,
            node_id=parent,
            doc_id=node.doc_id,
            related_node_id=node.node_id,
            related_doc_id=node.doc_id,
            hops=1,
            kinds=("composes_from",),
            direction="out",
            origin="hierarchy",
        )
    for node in nodes:
        hits = await traverse(node.node_id, hops, doc_id=node.doc_id, storage=store)
        for hit in hits:
            kinds = tuple(hit.via)
            _remember(
                relations,
                node_id=node.node_id,
                doc_id=node.doc_id,
                related_node_id=hit.node_id,
                related_doc_id=hit.doc_id,
                hops=hit.hops,
                kinds=kinds,
                direction=_direction_of(hops=hit.hops, kinds=kinds),
                origin="traverse",
            )
    return sorted(relations.values(), key=_relation_sort_key)


def _direction_of(*, hops: int, kinds: tuple[str, ...]) -> str | None:
    """单跳关系的边方向（多跳路径 → `None`）；方向表取自 M05 ``KIND_RULES``。"""
    if hops != 1 or len(kinds) != 1:
        return None
    rule = KIND_RULES.get(kinds[0])  # type: ignore[arg-type]
    return _DIRECTIONS[rule[0]] if rule is not None else None


def _remember(
    relations: dict[tuple[Any, ...], dict[str, Any]],
    *,
    node_id: UUID,
    doc_id: str,
    related_node_id: UUID,
    related_doc_id: str,
    hops: int,
    kinds: tuple[str, ...],
    direction: str | None,
    origin: str,
) -> None:
    """登记一条关系（同一 ``(node_id, related_node_id, hops, kinds)`` 只留首次）。"""
    key = (str(node_id), str(related_node_id), hops, kinds)
    relations.setdefault(
        key,
        {
            "node_id": str(node_id),
            "doc_id": doc_id,
            "related_node_id": str(related_node_id),
            "related_doc_id": related_doc_id,
            "hops": hops,
            "kinds": list(kinds),
            "direction": direction,
            "origin": origin,
        },
    )


def _relation_sort_key(relation: dict[str, Any]) -> tuple[Any, ...]:
    return (
        relation["doc_id"],
        relation["node_id"],
        relation["hops"],
        relation["related_doc_id"],
        relation["related_node_id"],
        relation["kinds"],
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
    """计数与口径元信息（供对端判包完整性；不入 `ExportResult`）。"""
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
    _write_text(
        target / EXPORT_MANIFEST_FILE, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
