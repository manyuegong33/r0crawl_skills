---
name: kctf2026-题9-星海抉择
description: KCTF 2026 第九题 AI 模型逆向：无 embedding 的字符级语言模型，将 flag 藏在 lm_head 第 62 行和线性不等式中，转化为线性规划求解。
---

# 题目摘要

目标为 `ICTFForCausalLM` 模型，仅 1,765 个参数，无 embedding 和 attention。输入为长度 16 的字符串，字符集 62 个，目标是让 `argmax` 落在 id 62（`<success>`）。

## 可验证常量

- 模型结构：16 → 21 → 64
- 参数量：1,765
- 字符集：`0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`
- 最终 flag：`f1ag2026c7fa1666`

## 标准解法流程

1. **模型结构分析**
   - 前向传播仅三行：`x = input_ids.float()` → `hidden = dense(x)` → `logits = lm_head(hidden)`
   - 无 embedding 层，token id 直接当浮点特征
   - 输入 `x ∈ {0,…,61}^16`，目标 `argmax(logits) == 62`

2. **lm_head 结构分析**
   - 64 行中 63 行权重全零，logit 为常数
   - 普通字符（0-61）：logit = -10000
   - `<fail>`（63）：logit = 0.4
   - `<success>`（62）：`logit[62] = h0 - 1e10 * (h1 + ... + h20) - 376131.21875`

3. **转化为线性规划**
   - 条件 A（可行性）：20 个隐藏单元必须被 ReLU 压成 0，即 `W[j]·x + b[j] <= 0`（j=1..20）
   - 条件 B（最优性）：`h0 = W[0]·x + b[0] > 0.4 + 376131.21875 = 376131.61875`

4. **求解**
   - `dense.weight[1:]` 为 20×16 整数矩阵，秩 16
   - 使用最小二乘求解 `A @ x + b == 0`，残差约 1.24e-11
   - 四舍五入到整数：`x = np.round(np.linalg.lstsq(A, -b, rcond=None)[0]).astype(int)`
   - 验证：`np.all(A @ x + b == 0)` 且 `w0 @ x + b0 > bl[63] - bl[62]`

5. **唯一性验证**
   - 条件 A 是 `<= 0` 而非 `= 0`，可行域为 16 维多面体
   - 目标函数系数全为整数且互质，目标值只能落在整数上
   - LP 最优值恰好等于下界 64573，解唯一

6. **映射与验证**
   - 将解 `x` 按字符集映射为字符串
   - 用 float32 精确复现原模型前向验证
   - 直接运行官方 `inference.py` 验证

## 可复用检查清单

- [ ] 识别无 embedding 的模型，token id 直接作为特征
- [ ] 分析 lm_head 结构，找出唯一随输入变化的行
- [ ] 将 argmax 条件转化为线性不等式组
- [ ] 使用最小二乘求解超定方程组
- [ ] 验证解的唯一性（LP 对偶、MILP 可行性测试）
- [ ] 用原始模型精确复现验证
