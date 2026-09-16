import { useState } from "react";
import type { MetricsSnapshotDTO } from "../api/types";
import { adminApi } from "../api/endpoints";
import { useFetch } from "../api/useFetch";

function ms(value: number | null): string {
  return value === null ? "—" : `${value.toFixed(1)} ms`;
}

/** 监控面板（admin；ADR-010）：在线指标快照 + 容量健康巡检。 */
export function AdminPage() {
  const [windowSeconds, setWindowSeconds] = useState(3600);
  const metricsState = useFetch(() => adminApi.metrics(windowSeconds), [windowSeconds]);
  const healthState = useFetch(() => adminApi.health(), []);

  const metrics: MetricsSnapshotDTO | null = metricsState.data;
  const health = healthState.data;
  const totalCalls = metrics?.endpoints.reduce((sum, endpoint) => sum + endpoint.calls, 0) ?? 0;
  const totalErrors = metrics?.endpoints.reduce((sum, endpoint) => sum + endpoint.errors, 0) ?? 0;
  const slowCount = metrics?.slowQueries.length ?? 0;
  const errorRate = totalCalls > 0 ? ((totalErrors / totalCalls) * 100).toFixed(2) : "0.00";

  return (
    <div className="page">
      <div className="page-head">
        <h1>监控</h1>
        <span className="meta">ADR-010 · admin 专属</span>
      </div>

      {metricsState.error ? (
        <div className="notice error">{metricsState.error.message}</div>
      ) : null}
      {healthState.error ? <div className="notice error">{healthState.error.message}</div> : null}

      <div className="toolbar">
        <label className="row" style={{ gap: "var(--sp-1)" }}>
          <span style={{ fontSize: "var(--fs-1)", color: "var(--ink-2)" }}>指标窗口</span>
          <select value={windowSeconds} onChange={(e) => setWindowSeconds(Number(e.target.value))}>
            <option value={600}>近 10 分钟</option>
            <option value={3600}>近 1 小时</option>
            <option value={21600}>近 6 小时</option>
            <option value={86400}>近 24 小时</option>
          </select>
        </label>
        <div className="spacer" />
        <span style={{ fontSize: "var(--fs-1)", color: "var(--ink-3)" }}>
          {metrics ? `快照 ${metrics.generatedAt.replace("T", " ").slice(0, 19)} · log_dir ${metrics.logDir}` : ""}
        </span>
      </div>

      {metricsState.loading ? <div className="loading">载入指标…</div> : null}
      {metrics ? (
        <>
          <div className="metric-grid">
            <div className="card metric">
              <div className="k">请求总数（窗口内）</div>
              <div className="v">{totalCalls}</div>
            </div>
            <div className="card metric">
              <div className="k">错误率</div>
              <div className="v">{errorRate}%</div>
            </div>
            <div className="card metric">
              <div className="k">鉴权失败</div>
              <div className="v">{metrics.authFailures}</div>
            </div>
            <div className="card metric">
              <div className="k">慢查询</div>
              <div className="v">{slowCount}</div>
            </div>
            <div className="card metric">
              <div className="k">渲染次数</div>
              <div className="v">{metrics.renders}</div>
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h2>端点耗时（P50 / P95 / Max）</h2>
            </div>
            <table className="data">
              <thead>
                <tr>
                  <th>端点</th>
                  <th>调用</th>
                  <th>P50</th>
                  <th>P95</th>
                  <th>Max</th>
                  <th>错误</th>
                </tr>
              </thead>
              <tbody>
                {metrics.endpoints.map((endpoint) => (
                  <tr key={`${endpoint.method}-${endpoint.route}`}>
                    <td>
                      <span className="chip">{endpoint.method}</span> {endpoint.route}
                    </td>
                    <td>{endpoint.calls}</td>
                    <td>{ms(endpoint.p50Millis)}</td>
                    <td>{ms(endpoint.p95Millis)}</td>
                    <td>{ms(endpoint.maxMillis)}</td>
                    <td>{endpoint.errors}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {metrics.slowQueries.length > 0 ? (
            <>
              <div className="section-label">慢查询明细</div>
              <div className="card">
                <div className="card-body">
                  {metrics.slowQueries.map((query, index) => (
                    <pre
                      key={index}
                      style={{ fontFamily: "var(--mono)", fontSize: "var(--fs-0)", margin: "0 0 var(--sp-2)" }}
                    >
                      {JSON.stringify(query)}
                    </pre>
                  ))}
                </div>
              </div>
            </>
          ) : null}
        </>
      ) : null}

      <div className="section-label">容量健康巡检</div>
      {healthState.loading ? <div className="loading">巡检中…</div> : null}
      {health ? (
        <>
          <div className="card">
            <div className="card-head">
              <h2>表健康（快照 {health.generatedAt.replace("T", " ").slice(0, 19)}）</h2>
            </div>
            <table className="data">
              <thead>
                <tr>
                  <th>表</th>
                  <th>行数（约）</th>
                  <th>分区</th>
                  <th>索引膨胀</th>
                  <th>死元组</th>
                  <th>归档</th>
                </tr>
              </thead>
              <tbody>
                {health.tables.map((table) => (
                  <tr key={table.table}>
                    <td>
                      <span className="chip">{table.table}</span>
                    </td>
                    <td>{table.rowsApprox.toLocaleString()}</td>
                    <td>{table.partitions ?? "—"}</td>
                    <td>{table.indexBloatPct === null ? "—" : `${table.indexBloatPct.toFixed(1)}%`}</td>
                    <td>{table.deadTuplePct === null ? "—" : `${table.deadTuplePct.toFixed(1)}%`}</td>
                    <td>{table.archiveOverdue ? <span className="badge orphaned">逾期</span> : <span className="badge resolved">正常</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {health.suggestions.length > 0 ? (
            <div className="notice" style={{ marginTop: "var(--sp-3)" }}>
              {health.suggestions.join("；")}
            </div>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
