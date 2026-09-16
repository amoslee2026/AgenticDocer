## 现象

omp 会话中 `smol` / `tiny` / `advisor` 三个模型角色全部失效，报错：

```
404 litellm.NotFoundError: NotFoundError: OpenAIException - 404 page not found
   No fallback model group found for original model_group=local/DeepSeek-v4-Flash-0731.
   Fallbacks=[{'local': ['openai/DeepSeek-V4-Flash']}, ...]
   Available Model Group Fallbacks=None
```

同类第二条（并发证据）：`~/.omp/logs/http-400-requests/1789553346036-1z7dm3ykvjjsw.json`

```
url:    http://10.147.19.15:4000/v1/responses
model:  local/DeepSeek-v4-Flash-0731
api:    openai-responses
status: 400
msg:    400 litellm.BadRequestError: ... 2533 validation errors ...
        No fallback model group found for original model_group=local/DeepSeek-v4-Flash-0731.
        Fallbacks=[{'local': ['openai/DeepSeek-V4-Flash']}, ...]
```

即：**400 与 404 是同一条链路的两个表现**，末尾都落到 `No fallback model group found`。

## 根因

链路实测（本机 TeraFab，2026-09-16）：

```
omp (smol/tiny/advisor = litellm/local)
  └─> LiteLLM 网关 10.147.19.15:4000        [key 有效, /v1/models HTTP 200]
        model_group = local/DeepSeek-v4-Flash-0731
        └─> fallbacks: {'local': ['openai/DeepSeek-V4-Flash']}
              └─> 上游 new-api 172.17.220.2:8080
                    ├─ DeepSeek-v4-Flash-0731  → 可用（0.32s，实测 3/3 成功）
                    └─ DeepSeek-V4-Flash       → HTTP 503
                                                 "No available channel for model
                                                  DeepSeek-V4-Flash under group"
```

**两个独立缺陷叠加**：

1. **LiteLLM 侧 fallback 指向不存在的上游模型名。**
   `/v1/models` 实际列出的是 `DeepSeek-v4-Flash-0731`（小写 `v4`），
   而 fallback 链里写的是 `openai/DeepSeek-V4-Flash`（大写 `V4`，且无 `-0731` 后缀）。
   该名字在上游 8080 无任何可用渠道 ⇒ 503 ⇒ LiteLLM 无组可退 ⇒ 原样抛 404。

2. **omp 发出的 `body.model` 是具体 upstream 名，而非配置里的 `id`。**
   `~/.omp/agent/models.yml` 的 `litellm` provider 定义的是 `id: local`，
   但实际请求体是 `model = local/DeepSeek-v4-Flash-0731`。
   取证：`~/.omp/logs/http-400-requests/1789549094306-5zyz31vo51ig.json` 的 `model` / `body.model` 字段。
   即 omp 未把裸模型组名 `local` 发出去，而是发了一个**下游已失效的具体组**。

## 关键反证

裸 `local` 模型组**完全健康**：

```
$ curl -H "Authorization: Bearer <litellm-key>" \
       -d '{"model":"local","messages":[{"role":"user","content":"say ok"}],"max_tokens":8}' \
       http://10.147.19.15:4000/v1/chat/completions
model_used = local ; content = 'ok'   (0.81s, HTTP 200)
```

对比 `local/DeepSeek-v4-Flash-0731`：HTTP 404。
⇒ **坏的是 `local/DeepSeek-v4-Flash-0731` 这个下游组，`local` 本身是好的。**

## 直连旁路已验证可用

```
$ curl -H "Authorization: Bearer <newapi-key>" \
       -d '{"model":"DeepSeek-v4-Flash-0731",...}' \
       http://172.17.220.2:8080/v1/chat/completions
→ 200 OK, 3/3 成功, ~0.32s, 返回中文内容正确
```

`newapi` provider 已在 `models.yml` 中定义（`baseUrl: http://172.17.220.2:8080/v1`, `id: DeepSeek-v4-Flash-0731`）。

## 建议修复（需在 mySkills/harness/omp 侧落地）

**方案 A（推荐，本机已验证）**：角色切到直连 newapi，绕过 LiteLLM 的失效 fallback 链。

```yaml
# harness/omp/config.yml
modelRoles:
  smol: newapi/DeepSeek-v4-Flash-0731
  tiny: newapi/DeepSeek-v4-Flash-0731
  advisor: newapi/DeepSeek-v4-Flash-0731
retry:
  fallbackChains:
    default:
      - deepseek/deepseek-flash
      - newapi/DeepSeek-v4-Flash-0731
```

配套需补 `newapi` provider 的 reasoning 声明（当前缺失，会丢弃思考）：
实测上游返回字段名是 **`reasoning`**（**不是** `reasoning_content`），
且 `usage.completion_tokens_details.reasoning_tokens = 172 > 0`。

```yaml
# harness/omp/models.yml — newapi provider 下
      - id: DeepSeek-v4-Flash-0731
        reasoning: true                      # ← 新增
        compat:
          maxTokensField: max_tokens
          reasoningContentField: reasoning   # ← 新增（注意不是 reasoning_content）
```

**方案 B（治本）**：修网关侧 LiteLLM 配置（10.147.19.15 上的 `model_list` / fallbacks），
把 `local/DeepSeek-v4-Flash-0731` 的 fallback 目标改成上游真实存在的 `DeepSeek-v4-Flash-0731`，
或直接移除该失效组。

## 待澄清（阻塞本机修复）

1. **omp 为何把 `body.model` 解析为具体 upstream 名而非配置 `id`？**
   若是 omp 的模型解析行为，方案 B 之外还需评估是否属 omp 侧缺陷。
2. `models.yml` 中 `litellm` provider 与 `newapi` provider 的凭据字段是
   `$$CREDENTIAL_<HASH>:<CASE>$$` 形态 —— 该占位符是 omp secret 混淆层产物。
   需确认运行时能否还原为真实 key（本机实测直连网关带真实 key 成功，故占位符应在运行时可解）。

## 环境

- 主机：TeraFab（非 write-guard 只读豁免主机 OO7）
- omp 配置：`~/.omp/agent/{config,models}.yml` → 软链至 `~/wrk/mySkills/harness/omp/`
- 网络：`all_proxy=socks5://172.17.220.111:7898`（GitHub 代理链路当前有瞬断）
