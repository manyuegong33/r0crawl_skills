# KCTF 2026 通用方法论索引

> 目标：遇到同类型题目时，按"识别特征 → 推导流程 → 验证清单 → 常见坑"四步走，不依赖具体答案。
> 每个方法论都是通用模板，常量/地址/密钥都需在新题中重新提取。

## 题型 → 方法论速查表

| 题型关键词 | 识别特征 | 方法论文件 | 核心思路 |
|---|---|---|---|
| 反AI/状态机/diagnostic record | 定长输入、多份 worker 记录、error bitmap 不短路 | [kctf-antiai-state-machine/METHODLOGY.md](../skills/kctf-antiai-state-machine/METHODLOGY.md) | 固定可观测事实 → 还原内部状态来源 → 固定位约束 → 理解 error 语义 → 模型求解+原程序确认 |
| Heaven's Gate/VEH VM/魔改AES/多项式根 | 32位PE藏64位、异常模拟指令、自定义Base64、超长Serial | [kctf2026-题4-车流困城/METHODLOGY.md](../skills/kctf2026-题4-车流困城/METHODLOGY.md) | 确认真实环境 → 恢复外层编码 → 差分逆AES → 多项式整数根 → 正向构造验证 |
| 多层校验链/XOR/校验和/RSA部分覆盖 | 单输入多层独立校验、各层覆盖不同区段 | [kctf2026-题5-忆海倒带/METHODLOGY.md](../skills/kctf2026-题5-忆海倒带/METHODLOGY.md) | 画覆盖图 → 分段逆推非RSA区 → 处理RSA区 → 拼接一致性检查 → 原程序验证 |
| Android JNI/奇偶通道/XOF/ARX/SAT/TEA | APK+so、输入按奇偶拆路、自定义section、SAT约束 | [kctf2026-题6-书院迷局/METHODLOGY.md](../skills/kctf2026-题6-书院迷局/METHODLOGY.md) | JNI边界 → 通道拆分 → section密钥 → XOF/ARX逆推 → SAT求解 → TEA/LCG密钥恢复 |
| 自定义块编码/nibble变换/位置重排 | 固定骨架、周期变换、分块重排、已知明文 | [kctf2026-题7-暗能潜流/METHODLOGY.md](../skills/kctf2026-题7-暗能潜流/METHODLOGY.md) | 定块结构找骨架 → 定分块 → 定密钥/变换 → 定位置重排 → 定尾块（配套 derive_solver.py 通用推导工具） |
| 多级SMC/反调试/Feistel/大域求根 | 导入表极少、VirtualProtect、自定义section、软断点污染密钥流 | [kctf-windows-smc-chain/METHODLOGY.md](../skills/kctf-windows-smc-chain/METHODLOGY.md) | 静态SMC还原 → 反调试过检 → Base-N解码 → Feistel逆推 → 大域多项式求根 |
| AI模型/无embedding/线性规划 | safetensors模型、无embedding层、flag藏lm_head行 | [kctf2026-题9-星海抉择/METHODLOGY.md](../skills/kctf2026-题9-星海抉择/METHODLOGY.md) | 模型结构还原 → 定位flag藏匿点 → 转线性规划 → 求解 → 前向验证 |
| NaN-boxing/类型混淆/tcache投毒 | REPL解释器、NaN装箱、BinOp截断、libc 2.27 | [kctf2026-题10-曦光初现/METHODLOGY.md](../skills/kctf2026-题10-曦光初现/METHODLOGY.md) | NaN-boxing还原 → 类型混淆原语 → 任意堆读写 → tcache fd投毒 → __free_hook劫持 |

## 通用解题元方法论（跨题型）

无论哪种题型，都遵循以下元流程：

### 1. 识别阶段（看到什么特征）
- 列出程序的"反常点"：导入表异常、自定义 section、异常指令、定长输入、多份状态记录等。
- 对照上表"识别特征"列，命中 3 条以上即可归类。

### 2. 分解阶段（拆成独立子问题）
- 把程序拆成"外层编码 → 中间变换 → 核心校验"三层。
- 每层独立逆推，避免交叉污染。
- 画"数据流图"：输入 → 各中间态 → 最终校验。

### 3. 逆推阶段（每层用对应工具）
- 编码层：字符表/字节序/位置相关变换。
- 变换层：可逆算子（XOR/ROL/Add）逐个逆；Feistel 用性质逆；AES 差分恢复。
- 校验层：XOR/校验和直接逆；RSA 看覆盖率与 e 大小；SAT/SMT 翻译约束；大域求根用 Sage/pari。

### 4. 验证阶段（三层验证）
- 单步自洽：每个逆操作在已知样本上验证。
- 整体一致：拼接后所有约束同时满足。
- 原程序确认：候选输入在未 patch、无调试器、白名单环境下跑通。

### 5. 避坑阶段（对照常见坑表）
- 每个方法论都有"常见坑"表，解题时逐条对照。

## 工具速查

| 场景 | 工具 |
|---|---|
| 静态 SMC 解密 | pefile + capstone 脚本 |
| 反调试过检 | Unicorn/Qiling 仿真、ScyllaHide |
| AES 差分恢复 | 异常上下文 CONTEXT 只读采样 |
| SAT/SMT 求解 | z3、bitwuzla、cvc5 |
| 大域多项式求根 | SageMath、Magma、pari-gp |
| 线性规划 | scipy.linprog、PuLP、OR-Tools |
| 种子爆破 | CUDA/OpenCL 并行 |
| 通用块编码推导 | derive_solver.py（题7配套，可改参数复用） |

## 使用建议

1. 遇到新题先查本索引，按"识别特征"归类。
2. 打开对应 METHODLOGY.md，按"推导流程"逐步执行。
3. 每步完成对照"验证清单"打勾。
4. 卡住时对照"常见坑"表排查。
5. 题7的 derive_solver.py 是通用推导工具模板，改 SAMPLES/BLOCK_SIZE/PLAIN_CHUNK 参数即可复用到其它块编码题。
