import { useState } from "react";
import type { DocDTO, NodeDTO, SchemaDTO } from "../api/types";
import { ApiError } from "../api/client";
import { nodeApi } from "../api/endpoints";
import { roleAtLeast } from "../api/roles";
import type { SessionDTO } from "../api/types";
import { TableGridEditor } from "./TableGridEditor";
import { NodeForm } from "./NodeForm";

interface Props {
  doc: DocDTO;
  schemas: SchemaDTO[];
  nodes: NodeDTO[];
  session: SessionDTO;
  node: NodeDTO;
  onNodeChanged: (node: NodeDTO) => void;
  onDocRefresh: () => void;
  onDeleted: () => void;
}

/** 右栏「节点详情」：元信息、content 查看、schema 表单编辑（editor+）、表格编辑（B6）。 */
export function NodeDetailPanel({ doc, schemas, nodes, session, node, onNodeChanged, onDocRefresh, onDeleted }: Props) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const canWrite = roleAtLeast(session.role, "editor");
  const tableEditable =
    doc.meta.editable_tables === true &&
    canWrite &&
    node.format !== "html" &&
    node.status === "active";

  async function softDelete() {
    setBusy(true);
    setError(null);
    try {
      await nodeApi.delete(node.nodeId, node.version);
      setNotice("节点已软删（open 批注同步置 orphaned）。");
      onDeleted();
    } catch (exc) {
      setError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  if (editing) {
    return (
      <NodeForm
        schemas={schemas}
        docId={doc.docId}
        node={node}
        parentCandidates={nodes
          .filter((candidate) => candidate.status === "active")
          .map((candidate) => ({ nodeId: candidate.nodeId, anchor: candidate.anchor }))}
        defaultParentId={node.parentNodeId}
        nextOrdinal={node.ordinal}
        onSaved={(saved) => {
          setEditing(false);
          onNodeChanged(saved);
          onDocRefresh();
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  const contentText = JSON.stringify(node.content, null, 2);

  return (
    <div>
      {error ? <div className="notice error">{error}</div> : null}
      {notice ? <div className="notice ok">{notice}</div> : null}

      <dl className="kv">
        <dt>nodeId</dt>
        <dd>{node.nodeId}</dd>
        <dt>anchor</dt>
        <dd>{node.anchor}</dd>
        <dt>atomType</dt>
        <dd>{node.atomType}</dd>
        <dt>format</dt>
        <dd>{node.format}</dd>
        <dt>ordinal / level</dt>
        <dd>
          {node.ordinal} / {node.level ?? "—"}
        </dd>
        <dt>status</dt>
        <dd>
          <span className={`badge ${node.status}`}>{node.status}</span>
        </dd>
        <dt>version</dt>
        <dd>v{node.version}</dd>
      </dl>

      {node.atomType === "table" || node.atomType === "table.register_field" ? (
        tableEditable ? (
          <div style={{ marginTop: "var(--sp-3)" }}>
            <div className="section-label">可编辑表格（editable_tables 开启 · editor+）</div>
            <TableGridEditor
              node={node}
              onSaved={(saved) => {
                onNodeChanged(saved);
                setNotice("表格已回写，节点 content 更新。");
              }}
            />
          </div>
        ) : (
          <div className="notice" style={{ marginTop: "var(--sp-3)" }}>
            表格只读——
            {doc.meta.editable_tables !== true
              ? "文档未开启 editable_tables"
              : !canWrite
                ? "角色不足（需 editor+）"
                : node.format === "html"
                  ? "HTML 片段恒直通（P4），不可转可编辑控件"
                  : "节点非 active 状态"}
            。
          </div>
        )
      ) : null}

      <div className="section-label">content</div>
      <pre
        style={{
          fontFamily: "var(--mono)",
          fontSize: "var(--fs-0)",
          background: "var(--surface-2)",
          border: "1px solid var(--line)",
          borderRadius: "var(--radius-sm)",
          padding: "var(--sp-2) var(--sp-3)",
          overflowX: "auto",
          margin: 0,
        }}
      >
        {contentText}
      </pre>

      {node.status === "active" ? (
        <div className="row" style={{ marginTop: "var(--sp-3)" }}>
          {canWrite ? (
            <button onClick={() => setEditing(true)}>schema 表单编辑</button>
          ) : (
            <span className="meta" style={{ fontSize: "var(--fs-1)", color: "var(--ink-3)" }}>
              editor 角色可编辑
            </span>
          )}
          {canWrite ? (
            <button className="danger" disabled={busy} onClick={() => void softDelete()}>
              软删节点
            </button>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
