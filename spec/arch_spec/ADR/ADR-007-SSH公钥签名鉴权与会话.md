---
title: ADR-007 SSH 公钥签名鉴权与会话
type: composite
purpose: architecture
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# ADR-007：SSH 公钥签名鉴权与会话机制

- **状态**：已接受（2026-09-16，依用户批注 A2/A1 及澄清）
- **决策者**：用户（批注）+ 架构评审
- **影响范围**：M10（新增）、M06/M07 全端点、`users`/`ssh_keys`/`grants`/`sessions` 表、CLI/WebUI 客户端、ADR-002 部署假设 B6

## 背景

原架构假设 **B6「单机、单用户、无鉴权」**（`clarifications.md` §2），M06 仅要求自由文本 `X-Actor` 头标识调用方。该假设在批注 A2 中被直接推翻：

> agent 写入需要鉴权，通过启动 agent 的人类用户的 ssh 公钥进行鉴定身份

且用户进一步要求：**WebUI 登录同样需要身份鉴权**，并**提供管理员账号用于用户权限管理**。规模目标亦提升至「≥10,000 个已注册 agent 身份」（批注 A8）。

因此需要一套**身份源单一、无需额外 PKI/密码体系**的鉴权方案。

## 决策

### 1. 身份根 = SSH 公钥（Ed25519 优先）

用户身份的唯一凭据是其 SSH 公钥（`~/.ssh/id_ed25519.pub`）。理由：

- **零新增秘密**：agent 本就运行在人类用户会话中，SSH 私钥天然可用，无需分发密码/token；
- **可归属**：公钥指纹 → `users` 行，`actor` 字段可精确归因到「哪个人类启动了哪个 agent」；
- **成熟**：Ed25519 验签由 `cryptography` 库提供，无自研密码学。

曲线支持：**Ed25519（首选）与 RSA-3072+（兼容）**；拒绝 DSA/ECDSA-P256 以下强度。

### 2. 两条鉴权路径，同一身份源

| 路径 | 凭据 | 交换时机 |
|---|---|---|
| **agent（CLI/API）** | 每请求签名（无状态） | 每次 HTTP 请求 |
| **WebUI（浏览器）** | 会话 Cookie | 一次挑战-响应登录 → 8h 会话 |

**agent 签名协议**（每请求）：

```
载荷 = f"{METHOD}\n{PATH}\n{SHA256(body).hex()}\n{X-Timestamp}\n{X-Nonce}"
请求头: X-SSH-Key-Id, X-SSH-Signature(base64), X-Timestamp, X-Nonce
```

服务端校验顺序：时间窗（±300s）→ nonce 未复用（PG 唯一约束）→ 公钥查表（active）→ 验签 → 角色解析。

**WebUI 登录协议**（一次性）：

```
1. POST /api/v1/auth/challenge        → { nonce, expiresAt }（TTL 120s）
2. 客户端用私钥签名 nonce（ssh-keygen -Y sign 或 libcrypto）
3. POST /api/v1/auth/login            → 验签通过 → Set-Cookie: agenticdocer_session=...（httpOnly, SameSite=Lax, Secure 视部署）
```

**为何不给 WebUI 用密码**：引入第二身份源会带来「密码↔公钥如何关联同一用户」的映射问题，且需额外的密码存储/重置/强度策略。SSH 挑战-响应复用同一 `users` 行，**身份源唯一**。

**浏览器如何签名**：登录页提供三种方式（按可用性降级）：(a) 本地 `agenticdocer-auth sign` CLI（推荐，签名结果粘贴回页面）；(b) WebAuthn 桥接（若浏览器支持且用户已绑定）；(c) 上传一次性签名文件。**明确不做**在浏览器内直接读取私钥（安全禁区）。

### 3. 逐步降级：从 B6 到鉴权的迁移

| 阶段 | 鉴权状态 |
|---|---|
| 部署 | 无 `users` 表行 → 系统拒绝所有请求（fail-closed） |
| 自举 | `ADMIN_SSH_PUBKEY_FILE` → 首个 admin（幂等） |
| 运行 | admin 在 WebUI 增用户/授角色；agent 用各自公钥签名 |

**fail-closed 而非 fail-open**：无 admin 时系统不可用（明确报错指向自举步骤），避免「忘记配鉴权=裸奔」。

### 4. 管理员自举

```bash
# 部署时（环境变量引导，用户裁决）
echo "$(cat ~/.ssh/id_ed25519.pub)" > data/admin_keys/admin.pub
uv run agenticdocer-auth bootstrap            # 幂等：已有 admin 则跳过
```

`data/admin_keys/` 纳入 `.gitignore`（含个人公钥，虽非秘密但不必入库）。

### 5. RBAC：四角色 + 文档集级授权

| 角色 | 权限 |
|---|---|
| admin | 用户/授权管理 + 全部文档操作 |
| editor | 文档 CRUD、批注、表格编辑 |
| reviewer | 批注、状态审批、只读 |
| reader | 只读 |

**文档集级授权（grant）**：在角色基线之上，可按 `doc_type` / `doc` / `repo` 授予额外 `read`/`write`/`review`/`admin`；**grant 只能叠加，不能超过角色上限**（防越权提升）。判定式：

```
authorize(user, perm, target) := role_permits(user.role, perm)
                                  OR exists(grant where grant.user==user AND grant.perm==perm AND grant.scope matches target)
```

## 后果

**正面**：
- 身份源单一，无密码体系，无额外 PKI 依赖；
- 每个写入可精确归属到人类用户（满足 A2「通过启动 agent 的人类用户鉴定」）；
- agent 侧无状态（签名），WebUI 侧有会话（体验），各取所需；
- 规模上支持 10k 身份（`users` 表 + 索引，无性能压力）。

**负面 / 代价**：
- **CLI 必须实现签名**（新增 M10 client 代码）；非本系统 agent 需集成签名逻辑；
- 每请求多一次验签 + 一次 PG 查询（预算 P95 <10ms，已列指标）；
- **B6 假设作废**：§5 部署需从「绑 127.0.0.1 无鉴权」改为「可对外监听 + 全端点鉴权」；
- WebUI 登录体验不如密码（需 CLI 辅助），已在 §2 给出降级路径。

**中立**：
- `X-Actor` 头从「自由文本」改为「必须与验签身份一致」（安全收紧，写端点已如此，现扩展至读端点）。

## 备选方案与否决理由

| 方案 | 否决理由 |
|---|---|
| 密码 + bcrypt | 引入第二身份源，与「SSH 公钥鉴定」批注不符；需密码策略/重置流程 |
| OIDC / 企业 SSO | 单机私有部署引入外部依赖；离线不可用 |
| API Token（一次性用公钥换 token） | token 泄露即可冒充，且与「每次用公钥鉴定」字面不符（用户已确认全体端点需 SSH 签名） |
| 仅 agent 需鉴权，WebUI 内网无名 | 被用户明确否决（要求 WebUI 登录也鉴权 + 管理员账号） |
| fail-open（无 users 表则放行） | 部署疏忽即裸奔，与 P1/P2 的严谨性不符 |

## 相关

- `architecture_specification.md` §3 M10、§4.1 DDL、§9.1 鉴权模型
- `ADR-002`（纯 PG 存储，本 ADR 复用其连接与角色体系）
- `functional_specification.md` REQ-M10-F01..F05
- `clarifications.md` B6（**已作废并替换**）
