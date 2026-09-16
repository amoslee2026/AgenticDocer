import { useState } from "react";
import type { DocDiffDTO } from "../api/types";
import { ApiError } from "../api/client";
import { docApi } from "../api/endpoints";

function renderValue(value: unknown): string {
  if (value === undefined) {
    return "（无）";
  }
  if (value === null) {
    return "null";
  }
  if (typeof value === "string") {
    return value;
  }
  return JSON.stringify(value, null, 1);
}

const OP_LABEL: Record<string, string> = {
  added: "新增",
  modified: "修改",
  deleted: "软删",
  ref_added: "引用 +",
  ref_removed: "引用 −",
};

/** 结构化 diff 视图（REQ-M08-F02）：按字段并排展示 before/after（非行级）。 */
export function DiffView({ docId }: { docId: string }) {
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [result, setResult] = useState<DocDiffDTO | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    setBusy(true);
    setError(null);
    try {
      setResult(await docApi.diff(docId, from.trim() || undefined, to.trim() || undefined));
    } catch (exc) {
      setError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <div className="toolbar">
        <label className="row" style={{ gap: "var(--sp-1)" }}>
          <span style={{ fontSize: "var(--fs-1)", color: "var(--ink-2)" }}>from（版本号或 ISO，空 = 上次变更）</span>
          <input type="text" value={from} placeholder="1 或 2026-09-16T12:00:00Z" onChange={(e) => setFrom(e.target.value)} style={{ width: 220 }} />
        </label>
        <label className="row" style={{ gap: "var(--sp-1)" }}>
          <span style={{ fontSize: "var(--fs-1)", color: "var(--ink-2)" }}>to（空 = 当前态）</span>
          <input type="text" value={to} placeholder="2" onChange={(e) => setTo(e.target.value)} style={{ width: 160 }} />
        </label>
        <button className="primary" onClick={() => void run()} disabled={busy}>
          {busy ? "计算中…" : "计算 diff"}
        </button>
      </div>
      {error ? <div className="notice error">{error}</div> : null}
      {result ? (
        <>
          <div className="notice">
            {result.fromTs ?? "（上次变更）"} → {result.toTs ?? "（当前）"} · 新增{" "}
            {result.summary.added} · 修改 {result.summary.modified} · 软删 {result.summary.deleted} · 引用{" "}
            {result.summary.refs}
          </div>
          {result.changes.length === 0 ? (
            <div className="empty">两个时点之间没有任何变更（空 diff，非 404）。</div>
          ) : null}
          {result.changes.map((entry, index) => (
            <div key={index} className={`diff-entry op-${entry.op}`}>
              <div className="diff-head">
                <strong>{OP_LABEL[entry.op] ?? entry.op}</strong>
                <span>{entry.nodeId ?? "—"}</span>
                {entry.anchor ? <span>#{entry.anchor}</span> : null}
                {entry.field ? <span>field: {entry.field}</span> : null}
              </div>
              {entry.op === "modified" ? (
                <div className="diff-cols">
                  <div className="before">
                    <span className="label">before</span>
                    {renderValue(entry.before)}
                  </div>
                  <div className="after">
                    <span className="label">after</span>
                    {renderValue(entry.after)}
                  </div>
                </div>
              ) : (
                <div className="diff-cols">
                  <div className={entry.op === "deleted" ? "before" : "after"} style={{ gridColumn: "1 / -1" }}>
                    <span className="label">{entry.op === "added" ? "after" : "before"}</span>
                    {renderValue(entry.op === "added" ? entry.after : entry.before)}
                  </div>
                </div>
              )}
            </div>
          ))}
        </>
      ) : null}
    </div>
  );
}
