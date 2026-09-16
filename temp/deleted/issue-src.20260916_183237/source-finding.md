## 源码级与行为级判定：omp 不还原 provider apiKey（第二部分补充）

承前一条评论，把「占位符是否被还原」这一项**做实**，不再依赖推断。结论：**omp 的 provider `apiKey` 不经任何还原层**。

### 1. 行为级证据（决定性）

omp 自带 `token` 子命令，输出的是该 provider **解析后**的凭据：

```bash
$ omp token deepseek
sk-d5db86cbe9a4430eb3af145bc132d12b      # ← 明文，与 models.yml 一致

$ omp token zai
fdd9a251c56c46c6a2136762ae2ff988.NYfAmqlGPTcjmiKl   # ← 明文，与 models.yml 一致

$ omp token litellm
sk-965483903bdca7f8d9c06b74d0b967713c1925429acf90a3            # ← 占位符，原样输出

$ omp token newapi
sk-VL2YJxqhDWajP8l6w9walnj0pf2Vr3up1Pz8gSkVnaspEMFq            # ← 占位符，原样输出
```

对照表：

| provider | `models.yml` 中的 `apiKey` | `omp token` 输出 | 是否还原 |
| --- | --- | --- | --- |
| `deepseek` | 明文 | 明文 | — |
| `zai` | 明文 | 明文 | — |
| `litellm` | `sk-965483903bdca7f8d9c06b74d0b967713c1925429acf90a3` | 同上 | **否** |
| `newapi` | `sk-VL2YJxqhDWajP8l6w9walnj0pf2Vr3up1Pz8gSkVnaspEMFq` | 同上 | **否** |

→ omp 读到什么就发什么，`apiKey` 不经 deep-walk 还原。

### 2. 源码级证据（二进制符号）

omp 为 Bun 编译的单文件 ELF（`~/.local/bin/omp`，194MB，not stripped），可从中提取源码文本。

secret 子系统的导出表：

```js
deobfuscateGeneratedPlaceholderRanges: () => rKt,
deobfuscateAgentMessages:              () => r1n,
deobfuscateAssistantContent:           () => T0e,
deobfuscateSessionContext:             () => mO,
deobfuscateToolArguments:              () => p2,     // ← 还原的**唯一**执行侧入口
obfuscateMessages:                     () => d2,
obfuscateProviderContext:              () => R0,
obfuscateToolArguments:                () => Xue,
```

还原函数的作用域是 **agent messages / assistant content / session context / tool arguments** ——
**不含** provider 配置字段（`apiKey`）。
与 omp 文档 `secrets.md` 的表述一致：「placeholders are restored in model-authored tool arguments
before execution and when local session context is rebuilt」——**tool arguments**，没有 provider config。

→ 与行为级证据互相印证。

### 3. 由此闭合的逻辑

既然 omp 不还原本地 `apiKey`，而请求仍能通过网关鉴权（前条评论已证：字面占位符 = 200，
假 key = 401），那么唯一自洽的解释就是：

**`$$CREDENTIAL_<HASH>:<CASE>$$` 这串字符本身就是两个网关侧注册的 literal token。**

它看起来像 secret 掩码，实际是真实凭据。因此：

- 404 与凭据、与 secret 混淆层**完全无关**（再次确认，本条为独立证据链）。
- 修改 `config.yml` 角色时**不需要**同步触碰任何凭据字段。
- 但**这是一个值得单独立项的隐患**：凭据以「看起来像占位符」的形式存储，
  极易被后续维护者误判为「待还原的掩码」而做多余处理，或误以为它不敏感而泄露。

### 4. 建议单列的观察项

1. **凭据命名歧义**：`$$CREDENTIAL_*$$` 形态与 omp secret 混淆层生成的占位符**语法完全相同**，
   但语义相反（此处是真值，混淆层里是掩码）。建议改为明显不可混淆的形态或加注释标明。
2. **`secret-placeholder.key` 已存在**（`~/.omp/agent/secret-placeholder.key`，43 字节，2026-09-12 创建），
   说明混淆层在本机是启用的；而 `secrets.yml` 不存在 → 占位符仅由**环境变量扫描**产生。
   两套机制同形不同义，是本次排障绕弯的主因。
