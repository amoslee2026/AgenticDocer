import { useMemo, useState } from "react";
import type { CommentDTO, CommentState, NodeDTO } from "../api/types";
import { ApiError } from "../api/client";
import { commentApi } from "../api/endpoints";
import { useFetch } from "../api/useFetch";

const STATES: CommentState[] = ["open", "resolved", "orphaned"];

interface Props {
  docId: string;
  nodes: NodeDTO[];
  /** 当前选中的节点（新建批注锚定它）。 */
  selectedNode: NodeDTO | null;
  canReview: boolean;
  onNodeJump: (node: NodeDTO) => void;
  onChanged: () => void;
}

/** 批注面板（REQ-M08-F03）：open/resolved/orphaned 全状态，含状态流转与新建。 */
export function CommentsPanel({ docId, nodes, selectedNode, canReview, onNodeJump, onChanged }: Props) {
  const [stateFilter, setStateFilter] = useState<CommentState | "">("");
  const { data, loading, error, reload } = useFetch(
    () => commentApi.listByDoc(docId, stateFilter ? [stateFilter] : undefined),
    [docId, stateFilter],
  );
  const [busy, setBusy] = useState(false);
  const [panelError, setPanelError] = useState<string | null>(null);
  const [newBody, setNewBody] = useState("");

  const nodeById = useMemo(() => {
    const map = new Map<string, NodeDTO>();
    for (const node of nodes) {
      map.set(node.nodeId, node);
    }
    return map;
  }, [nodes]);

  async function create() {
    if (!selectedNode || !newBody.trim()) {
      return;
    }
    setBusy(true);
    setPanelError(null);
    try {
      await commentApi.create(selectedNode.nodeId, newBody.trim(), selectedNode.version);
      setNewBody("");
      await reload();
      onChanged();
    } catch (exc) {
      setPanelError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  async function transition(comment: CommentDTO, state: CommentState) {
    setBusy(true);
    setPanelError(null);
    try {
      await commentApi.setState(comment.commentId, state, comment.version);
      await reload();
      onChanged();
    } catch (exc) {
      setPanelError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      {panelError ? <div className="notice error">{panelError}</div> : null}
      {error ? <div className="notice error">{error.message}</div> : null}

      <div className="toolbar">
        <select value={stateFilter} onChange={(e) => setStateFilter(e.target.value as CommentState | "")}>
          <option value="">全部状态</option>
          {STATES.map((state) => (
            <option key={state} value={state}>
              {state}
            </option>
          ))}
        </select>
        <div className="spacer" />
        <span className="meta" style={{ fontSize: "var(--fs-1)", color: "var(--ink-3)" }}>
          {data?.length ?? 0} 条
        </span>
      </div>

      {canReview ? (
        <div className="card" style={{ marginBottom: "var(--sp-3)" }}>
          <div className="card-body">
            <label className="field">
              <span>
                新批注 → 锚定节点：
                {selectedNode ? (
                  <span className="chip">{selectedNode.anchor}</span>
                ) : (
                  "（先在左侧选中一个节点）"
                )}
              </span>
              <textarea
                rows={2}
                value={newBody}
                placeholder="写批注…（reviewer 及以上角色）"
                onChange={(e) => setNewBody(e.target.value)}
              />
            </label>
            <div className="row end">
              <button
                className="primary"
                disabled={busy || !selectedNode || !newBody.trim()}
                onClick={() => void create()}
              >
                创建批注
              </button>
            </div>
          </div>
        </div>
      ) : null}

      {loading ? <div className="loading">载入中…</div> : null}
      {!loading && (data?.length ?? 0) === 0 ? (
        <div className="empty">当前过滤条件下没有批注。</div>
      ) : null}
      {(data ?? []).map((comment) => {
        const node = nodeById.get(comment.nodeId);
        return (
          <div key={comment.commentId} className={`comment ${comment.state}`}>
            <div className="head">
              <span className={`badge ${comment.state}`}>{comment.state}</span>
              <span className="author">{comment.author}</span>
              <span>{comment.ts.replace("T", " ").slice(0, 16)}</span>
              {node ? (
                <button className="ghost" onClick={() => onNodeJump(node)}>
                  → {node.anchor}
                </button>
              ) : comment.state === "orphaned" ? (
                <span className="chip">节点已删除</span>
              ) : null}
              <div className="spacer" />
              {canReview && comment.state === "open" ? (
                <button className="ghost" disabled={busy} onClick={() => void transition(comment, "resolved")}>
                  标记已解决
                </button>
              ) : null}
              {canReview && comment.state === "resolved" ? (
                <button className="ghost" disabled={busy} onClick={() => void transition(comment, "open")}>
                  重新打开
                </button>
              ) : null}
            </div>
            <div className="body">{comment.body}</div>
          </div>
        );
      })}
    </div>
  );
}
