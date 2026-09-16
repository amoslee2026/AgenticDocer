## 补充证据与假设修正（2026-09-16 追加）

### 1. 撤回「凭据待澄清」假设 —— 404 与鉴权完全无关

原文末尾列的第 2 条待澄清项（`$$CREDENTIAL_...$$` 占位符运行时可还原性）**已证伪**，结论如下。

两个网关**都把字面占位符当作有效 key**：

| 请求 | 结果 |
| --- | --- |
| 无 Authorization | **401** |
| `Bearer sk-totally-fake-key-123456` | **401** |
| `Bearer x` | **401** |
| `Bearer sk-VL2YJxqhDWajP8l6w9walnj0pf2Vr3up1Pz8gSkVnaspEMFq`（字面） | **200** |
| `Bearer <真实 key 来自 ~/.pi/agent/auth.json>` | **200** |

4000 网关同样表现，且两种 key 返回**完全相同的 21 个模型组**：

```
$ curl -H 'Authorization: Bearer sk-965483903bdca7f8d9c06b74d0b967713c1925429acf90a3' http://10.147.19.15:4000/v1/models
→ 200, 21 个 model id

$ curl -H "Authorization: Bearer <真实 key>" http://10.147.19.15:4000/v1/models
→ 200, 21 个 model id   (集合逐项相同)

任取第三个假 key → 401
```

**结论**：`$$CREDENTIAL_<HASH>:<CASE>$$` 形态的字符串本身就是注册在网关侧的 literal token
（即 omp 直接把 `models.yml` 里那串字符当 key 发出，网关认。**不是** omp 做了还原）。
因此 404 与鉴权链、与 secret 混淆层**均无关**，纯粹是模型组解析/上游可用性问题。
原假设「占位符可能无法还原」作废。

### 2. `/v1/models` 列表与可调用性脱节（新证据）

同一把 key 横向测试 4000 网关：

| 请求的 model | 结果 |
| --- | --- |
| `local` | **200 OK**（0.81s，内容 `ok`） |
| `free` | **200 OK** |
| `local/DeepSeek-v4-Flash-8081` | **400** `Invalid model name passed in model=...` |
| `local/DeepSeek-v4-Flash-0731` | **404 page not found** + `No fallback model group found` |

即：`/v1/models` **列出的** `local/DeepSeek-v4-Flash-0731` 与 `local/DeepSeek-v4-Flash-8081`
**两个都不可调用**（404 / 400），列表内容不代表可用性。
而列表里那个不起眼的裸 `local` 恰恰是唯一可用的。

→ 强化原结论：**坏的是 `local/DeepSeek-v4-Flash-*` 这组下游，`local` 是好的。**

### 3. 方案 A 的实证补强

直连旁路（`newapi` provider → `172.17.220.2:8080`）端到端复测通过：

```
$ omp -p "只回复：PLACEHOLDER-RESOLVED" --model newapi/DeepSeek-v4-Flash-0731
Working...
PLACEHOLDER-RESOLVED          (18.45s 含启动，推理本身 ~0.32s)
```

且对上游 `172.17.220.2:8080` 的 `chat/completions` 做 key 形态三态对照
（无 key=401 / 字面占位符=200 / 真实 key=200）—— 与 4000 网关同构，
说明两侧网关共享同一套 token 校验语义。

### 4. 更新后的修复建议

方案 A / B 均不受本节影响，仍成立。补充一点：

- 由于**两网关都认字面占位符**，改 `config.yml` 角色绑定时**无需**同步触碰任何凭据字段，
  改动面可压缩到纯角色切换 + `reasoning` 声明两条。

### 附：完整取证命令（可复现）

```bash
# 网关模型组清单
curl -H 'Authorization: Bearer sk-965483903bdca7f8d9c06b74d0b967713c1925429acf90a3' http://10.147.19.15:4000/v1/models

# 组可用性横测
for m in local free local/DeepSeek-v4-Flash-0731 local/DeepSeek-v4-Flash-8081; do
  curl -s -o /dev/null -w "$m -> %{http_code}\n" \
    -H 'Authorization: Bearer sk-965483903bdca7f8d9c06b74d0b967713c1925429acf90a3' \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"$m\",\"messages\":[{\"role\":\"user\",\"content\":\"ok?\"}],\"max_tokens\":5}" \
    http://10.147.19.15:4000/v1/chat/completions
done

# 上游直连
curl -H "Authorization: Bearer <newapi key>" \
     -d '{"model":"DeepSeek-v4-Flash-0731",...}' \
     http://172.17.220.2:8080/v1/chat/completions
```
