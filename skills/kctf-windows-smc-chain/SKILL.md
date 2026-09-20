---
name: kctf-windows-smc-chain
description: KCTF 2026 第八题“亥子合辰·塔影迷楼”两级 SMC、反调试、Feistel 与 GF(2^127-39) 多项式求根的可复用解题流程。
---

# 题型与结论

目标文件为 PE32+ x64。入口并不直接执行 checker，而是在内存镜像上完成两级运行时解密；解密后的 checker 把 16 个可打印字符编码为有限域元素，经过五次多项式和两路 20 轮 Feistel，逆向后在有限域求根。最终输入/Flag：

```text
kanxue@2o26o8!@#
```

## 1. 从 PE 中静态还原 SMC

`.tgt` 给出参数：`stage1_rva=0x1800`、`stage1_len=0x510`，`stage2_rva=0x1d10`、`stage2_len=0x4962`。可用 section 映射的 `bytearray`，不必修复导入表。

Stage 1：对 `img[0x1800:0x1d10]` 每字节 XOR `0x5a`。

对 Stage 1 明文计算两组 FNV-1a：

```python
MASK=(1<<64)-1; PRIME=0x100000001b3
h1=0xcbf29ce484222325; h2=0x9e3779b97f4a7c15
for b in stage1:
    h1=((h1^b)*PRIME)&MASK
    h2=((h2^b)*PRIME)&MASK
```

本样本结果：`h1=0x73fb4f498aab364f`，`h2=0xb157c7e044b966df`。

Stage 2 每字节：

```python
G=0x9e3779b97f4a7c15; C=0xff51afd7ed558ccd
for i in range(0x4962):
    t=((i*G)&MASK)^h1^h2
    t=(t^(t>>33))*C & MASK
    img[0x1d10+i] ^= t>>56
```

得到有效 x64 checker（约 `0x140004380`）。动态下软件断点可能破坏第二阶段密钥流；优先离线解密或用 Unicorn 模拟。

## 2. Checker 逆向

输入约束：长度 16、ASCII 33..126，且 `sum(input)==0x500`。Base-94 Horner 编码：

```python
N=0
for b in inp: N=(N*94 + b-0x21) % P
P=(1<<127)-39
```

运行时常量由 Stage 2 两个 hash 派生；两路 Feistel 各 20 轮。实现逆轮时按相反顺序恢复 `(L,R)`，并确认两路逆推结果相同。文章给出的公共目标：

```text
Y = 0x4be831b0ad3a2d361489375bba3fb8de
```

于是构造：

```text
f(X)=X^5+FE0*X^4+FE1*X^3+FE2*X^2+FE3*X+(FE4-Y) mod P
```

在 GF(P) 上计算 `gcd(f, x^P-x)`，再用 Cantor–Zassenhaus（或五次小多项式的随机 gcd 切分）求一次因式。根连续 `%94` 展开，逐字节 `+0x21`，检查长度/可打印性/ASCII 和。

## 3. 反调试处理

checker 汇总 PEB.BeingDebugged、NtGlobalFlag、硬件断点、ProcessDebugPort/Object 及多次 `rdtsc` 差值并混入 PRNG；调试器会导致常量/S-box 脏化。离线解密无需处理；若必须动态执行，应 hook `rdtsc`、syscall，并令累加器 `rbx=0`，Class `0x1e` 返回 `STATUS_PORT_NOT_SET` 且 buffer=0。

## 验证清单

- 两阶段解密长度和 RVA 正确；Stage2 开头应为正常 x64 序言。
- 两路 Feistel 逆推出的 `Y` 完全一致。
- 根 `<94^16`，还原字符串全为可打印字符且 ASCII 和为 `0x500`。
- 原始 EXE 运行时输入 `kanxue@2o26o8!@#` 通过。

