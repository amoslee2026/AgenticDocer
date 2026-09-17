import { useState } from "react";
import { authApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { useAuth } from "./AuthContext";

/** 登录页（REQ-M10-F02 / user_manual §5.1）：SSH 挑战-响应，本地 CLI 签名粘贴。 */
export function LoginPage() {
  const { refresh } = useAuth();
  const [nonce, setNonce] = useState<string | null>(null);
  const [fingerprint, setFingerprint] = useState("");
  const [signature, setSignature] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  async function fetchChallenge() {
    setBusy(true);
    setError(null);
    try {
      const challenge = await authApi.challenge();
      setNonce(challenge.nonce);
      setSignature("");
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  async function submit() {
    if (!nonce || !fingerprint.trim() || !signature.trim()) {
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await authApi.login(fingerprint.trim(), nonce, signature.trim());
      setDone(true);
      await refresh();
    } catch (exc) {
      setError(exc instanceof ApiError ? exc.message : String(exc));
    } finally {
      setBusy(false);
    }
  }

  const command = nonce
    ? `uv run agenticspec auth sign --login --nonce ${nonce}`
    : "uv run agenticspec auth sign --login --nonce <nonce>";

  return (
    <div className="login-wrap">
      <div className="card login-card">
        <div className="card-head">
          <h2>登录 AgenticSpec</h2>
          <span className="chip">SSH 挑战-响应</span>
        </div>
        <div className="card-body">
          {error ? <div className="notice error">{error}</div> : null}
          <div className="login-steps">
            <div className="login-step">
              <div className="step-title">
                <span className="step-no">1</span> 获取一次性挑战（TTL 120s）
              </div>
              {nonce ? (
                <div className="nonce-box">
                  <span>{nonce}</span>
                  <button className="ghost" onClick={() => void fetchChallenge()} disabled={busy}>
                    换一个
                  </button>
                </div>
              ) : (
                <button className="primary" onClick={() => void fetchChallenge()} disabled={busy}>
                  获取挑战
                </button>
              )}
            </div>

            <div className="login-step">
              <div className="step-title">
                <span className="step-no">2</span> 在本机用 SSH 私钥签名（浏览器不接触私钥）
              </div>
              <div className="cmd-hint">{command}</div>
              <label className="field">
                <span>公钥指纹（ssh-keygen -lf ~/.ssh/id_ed25519.pub 的输出）</span>
                <input
                  type="text"
                  placeholder="SHA256:…"
                  value={fingerprint}
                  onChange={(e) => setFingerprint(e.target.value)}
                />
              </label>
            </div>

            <div className="login-step">
              <div className="step-title">
                <span className="step-no">3</span> 粘贴签名并登录
              </div>
              <label className="field">
                <span>SSHSIG 签名（base64 或 armor 均可）</span>
                <textarea
                  rows={4}
                  placeholder={"-----BEGIN SSH SIGNATURE-----\n…\n-----END SSH SIGNATURE-----"}
                  value={signature}
                  onChange={(e) => setSignature(e.target.value)}
                />
              </label>
              <div className="row end">
                <button
                  className="primary"
                  disabled={busy || !nonce || !fingerprint.trim() || !signature.trim()}
                  onClick={() => void submit()}
                >
                  登录
                </button>
              </div>
            </div>
          </div>
          <div className="login-foot">
            会话 8 小时滑动续期 · 无密码体系，身份唯一根为 SSH 公钥（ADR-007）
          </div>
          {done ? <div className="notice ok">登录成功，正在进入…</div> : null}
        </div>
      </div>
    </div>
  );
}
