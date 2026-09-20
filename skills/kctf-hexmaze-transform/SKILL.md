---
name: kctf-hexmaze-transform
description: Solve KCTF byte-transform puzzles with fixed-size blocks, tail handling, and reversible nibble/byte mappings. Use when the challenge behaves like a deterministic encoder/decoder rather than a checker.
---

# KCTF 第七题 HexMaze·暗能潜流

## 核心结论
输入是可打印 ASCII，密钥字符串 `121` 实际选择两种 nibble 变换，数据按右侧 3 字节分块并反转块序。每 3 字节编码为 6 字节（固定半字节骨架），尾块由长度 mod 3 决定。

## Workflow

1. Measure the block size, output expansion, and tail rule.
2. Compare one sample block against one wrong block.
3. Infer the forward transform on the smallest possible chunk.
4. Invert the transform block by block.
5. Replay the original sample before trusting the inverse.

## 逆向算法

从密文每 6-byte 块提取有效半字节位置 `[0.high,1.high,1.low,2.low,4.high,5.high]`，拼成 3 个数据字节。按密钥周期 `1,2,1` 逆变换：

* key=1（加密 `(H,L)->(L+4,H+5)`）：解密 `(a,b)->(H=b-5,L=a-4)`。
* key=2（加密 `(H,L)->(H+5,L+4)`）：解密 `(a,b)->(H=a-5,L=b-4)`。

得到中间串后，按 3 字节块执行左循环（`CAB→ABC`），再反转块序；余 2 字节块先交换，余 1 字节不变。FLAG 例：`flag{T1u_2026_Kc7f_Crypt0_M4ster!}`。

## 验证

使用样例 `TLU→94AA48550495`、`Hello→34BB405504B5223594B94C53` 对提取、逆 nibble、块重排全流程回放；确认尾块格式分别对应 `len mod 3`。

## Use this pattern

- 3-byte to 6-byte or other fixed-ratio expansion
- length-dependent tail handling
- deterministic byte/nibble mapping
- inverse derived from samples, not guesses

## Reference

- `references/pattern.md`
