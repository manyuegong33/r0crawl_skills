---
name: kctf-9-ictf-linear-model
description: 从无 embedding 的 PyTorch/ safetensors 小型语言模型中恢复 KCTF 第九题 flag；将 argmax 约束转化为整数线性规划并验证输出。
---

# KCTF9：ICTFForCausalLM 线性约束求解

## 适用场景

模型 `forward` 直接把 16 个 token id 转为 float，经过 `Linear(16→21)+ReLU+Linear(21→64)`；`lm_head` 的 success 行带超大负 bias，目标是找出使 token 62 (`<success>`) 成为 argmax 的 16 字符串。

## 蒸馏流程

1. **解析模型文件**：读取 safetensors（8 字节 little-endian header 长度、JSON header、随后 float32 数据），提取 `dense.weight/bias` 与 `lm_head.weight/bias`，无需安装 torch。
2. **识别输出约束**：success 行 logit 形如 `h0 - 1e10·Σ(h1..h20) - 376131.21875`，fail 行恒为 `0.4`。因此可行条件是
   - 对 j=1..20：`W[j]·x + b[j] ≤ 0`（ReLU 后全零）；
   - `W[0]·x+b[0] > 376131.61875`。
3. **先求隐藏层零点**：对 20×16 整数矩阵做最小二乘 `x=lstsq(W[1:],-b[1:])`，四舍五入并验证每个残差为 0；若不满足，使用 `scipy.optimize.milp` 或枚举字符域 `{0..61}` 求解线性不等式。
4. **字符映射**：字符表 `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`，将 16 个整数索引转换字符串；示例解为 `[15,1,10,16,2,0,2,6,12,7,15,10,1,6,6,6] → f1ag2026c7fa1666`。
5. **验证**：重新实现 forward，确认 20 个 ReLU 输出为 0、h0 超过阈值，argmax=62；同时测试 padding id=0 与长度不足输入。

## 常见陷阱

- 不要把模型当作标准 embedding LM；token id 数值本身就是特征。
- `argmax` 必须同时考虑 fail 常数和 success 超大惩罚，不能只看隐藏层零点。
- 浮点残差应检查到原始精度（通常约 1e-5），再转整数并验证字符范围。

