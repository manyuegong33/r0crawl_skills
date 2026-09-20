---
name: kctf2026-题10-曦光初现
description: KCTF 2026 第十题 Linux Pwn：NaN-boxing 解释器、BinOp 48 位截断漏洞、伪造对象头前向任意堆读写、tcache 0x20 fd 投毒、__free_hook 劫持。
---

# 题目摘要

目标为 C++ 编写的 NaN-boxing 玩具解释器（glibc 2.27，PIE / Full RELRO / NX / Canary）。唯一漏洞在 `BinOp` 运算结果不做 48 位截断，可伪造对象头拿到前向任意堆读写，最终通过 tcache 投毒劫持 `__free_hook` 为 `system` 拿 shell。

## 可验证常量

- 环境：glibc 2.27，PIE / Full RELRO / NX / Canary
- 值编码：高 16 位 == `0x1337` → 对象句柄，低 48 位 = arena 内对象头堆地址；否则为 48 位整数
- 对象头：`key ^ (0xBEEF<<48 | nchildren)`
- 数字叶子：`key ^ (val & 0xFFFFFFFFFFFF)`
- 最终 flag：`flag{f2ab8ac8-cd80-4c45-b859-ae6ba9289959}`（每实例轮换）

## 标准解法流程

1. **漏洞定位**
   - `BinOp_eval` 是唯一不给结果做 48 位 mask 的路径
   - 可拼出任意高 16 位：`$1=0x1337; $2=0x1000000; $1=$1*$2; $1=$1*$2` → `env[1] = 0x1337<<48`
   - 伪造对象头：`$k = 0xBEEF<<48 | len`

2. **伪造超长对象头 → 前向任意堆读写**
   - 建真对象 `$0=[0,0]`，用 BinOp 造 `hdr = 0xBEEF<<48 | 0x6000`
   - `SetField` 写入 `$0` 的第 0 个叶子
   - `$0[0][k]` 即可读写 `arena + 16 + 8*k`（k < 0x6000）

3. **信息泄露（1-bit oracle）**
   - 题目无打印功能，通过命令成功/`runtime error!`/`invalid syntax!` 三态逐位读出
   - 方法：`(v>>i)&1` 造成 `0x1337` tag，再让 BinOp 因右操作数是句柄而 `runtime error` → 该位为 1
   - 泄露 key：`$dst=$0[0][1]` 读未初始化槽 → `0 ^ key = key`
   - 泄露 arena/libc：`k=8193`（heap 自指针）、`k=8205`（指向 `_IO_2_1_stderr_` 的 libc 指针）

4. **tcache 0x20 fd 投毒 → `__free_hook = system`**
   - 用 `write1` 把某个 0x20 freed chunk 的 fd 改成 `__free_hook`
   - 攻击命令 `$4=$0[<system 十进制>]`：解析时下标 push 进 `std::vector`，其 8 字节 buffer 从 tcache 0x20 bin 取
   - 若 buffer 落在 `__free_hook`，则 `buffer[0] = 下标 = system`

5. **两个决定性坑**
   - **15 位下标 = 2-pop，不是 3-pop**：libc 地址十进制恒为 15 位，15 字符落在 libstdc++ SSO 边界内，不为下标数字分配临时 string。用 ≥16 位占位大数调试会落进 3-pop 分支，投毒目标算错。
   - **触发行必须是 0x30 分配，不能是 0x20**：攻击把 `__free_hook` 写成 `system` 后，`__free_hook` 位于 0x20 bin 链头。若触发行是 16 字符（0x20 分配），其 `std::string` 会 `malloc` 0x20 chunk，把 `__free_hook` pop 出来当缓冲，用 `/bin/sh` 覆盖掉 `system` → 崩溃。改用 24-39 字符的 0x30 分配行（如 `/bin/sh #` + 22×`A` = 31 字符）。

6. **读旗**
   - 远程极简 chroot 无 `cat`/`id`/`head`/`grep`，只有 `ls` 和 `/bin/sh`
   - 用 dash 内置 `read a < flag; echo "$a"` 读出

## 可复用检查清单

- [ ] 识别 NaN-boxing 值编码和对象句柄结构
- [ ] 定位不做位数截断的运算路径（BinOp）
- [ ] 伪造对象头获取前向任意堆读写
- [ ] 利用三态 oracle（成功/运行时错误/语法错误）逐位泄露信息
- [ ] 注意 SSO 边界对 tcache 分配次数的影响（15 位 = 2-pop）
- [ ] 触发行大小必须避开被投毒的 bin 大小（0x30 vs 0x20）
- [ ] 在极简环境中使用 shell 内置命令读旗
