import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useFetch } from "../api/useFetch";
import { docApi } from "../api/endpoints";
import type { DocDTO } from "../api/types";

function formatWhen(iso: string): string {
  return iso.replace("T", " ").slice(0, 19);
}

/** 文档清单（REQ-M08：列表含 version/status）。 */
export function DocsPage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState("");
  const [query, setQuery] = useState("");
  const { data, loading, error } = useFetch(() => docApi.list(status || undefined), [status]);

  const docs = useMemo(() => {
    const all = data ?? [];
    const needle = query.trim().toLowerCase();
    if (!needle) {
      return all;
    }
    return all.filter(
      (doc) =>
        doc.title.toLowerCase().includes(needle) ||
        doc.docId.toLowerCase().includes(needle) ||
        doc.docType.toLowerCase().includes(needle),
    );
  }, [data, query]);

  return (
    <div className="page">
      <div className="page-head">
        <h1>文档</h1>
        <span className="meta">{docs.length} 份</span>
      </div>
      <div className="toolbar">
        <input
          type="search"
          placeholder="按标题 / docId / 类型过滤…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: 320 }}
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">全部状态</option>
          <option value="draft">draft</option>
          <option value="reviewed">reviewed</option>
          <option value="approved">approved</option>
        </select>
        <div className="spacer" />
      </div>
      {error ? <div className="notice error">{error.message}</div> : null}
      {loading ? <div className="loading">载入中…</div> : null}
      {docs.length === 0 && !loading ? (
        <div className="empty">没有匹配的文档——调整过滤条件，或先用导入器（M03）导入语料。</div>
      ) : null}
      {docs.length > 0 ? (
        <div className="card">
          <table className="data">
            <thead>
              <tr>
                <th>标题</th>
                <th>docId</th>
                <th>类型</th>
                <th>状态</th>
                <th>版本</th>
                <th>更新时间</th>
              </tr>
            </thead>
            <tbody>
              {docs.map((doc: DocDTO) => (
                <tr
                  key={doc.docId}
                  className="clickable"
                  onClick={() => navigate(`/docs/${encodeURIComponent(doc.docId)}`)}
                >
                  <td>{doc.title}</td>
                  <td>
                    <span className="chip">{doc.docId}</span>
                  </td>
                  <td>{doc.docType}</td>
                  <td>
                    <span className={`badge ${doc.status}`}>{doc.status}</span>
                  </td>
                  <td>
                    <span className="chip">v{doc.version}</span>
                  </td>
                  <td>{formatWhen(doc.updatedAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
