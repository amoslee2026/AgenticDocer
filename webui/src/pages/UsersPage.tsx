import { useState } from "react";
import type { GrantDTO, RoleInfoDTO, UserDTO } from "../api/types";
import { ApiError } from "../api/client";
import { userApi } from "../api/endpoints";
import { useFetch } from "../api/useFetch";

function shortFp(fp: string): string {
  return fp.length > 28 ? `${fp.slice(0, 25)}…` : fp;
}

/** 用户与权限管理（admin 专属；user_manual §5.2 / §8）。 */
export function UsersPage() {
  const usersState = useFetch(() => userApi.list(), []);
  const rolesState = useFetch(() => userApi.roles(), []);
  const grantsState = useFetch(() => userApi.grants(), []);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [newUsername, setNewUsername] = useState("");
  const [newRole, setNewRole] = useState("reader");
  const [keyDrafts, setKeyDrafts] = useState<Map<string, string>>(new Map());
  const [grantDraft, setGrantDraft] = useState({ userId: "", scope: "doc_type", value: "", permission: "read" });

  const users = usersState.data ?? [];
  const roles: RoleInfoDTO[] = rolesState.data ?? [];
  const grants = grantsState.data ?? [];

  async function run(action: () => Promise<unknown>, okMessage: string) {
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      await action();
      setNotice(okMessage);
      await Promise.all([usersState.reload(), grantsState.reload()]);
    } catch (exc) {
      setError(exc instanceof ApiError ? `${exc.message}${exc.violations.length ? `（${exc.violations[0]?.fixHint ?? ""}）` : ""}` : String(exc));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="page">
      <div className="page-head">
        <h1>用户与权限</h1>
        <span className="meta">admin 专属</span>
      </div>
      {error ? <div className="notice error">{error}</div> : null}
      {notice ? <div className="notice ok">{notice}</div> : null}

      <div className="section-label">用户新建</div>
      <div className="card">
        <div className="card-body">
          <div className="row">
            <input
              type="text"
              placeholder="用户名"
              value={newUsername}
              onChange={(e) => setNewUsername(e.target.value)}
              style={{ width: 220 }}
            />
            <select value={newRole} onChange={(e) => setNewRole(e.target.value)}>
              {(roles.length > 0 ? roles.map((r) => r.role) : ["admin", "editor", "reviewer", "reader"]).map(
                (role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ),
              )}
            </select>
            <button
              className="primary"
              disabled={busy || !newUsername.trim()}
              onClick={() =>
                void run(async () => {
                  await userApi.create(newUsername.trim(), newRole);
                  setNewUsername("");
                }, "用户已创建。")
              }
            >
              创建用户
            </button>
          </div>
        </div>
      </div>

      <div className="section-label">用户（{users.length}）</div>
      {usersState.loading ? <div className="loading">载入中…</div> : null}
      {users.length > 0 ? (
        <div className="card">
          <table className="data">
            <thead>
              <tr>
                <th>用户名</th>
                <th>角色</th>
                <th>状态</th>
                <th>公钥指纹</th>
                <th>登记新公钥</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {users.map((user: UserDTO) => (
                <tr key={user.userId}>
                  <td>{user.username}</td>
                  <td>
                    <select
                      value={user.role}
                      onChange={(e) =>
                        void run(
                          () => userApi.patch(user.userId, { role: e.target.value }),
                          `${user.username} 角色已改为 ${e.target.value}。`,
                        )
                      }
                    >
                      {(roles.length > 0 ? roles.map((r) => r.role) : [user.role]).map((role) => (
                        <option key={role} value={role}>
                          {role}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <span className={`badge ${user.status}`}>{user.status}</span>
                  </td>
                  <td>
                    {user.keyFingerprints.length === 0 ? (
                      <span className="meta">（无）</span>
                    ) : (
                      user.keyFingerprints.map((fp) => (
                        <div key={fp} className="row" style={{ gap: "var(--sp-1)" }}>
                          <span className="chip" title={fp}>
                            {shortFp(fp)}
                          </span>
                          <button
                            className="ghost danger"
                            disabled={busy}
                            onClick={() =>
                              void run(
                                () => userApi.revokeKey(user.userId, fp),
                                "公钥已吊销。",
                              )
                            }
                          >
                            吊销
                          </button>
                        </div>
                      ))
                    )}
                  </td>
                  <td>
                    <div className="row" style={{ gap: "var(--sp-1)" }}>
                      <input
                        type="text"
                        placeholder="ssh-ed25519 AAAA…"
                        value={keyDrafts.get(user.userId) ?? ""}
                        onChange={(e) =>
                          setKeyDrafts((current) => new Map(current).set(user.userId, e.target.value))
                        }
                        style={{ width: 260 }}
                      />
                      <button
                        disabled={busy || !(keyDrafts.get(user.userId) ?? "").trim()}
                        onClick={() =>
                          void run(async () => {
                            await userApi.addKey(user.userId, (keyDrafts.get(user.userId) ?? "").trim());
                            setKeyDrafts((current) => new Map(current).set(user.userId, ""));
                          }, "公钥已登记。")
                        }
                      >
                        登记
                      </button>
                    </div>
                  </td>
                  <td>
                    <div className="row">
                      <button
                        className="ghost"
                        disabled={busy}
                        onClick={() =>
                          void run(
                            () =>
                              userApi.patch(
                                user.userId,
                                { status: user.status === "active" ? "disabled" : "active" },
                              ),
                            "用户状态已更新。",
                          )
                        }
                      >
                        {user.status === "active" ? "禁用" : "启用"}
                      </button>
                      <button
                        className="ghost danger"
                        disabled={busy}
                        onClick={() => void run(() => userApi.remove(user.userId), "用户已删除。")}
                      >
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      <div className="section-label">文档集级授权（grant：角色硬上限内的范围收窄）</div>
      <div className="card">
        <div className="card-body">
          <div className="row">
            <select
              value={grantDraft.userId}
              onChange={(e) => setGrantDraft((d) => ({ ...d, userId: e.target.value }))}
            >
              <option value="">选择用户…</option>
              {users.map((user) => (
                <option key={user.userId} value={user.userId}>
                  {user.username}
                </option>
              ))}
            </select>
            <select
              value={grantDraft.scope}
              onChange={(e) => setGrantDraft((d) => ({ ...d, scope: e.target.value }))}
            >
              <option value="doc_type">doc_type</option>
              <option value="doc">doc</option>
            </select>
            <input
              type="text"
              placeholder={grantDraft.scope === "doc_type" ? "standard / product…" : "docId…"}
              value={grantDraft.value}
              onChange={(e) => setGrantDraft((d) => ({ ...d, value: e.target.value }))}
              style={{ width: 220 }}
            />
            <select
              value={grantDraft.permission}
              onChange={(e) => setGrantDraft((d) => ({ ...d, permission: e.target.value }))}
            >
              <option value="read">read</option>
              <option value="write">write</option>
              <option value="review">review</option>
            </select>
            <button
              className="primary"
              disabled={busy || !grantDraft.userId || !grantDraft.value.trim()}
              onClick={() =>
                void run(async () => {
                  await userApi.createGrant({ ...grantDraft, value: grantDraft.value.trim() });
                  setGrantDraft((d) => ({ ...d, value: "" }));
                }, "授权已创建。")
              }
            >
              授予
            </button>
          </div>
          {grants.length > 0 ? (
            <table className="data" style={{ marginTop: "var(--sp-3)" }}>
              <thead>
                <tr>
                  <th>用户</th>
                  <th>scope</th>
                  <th>value</th>
                  <th>permission</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {grants.map((grant: GrantDTO) => (
                  <tr key={`${grant.userId}-${grant.scope}-${grant.value}-${grant.permission}`}>
                    <td>{users.find((user) => user.userId === grant.userId)?.username ?? grant.userId}</td>
                    <td>{grant.scope}</td>
                    <td>
                      <span className="chip">{grant.value}</span>
                    </td>
                    <td>{grant.permission}</td>
                    <td>
                      <button
                        className="ghost danger"
                        disabled={busy}
                        onClick={() => void run(() => userApi.deleteGrant(grant.userId), "授权已撤销。")}
                      >
                        撤销
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty" style={{ marginTop: "var(--sp-3)" }}>
              暂无 grant 记录。
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
