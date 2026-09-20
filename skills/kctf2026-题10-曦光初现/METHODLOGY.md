# 通用方法论：NaN-boxing 解释器 Pwn（类型混淆 → tcache 投毒 → hook 劫持）

> 适用题型：自研解释器/VM 用 NaN-boxing 表示值，某运算（如 BinOp）位数截断导致类型混淆，可伪造对象头实现任意堆读写，最终 tcache fd 投毒劫持 __free_hook。典型特征：REPL 式交互、值用 64-bit NaN 装箱、对象头含长度字段、libc 2.27（tcache 无 safe-linking）。

## 一、题型识别特征

- 程序是 REPL/解释器，值用 NaN-boxing（64-bit 双精度的 NaN 空间装箱整数/指针/对象）。
- 某二元运算（BinOp）结果未做 48 位截断/掩码 → 可构造出"看起来是对象指针"的值。
- 对象头格式：高 16 位 tag（如 0xBEEF<<48）+ 低 48 位长度/指针。
- libc 2.27（tcache 无双向链表保护、无 safe-linking）。
- 有 __free_hook / __malloc_hook 可劫持。

## 二、通用推导流程（6 步）

### 第 1 步：NaN-boxing 编码还原
- 确认各类型的 NaN-boxing 编码：double、int、pointer、object 各自的 tag 位。
- 写出 encode/decode 函数，确认 BinOp 的截断行为。

### 第 2 步：找到类型混淆原语
- 确认哪个运算（如 BinOp）不做 48 位掩码 → 可构造任意 64-bit 值被当作对象指针。
- 伪造对象头：`0xBEEF<<48 | length`，指向可控堆区域。

### 第 3 步：任意堆读写
- 用伪造对象实现前向任意读（读对象字段）。
- 用 1-bit oracle（如三态比较）逐位泄露地址（堆地址、libc 地址）。
- 确认泄露精度与速度平衡。

### 第 4 步：tcache fd 投毒
- libc 2.27 tcache：单链表、fd 存明文、无 safe-linking。
- 用任意写改 tcache entry 的 fd 为目标地址（如 __free_hook-8）。
- 注意 tcache 计数与大小类（如 0x20）。

### 第 5 步：劫持 __free_hook
- 分配两次拿到 __free_hook 处的 chunk。
- 写入 system 地址。
- 注意 SSO（小字符串优化）：15 字符以内字符串可能不走堆，需 2-pop 等技巧绕过。

### 第 6 步：触发 getshell
- free 一个内容为 "/bin/sh" 的 chunk → __free_hook("/bin/sh") → system("/bin/sh")。
- 注意触发分配的大小（如 0x30）要避开 SSO。

## 三、验证清单

- [ ] NaN-boxing 编码/解码在已知值上自洽。
- [ ] 类型混淆原语可稳定构造伪造对象。
- [ ] 任意读泄露的地址与 /proc/pid/maps 一致。
- [ ] tcache fd 投毒后分配落在目标地址。
- [ ] __free_hook 写入 system 后 free("/bin/sh")  getshell。

## 四、常见坑

| 坑 | 表现 | 规避 |
|---|---|---|
| BinOp 截断位数记错 | 伪造对象 tag 不对 | 从反汇编确认掩码宽度（48 位） |
| 对象头 tag 错 | 解释器崩溃 | 确认 tag（如 0xBEEF）与长度字段位置 |
| libc 版本误判 | safe-linking 挡住 fd 投毒 | 确认 libc 2.27 无 safe-linking |
| SSO 字符串不走堆 | free 不到目标 | 用 2-pop 或超 15 字符强制堆分配 |
| 触发分配大小错 | 拿不到目标 chunk | 确认 tcache 大小类（0x20/0x30） |
| 1-bit oracle 泄露慢 | 交互超时 | 优化 oracle（三态比较一次泄露 1 bit） |
