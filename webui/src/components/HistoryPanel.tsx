import { useMemo, useState } from "react";
import type { EventDTO, NodeDTO } from "../api/types";
import { ApiError } from "../api/client";
import { eventApi } from "../api/endpoints";

function payloadSummary(event: EventDTO): string {
  const payload = event.payload ?? {};
  const keys = Object.keys(payload);
  if (keys.length === 0) {
    return "";
  }
  return keys
    .map((key) => {
      const value = payload[key];
      const text = typeof value === "string" ? value : JSON.stringify(value);
      return `${key}=${text?.slice(0, 60)}`;
    })
    .join("  ");
}

/**
 * 追溯与历史视图（REQ-M08-F04）：`/events/replay` 折叠 + 事件序列；
 * 每个历史事件经 `?upto=<event_id>` 回放该时点的折叠态（含端）。
 */
export function HistoryPanel({ node }: { node: NodeDTO }) {
  const [snap, setSnap] = useState<{ node: NodeDTO | null; history: EventDTO[] } | null>(null);
  const [pointNode, setPointNode] = useState<NodeDTO | null>(null);
  const [pointBusy, setPointBusy] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function viewAt(event: EventDTO) {
    setPointBusy(true);
    setError(null);
    try {
      setPointNode((await eventApi.replayNode(node.nodeId, event.eventId)).node);
    } catch (exc) {
      setError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setPointBusy(false);
    }
  }

  async function load() {
    setBusy(true);
    setError(null);
    setSnap(null);
    setViewIndex(null);
    try {
      const result = await eventApi.replayNode(node.nodeId);
      setSnap(result);
    } catch (exc) {
      setError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  const viewed = useMemo(() => {
    if (!snap) {
      return null;
    }
    if (viewIndex === null) {
      return snap.node;
    }
    return null;
  }, [snap, viewIndex]);

  return (
    <div>
      <div className="toolbar">
        <button className="primary" onClick={() => void load()} disabled={busy}>
          {busy ? "重放中…" : "载入版本历史（事件重放）"}
        </button>
        <span style={{ fontSize: "var(--fs-1)", color: "var(--ink-3)" }}>
          当前 v{node.version} · {node.status}
        </span>
      </div>
      {error ? <div className="notice error">{error}</div> : null}
      {snap ? (
        <>
          {viewed ? (
            <div className="card" style={{ marginBottom: "var(--sp-3)" }}>
              <div className="card-head">
                <h2>{viewIndex === null ? "当前折叠态" : "历史时点折叠态"}</h2>
                <span className="chip">v{viewed.version}</span>
              </div>
              <div className="card-body">
                <dl className="kv">
                  <dt>anchor</dt>
                  <dd>{viewed.anchor}</dd>
                  <dt>atomType</dt>
                  <dd>{viewed.atomType}</dd>
                  <dt>status</dt>
                  <dd>{viewed.status}</dd>
                  <dt>content</dt>
                  <dd>{JSON.stringify(viewed.content)}</dd>
                </dl>
              </div>
            </div>
          ) : (
            <div className="notice" style={{ marginBottom: "var(--sp-3)" }}>
              折叠序列中无 create 事件（node=null）。
            </div>
          )}
          <ol className="timeline">
            {snap.history.map((event, index) => (
              <li key={event.eventId}>
                <div className="tl-head">
                  <span className="tl-op">{event.op}</span>
                  <span>{event.actor}</span>
                  <span>{event.ts.replace("T", " ").slice(0, 19)}</span>
                  <span>{event.eventId}</span>
                </div>
                <div className="tl-body">{payloadSummary(event)}</div>
                <button className="ghost" onClick={() => setViewIndex(index)}>
                  回看此事件后的状态
                </button>
              </li>
            ))}
          </ol>
        </>
      ) : null}
    </div>
  );
}
