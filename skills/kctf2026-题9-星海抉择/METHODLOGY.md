# 通用方法论：AI 模型逆向（无 embedding 语言模型 → 线性规划）

> 适用题型：给一个训练好的小模型（safetensors/pytorch），flag 藏在权重里，需要把"模型行为约束"转化为数学规划问题求解。典型特征：无 embedding 层的字符级 LM、参数量小（如 1765）、flag 与 lm_head 某行/某些线性不等式相关。

## 一、题型识别特征

- 给模型文件（model.safetensors + config.json + model_def.py + inference.py）。
- 模型无 embedding 层（字符级/one-hot 直接进 transformer/线性层）。
- 参数量小（几千以内），可全量读入内存分析。
- 题目暗示"flag 是某输入使模型输出特定 token"或"flag 满足某些线性约束"。
- lm_head（输出投影）某行与 flag 直接相关（如第 62 行）。

## 二、通用推导流程（5 步）

### 第 1 步：模型结构还原
- 读 config.json + model_def.py，确认层数、隐藏维度、有无 embedding。
- 用 safetensors/torch 加载所有权重，列出每层的 shape。
- 无 embedding 时，输入通常是 one-hot 或字符 id 直接进第一层。

### 第 2 步：定位 flag 藏匿点
- 跑 inference.py，观察 argmax 输出与输入的关系。
- 若 flag 是"使 argmax = 特定 id（如 62）的输入"：分析 lm_head 第 62 行。
- 若 flag 满足线性不等式：找出约束对应的权重矩阵行。

### 第 3 步：转化为数学规划
- argmax 约束：`for all j != target: (lm_head[target] - lm_head[j]) · h > 0`，其中 h 是最后一层隐藏态。
- 若 h 本身是输入的线性函数（无激活或激活可分段线性化）：整个问题是线性不等式组。
- 变量 = 输入字符的 one-hot/embedding，约束 = 上述不等式 + flag 格式约束（如可打印字符）。

### 第 4 步：求解
- 线性规划：用 scipy.optimize.linprog / PuLP / z3。
- 若约束是等式且超定：最小二乘（numpy.linalg.lstsq）。
- 若含整数约束（字符 id 是整数）：用 z3 Int 或 OR-Tools CP-SAT。

### 第 5 步：验证
- 把解代入模型前向跑一遍，确认 argmax 命中目标 id。
- 检查解符合 flag 格式（如 flag{...}）。

## 三、验证清单

- [ ] 模型结构完全还原，每层权重 shape 明确。
- [ ] flag 藏匿点（lm_head 行/约束矩阵）定位准确。
- [ ] argmax 约束正确展开为线性不等式。
- [ ] 求解器返回的解代入模型前向验证通过。
- [ ] 解符合 flag 格式。

## 四、常见坑

| 坑 | 表现 | 规避 |
|---|---|---|
| 忽略激活函数 | 约束非线性，LP 求解失败 | 确认激活（ReLU 可分段线性化，GELU 需近似） |
| one-hot 当连续变量 | 解出非整数 id | 加整数约束或枚举 |
| lm_head 行号数错 | 约束建错 | 从 0 开始数，与 inference 输出对齐 |
| 隐藏态不是输入线性函数 | 无法直接 LP | 逐层展开，确认每层都是线性/可线性化 |
| 最小二乘当精确解 | 残差大 | 超定等式用 lstsq，不等式用 LP/SMT |
