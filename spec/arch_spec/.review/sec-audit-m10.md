---
title: M10 独立安全复核报告（SecAudit）
type: composite
purpose: review
audience: both
direction: output
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# M10 鉴权独立安全复核（SecAudit，2026-09-16）

**复核方式**：只读对抗复核（不修改任何文件），独立隔离库 `agenticspec_secaudit_test`（已 DROP）。
**复核对象**：`src/agenticspec/auth/`（10 文件）+ 其 83 测试。
**结论**：**通过，无阻塞**。8 项断言 **7 项已验属实**、1 项部分（S11 RSA 反向，属规范既定选择）。无 CRITICAL/HIGH。

## 一、8 项断言逐条验证

| # | 断言 | 结论 | 证据 |
|---|---|---|---|
| 1 | S11 与真实 `ssh-keygen` 互操作 | **已验**（RSA 反向部分） | ed25519 双向 PASS；RSA-3072 正向 PASS；**反向 RSA：M10 默认 PSS 签名被 OpenSSH 8.0p1 `-Y verify` 拒绝**，但规范明文「签名固定 PSS/验签回落 v1.5」，故属规范选择非实现偏差。**宣传口径修正**：「双向互操作」仅在 ed25519 严格成立 |
| 2 | S2 签名载荷含 query | **已验** | `signing.py:186-189` + `middleware.py:213-218`；实测签 `?limit=5` 验 `?limit=6` 失败。**附带发现 AUD-2**：用 `scope["path"]`（已解码）而非原样字节，与 S2 字面不符（无绕过，仅互操作陷阱） |
| 3 | S7 未认证不写库 | **已验（实测）** | 坏签名 401 → `nonces` 计数不变；未注册 key 403 → 不变；好签名 200 → +1；重放 → 401 无新行。（豁免端点 `/auth/challenge` 每签发写一行，属设计例外） |
| 4 | S4 fail-closed 与豁免清单 | **已验** | 空 users 库：`/auth/challenge` 200、`/auth/login` 401、`/healthz` 200、其余 401 + bootstrap 提示；`/docs`/`/openapi.json` 非 DEV_MODE → 404；DEV_MODE 非 loopback 仍禁用。**M06 10 + M07 27 端点逐一核对全部携带鉴权依赖** |
| 5 | S10 审计防污染 | **已验** | 伪造 `X-SSH-Key-Id` + 坏签名 → `actor='anonymous'`，自述身份仅在 `payload.claimed_key_id`；SQL 断言含 `user_id`/`key_fingerprint` 键的失败事件数 = 0 |
| 6 | S5 双点拒绝 | **已验** | 授予侧 422；**绕过侧**（直插 grants 行）后判定仍 403（no-target / SPEC-A / SPEC-B 三目标均拒）——角色硬上限在判定时刻独立生效 |
| 7 | S3 nonce 时间窗耦合 | **已验（非 CRITICAL）** | `nonce_ttl_seconds() = max(2×skew, 600)`，实测 skew=300 → ttl=**600**（非写死 300）；时间戳窗 `[-30,+300]` 边界实测；无重放间隙 |
| 8 | 会话安全 S8/S13/S15 | **已验** | token = `secrets.token_urlsafe(32)`；`token_hash == sha256(token)` 且 ≠ 明文；禁用用户后既有 Cookie 立即 401（JOIN `users.status`）；过期会话 401 + purge 后仍 401；Cookie httpOnly/SameSite=Lax、非 loopback 强制 Secure |

## 二、额外对抗检查（均无绕过）

- **Cookie/签名优先级**：垃圾 Cookie + 有效签名 → 401 `invalid_session`（**fail-closed 不回落**，不可绕过）
- **bootstrap 幂等**：有 active admin 时换 key 文件不改写 DB（实测 key 行数不变）
- **挑战 TTL 120s 过期拒**；请求 nonce 不能冒充登录挑战；公钥跨用户登记 409
- M07 调 `update_user`/`delete_user` 均传 `actor_id`（S9 已接线）

## 三、问题清单

| ID | Sev | 位置 | 问题 | 处置 |
|---|---|---|---|---|
| **AUD-1** | **P2** | `auth/middleware.py:221-227` | **XFF 限流绕过**：`AUTH_TRUSTED_PROXY=1` 时取 XFF **首段**。实测：限流 3/min 下伪造不同首段 → 10 次全 200。攻击者可无限制打 `/auth/challenge`（每次 INSERT 一行 nonces → **兼作 nonces 表无界增长 DoS**）与 `/auth/login` | **派修**（取最后一段或 `AUTH_PROXY_COUNT`） |
| AUD-2 | P3 | `auth/middleware.py:213-218` | `raw_path` 用 ASGI **已解码**的 `scope["path"]`，与 S2「原样字节」不符。无绕过，但客户端必须签「解码后路径」的**隐式耦合未写进规范** | **派修或修规范**（择一） |
| AUD-3 | P3 | `auth/signing.py:74-76` | M10 产出的 **RSA(PSS) 签名被旧 OpenSSH 拒绝**（8.0p1）。规范选择如此，但「双向互操作」宣传仅 ed25519 成立 | 部署提示：需 OpenSSH≥8.1，或签名侧改产 v1.5 |
| AUD-4 | P3 | `auth/users.py:688-694` | **授权失败（403）审计把已验证身份降格为 `claimed_*`**（`actor='anonymous'`）。S10 规则本意针对**未验证**身份；此处丢失可归因的确定性 actor | 派修（加 `verified_actor` 参数） |
| AUD-5 | P3 | `auth/sessions.py:142-167`、`users.py` | **限流与失败聚合状态为进程内** → 多 worker 部署时限流上限放大 N 倍 | 单进程默认部署不受影响；**部署文档声明单进程约束** |
| AUD-6 | P3 | `auth/middleware.py:96-135` | `is_exempt`/`EXEMPT_PATHS` **导出但无运行时消费者**；S4 fail-closed 完全依赖每个端点自行挂 `Depends`（现状 41 端点已逐一核对全部有依赖，**当前安全**） | 风险：未来新增路由漏挂依赖即静默开放。**派修**（app.py 加全局兜底中间件）或删除 `is_exempt` 避免假象 |
| AUD-7 | P3 | `webui_api/router.py:825-835` | **① `GET /roles` 用 `ReadAuth`**，而 §3 规定 admin 专属；**② `GET /events`（ReadAuth）可查 `entity='auth'` 事件 → reader 即可看到全部鉴权失败审计（含来源 IP、`claimed_key_id`）** | **派修**（`/roles` 升 AdminAuth 或改规范；`/events` 对 `entity=auth` 加 AdminAuth 门槛或过滤敏感字段） |

## 四、无法独立验证项（显式声明）

- **「M10 修复了 3 个真实 bug」**：无可考的 bug-fix 历史（代码已呈修复后状态），**标记为无法验证**，不影响结论。

## 五、复核方法学

- 只读：未修改任何文件（`git status` 可验）
- 隔离：独立库 `agenticspec_secaudit_test`，跑完 DROP
- **不采信自述**：8 项断言全部实际执行或精确代码引用，无一条依赖 M10 的报告
- 独立复现 OpenSSH 互操作（自建密钥、自跑 `ssh-keygen -Y sign/verify`）

## 相关

- `architecture_specification.md` §3 M10、ADR-007（鉴权权威）
- `functional_specification.md` REQ-M10-F01..F05、§「安全评审（S1–S16）验收项补充」
- 复核者：`SecAudit`（reviewer agent），2026-09-16
