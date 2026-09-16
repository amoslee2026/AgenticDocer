import { useState } from "react";
import type { MetricsSnapshotDTO } from "../api/types";
import { adminApi } from "../api/endpoints";
import { useFetch } from "../api/useFetch";

function ms(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${value.toFixed(1)} ms`;
}

/** 监控面板（admin；ADR-010）：在线指标快照 + 容量健康巡检。字段形状以实测 API 为准。 */
export function AdminPage() {
  const [windowSeconds, setWindowSeconds] = useState(3600);
  const metricsState = useFetch(() => adminApi.metrics(windowSeconds), [windowSeconds]);
  const healthState = useFetch(() => adminApi.health(), []);

  const metrics = metricsState.data;
  const health = healthState.data;
  const totalCalls = metrics?.endpoints.reduce((sum, endpoint) => sum + endpoint.count, 0) ?? 0;
  const avgErrorRate =
    metrics && totalCalls > 0
      ? metrics.endpoints.reduce((sum, endpoint) => sum + endpoint.errorRate * endpoint.count, 0) / totalCalls
      : 0;
  const slowCount = metrics?.slowQueries.length ?? 0;

  return (
    <div className="page">
      <div className="page-head">
        <h1>监控</h1>
        <span className="meta">ADR-010 · admin 专属</span>
      </div>

      {metricsState.error ? <div className="notice error">{metricsState.error.message}</div> : null}
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
      </div>

      {metricsState.loading ? <div className="loading">载入指标…</div> : null}
      {metrics ? (
        <>
          <div className="metric-grid">
            <div className="card metric">
              <div className="k">请求总数（窗口 {metrics.windowSeconds}s）</div>
              <div className="v">{totalCalls}</div>
            </div>
            <div className="card metric">
              <div className="k">加权错误率</div>
              <div className="v">{(avgErrorRate * 100).toFixed(2)}%</div>
            </div>
            <div className="card metric">
              <div className="k">鉴权失败</div>
              <div className="v">{metrics.authFailures}</div>
            </div>
            <div className="card metric">
              <div className="k">慢查询</div>
              <div className="v">{slowCount}</div>
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h2>端点耗时（P50 / P95 / P99）</h2>
            </div>
            <table className="data">
              <thead>
                <tr>
                  <th>端点</th>
                  <th>调用</th>
                  <th>P50</th>
                  <th>P95</th>
                  <th>P99</th>
                  <th>错误率</th>
                </tr>
              </thead>
              <tbody>
                {metrics.endpoints.map((endpoint) => (
                  <tr key={endpoint.route}>
                    <td>
                      <span className="chip">{endpoint.route}</span>
                    </td>
                    <td>{endpoint.count}</td>
                    <td>{ms(endpoint.p50)}</td>
                    <td>{ms(endpoint.p95)}</td>
                    <td>{ms(endpoint.p99)}</td>
                    <td>{(endpoint.errorRate * 100).toFixed(2)}%</td>
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
              <h2>表健康（分区级行数）</h2>
              <span className={`badge ${/ok|正常|healthy/i.test(health.verdict) ? "resolved" : "orphaned"}`}>
                {health.verdict}
              </span>
            </div>
            <table className="data">
              <thead>
                <tr>
                  <th>表 / 分区</th>
                  <th>行数</th>
                  <th>大小</th>
                  <th>死元组</th>
                  <th>最近 autovacuum</th>
                </tr>
              </thead>
              <tbody>
                {health.tables.slice(0, 12).map((table) => (
                  <tr key={table.name}>
                    <td>
                      <span className="chip">{table.name}</span>
                    </td>
                    <td>{table.rows.toLocaleString()}</td>
                    <td>{(table.sizeBytes / 1024).toFixed(0)} KB</td>
                    <td>{table.deadTup}</td>
                    <td>{table.lastAutovacuum ? table.lastAutovacuum.replace("T", " ").slice(0, 19) : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="notice" style={{ marginTop: "var(--sp-3)" }}>
            巡检建议：{health.advice.length > 0 ? health.advice.join("；") : "无（各项正常）"}
          </div>
        </>
      ) : null}
    </div>
  );
}
