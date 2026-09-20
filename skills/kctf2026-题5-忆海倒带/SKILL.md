---
name: kctf2026-题5-忆海倒带
description: KCTF 2026 第五题 Windows CrackMe 逆向：88-hex 输入、44 字节大数、XOR/checksum/RSA/lookup 四重校验，利用 RSA 只覆盖后 16 字节的特性分段逆推。
---

# 题目摘要

目标文件为 32 位 Windows PE（`cm.exe`），无壳。输入为 88 个十六进制字符，解析为 44 字节大端序大数。程序通过四道独立校验后输出 `verify success.`。

## 可验证常量

- 输入长度：88 hex chars = 44 bytes
- 目标字符串：`Welcome to KCTF2026! Come and give it a try.`（44 字符）
- XOR 校验：44 字节异或和 = `0x8F`
- Checksum 校验：带置换的 checksum = `0xBEFF`
- RSA 覆盖范围：仅 `ArgList[28..43]`（后 16 字节）
- RSA 方向：程序计算 `m = c^e mod N`（用公钥指数 e 处理输入）
- 最终 Serial：`323C47184B0D3C44254B445842552F365C362C1144424B0D3C4416433B0DD6B12A0D3D95FA65B5E0ADE5E11B`

## 标准解法流程

1. **静态分析确认四重校验结构**
   - 读取 88 hex → 44 字节大端序 `ArgList`
   - 关卡 A：`xor_all(ArgList, 44) == 0x8F`
   - 关卡 B：`transform(ArgList, tmp); checksum(tmp) == 0xBEFF`
   - 关卡 C：`rsa(ArgList+28, ArgList+28)`（仅覆盖后 16 字节）
   - 关卡 D：`out_str[i] = lookup_table[ArgList[i]]; strcmp(out_str, "Welcome...") == 0`

2. **Frida 动态确认关键细节**
   - 字节序：hook 主校验函数入口，确认 `ArgList` 为大端序
   - RSA 方向：hook RSA 函数，用两组不同输入捕获 `(c, m)` 对，验证 `pow(c, e, N) == m`
   - lookup 表：hook lookup 函数，遍历 0..255 得到完整 256 字节映射表
   - RSA 覆盖范围：hook RSA 函数，确认仅 `ArgList[28..43]` 被修改

3. **分段逆推**
   - 前 28 字节：直接由 lookup 表反查目标字符串得到 `required[0..27]`
   - 后 16 字节：计算 `m_required = int.from_bytes(required[28:44], 'big')`，然后 `c = pow(m_required, d, N)`，其中 `d` 为 RSA 私钥（N 为 128-bit，p/q 在常量区可直接分解）
   - 拼接：`key = (required[0:28] + c.to_bytes(16, 'big')).hex().upper()`

4. **验证 XOR/checksum 约束**
   - 由于 RSA 段有 16 字节自由度，且 p/q 为出题人选定，正确解恰好满足 XOR 和 checksum
   - 若约束不满足，需在 16 字节自由度内调整

5. **最终验证**
   - 必须在原始未修改的 binary 上验证，动态调试过程中 patch 过的 binary 输出不可信

## 可复用检查清单

- [ ] 识别多关卡独立校验结构，确定各关卡覆盖的数据范围
- [ ] 用 Frida 动态确认字节序、RSA 方向、lookup 表、覆盖范围
- [ ] 利用 RSA 只覆盖部分数据的特性分段逆推
- [ ] 检查逆推结果是否满足所有前置约束（XOR、checksum）
- [ ] 在原始 binary 上最终验证，不依赖 patch 后的环境
