---
name: kctf2026-题6-书院迷局
description: KCTF 2026 第六题 Android APK 逆向：JNI 混合流程、奇偶通道分离、XOF/ARX 状态机、46 位稀疏布尔门 SAT 求解、TEA/LCG 密钥恢复。
---

# 题目摘要

目标文件为 Android APK（`KCTF2026.apk`）。输入为 100 个小写十六进制字符，Java 层解码为 50 字节后调用 JNI 函数。native 层将输入奇偶解交织为两个 25 字节通道，分别经过不同的变换和校验。

## 可验证常量

- 输入：100 个小写 hex 字符 = 50 字节
- 奇偶分离：`even[i] = input[2*i]`, `odd[i] = input[2*i+1]`
- 16 字节密钥：`870573e5f5c63d52862dbd05ab3d9494`
- 32 字节隐藏目标：`9f73be24a1dd6c96b90723bba7cdfdc9fd521311dd1b172572014429f93dd77c`
- 最终 flag：`a77a7ae3781bff946ad2945636f87d0c1b414eb7b4293f8eaa638da5e2dfb310044b00c8bd72533d3d96e80f55e4345843ad`

## 标准解法流程

1. **Java 层与 JNI 入口分析**
   - 确认输入格式：100 hex chars → 50 bytes
   - 定位 JNI 函数：`nativeProcessInput`
   - 识别 `.init_array` 中的反调试初始化（读取 `/proc/self/status` 的 `TracerPid`）

2. **密钥恢复**
   - Java 层读取自身 APK，解析 ELF 节表，定位 96 字节 `.kctfguard` 节
   - 结合 CRC、节偏移和节大小生成 32 字节数据
   - 与固定向量异或得到 16 字节 native 密钥

3. **去混淆语义**
   - 识别并替换基础函数：`sub_E818(a,b,noise) = a XOR b`、`sub_EE90(a,b) = a + b` 等
   - 删除成对的 `InvMixColumns(MixColumns(x)) = x` 结构
   - 识别 `mix32` 散列函数及其在 SIMD 中的并行计算

4. **Odd 通道：XOF/ARX 状态机**
   - XOF 输入：`odd25 || 5a5a5a5a5a5a5a`（32 字节）
   - 轮函数：基于 `ror64/rol64` 的 ARX 结构，可逆
   - 校验要求 `XOF[80:96]` 等于隐藏目标前 16 字节
   - 通过逆推固定 XOF 初始状态中的 `c` 和 `d`

5. **46 位稀疏布尔门**
   - 每个输出位仅依赖输入 `b` 的 2-5 位
   - 对每个输出位枚举局部真值表，生成 CNF 阻断子句
   - 使用 SAT 求解器（如 Z3）求解，结合 XOF 逆函数筛选有效解

6. **Even 通道：TEA/LCG 状态机**
   - 可逆字节置换和链式状态变换
   - 标准 TEA 常量 `delta = 0x9e3779b9`，16 轮
   - 32 位 LCG 生成轮密钥：`seed = seed * 1664525 + 1013904223`
   - 使用 CUDA 暴力枚举 32 位 seed，通过三组 KAT 验证

7. **合并与验证**
   - 按原输入布局交织两个 share：`flag_bytes = bytes(x for pair in zip(even25, odd25) for x in pair)`
   - 在原始 APK 或提取的样本上验证，不依赖反编译伪代码

## 可复用检查清单

- [ ] 识别 JNI 混合流程，分离 Java 层和 native 层校验
- [ ] 处理奇偶通道分离和独立状态机
- [ ] 对 XOF/ARX 结构进行逆推，利用已知输出约束固定初始状态
- [ ] 对稀疏布尔门使用局部 SAT 求解而非全局约束
- [ ] 对 TEA/LCG 等标准算法使用 GPU 加速暴力枚举
- [ ] 在原始 APK 上验证，不依赖反编译结果
