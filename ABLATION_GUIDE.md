# 消融实验 (Ablation Study) 使用指南

## 什么是消融实验？

消融实验是机器学习中常用的方法，用于测试模型中每个组件的贡献度。通过系统性地移除或禁用某个组件，观察性能变化，从而理解该组件的重要性。

在本项目中，我们通过**将权重设为0**来"移除"某个适应度函数，测试其对生成音乐质量的影响。

---

## 📋 实验设计

### 当前配置

所有权重已设为 **0.0**（在 `config.py` 中）：

```python
RHYTHM_WEIGHTS = {
    'basic': 0.0,        # 基础平衡性
    'legato': 0.0,       # 连贯性
    'balanced': 0.0,     # 避免极端
}

PITCH_WEIGHTS = {
    'stepwise': 0.0,     # 级进为主
    'arch': 0.0,         # 拱形轮廓
    'end_tonic': 0.0,    # 结束在主音
}
```

### 实验方案

我们提供了 **3种方式** 进行消融实验：

---

## 🔬 方法1: 完整消融实验（推荐用于论文/研究）

运行完整的8个实验，系统性测试每个函数：

```bash
python ablation_study.py
```

### 实验内容

| 实验编号 | 实验名称 | 启用函数 | 输出文件 |
|---------|---------|---------|----------|
| 1 | 基线 | 无（全0） | `ablation_01_baseline_all_zero.mid` |
| 2 | 节奏-basic | rhythm_basic | `ablation_02_rhythm_only_basic.mid` |
| 3 | 节奏-legato | rhythm_legato | `ablation_03_rhythm_only_legato.mid` |
| 4 | 节奏-balanced | rhythm_balanced | `ablation_04_rhythm_only_balanced.mid` |
| 5 | 音高-stepwise | pitch_stepwise | `ablation_05_pitch_only_stepwise.mid` |
| 6 | 音高-arch | pitch_arch | `ablation_06_pitch_only_arch.mid` |
| 7 | 音高-end_tonic | pitch_end_tonic | `ablation_07_pitch_only_end_tonic.mid` |
| 8 | 完整组合 | 全部启用 | `ablation_08_full_combination.mid` |

### 预期结果

- **实验1（基线）**: 完全随机的音乐，没有方向性
- **实验2-4**: 只有节奏结构，音高随机
- **实验5-7**: 只有音高结构，节奏随机
- **实验8**: 最优质的音乐

### 分析方法

播放并对比所有生成的MIDI文件：

```bash
python playmid.py
```

观察：
- 哪个单独函数的效果最明显？
- 节奏vs音高，哪个对音乐质量影响更大？
- 完整组合是否显著优于单个函数？

---

## ⚡ 方法2: 快速交互式测试

适合快速试验和调试：

```bash
python quick_ablation.py
```

### 功能

1. **测试单个节奏函数** - 快速启用某个节奏函数
2. **测试单个音高函数** - 快速启用某个音高函数
3. **测试组合** - 同时启用一个节奏+一个音高函数
4. **恢复默认权重** - 重置到推荐配置
5. **查看当前权重** - 显示当前配置
6. **运行主程序** - 用当前配置生成音乐

### 示例操作流程

```
1. 运行 python quick_ablation.py
2. 选择 "1" (测试单个节奏函数)
3. 选择 "2" (测试legato)
4. 设置权重 1.0
5. 选择 "6" (运行主程序)
6. 生成音乐并播放
```

---

## 🛠️ 方法3: 手动编辑配置

直接编辑 `config.py` 进行精确控制：

### 示例1: 只测试 stepwise 函数

```python
RHYTHM_WEIGHTS = {
    'basic': 0.0,
    'legato': 0.0,
    'balanced': 0.0,
}

PITCH_WEIGHTS = {
    'stepwise': 2.0,     # 只启用这个
    'arch': 0.0,
    'end_tonic': 0.0,
}
```

然后运行：
```bash
python main.py
```

### 示例2: 测试节奏+音高各一个

```python
RHYTHM_WEIGHTS = {
    'basic': 1.5,        # 启用
    'legato': 0.0,
    'balanced': 0.0,
}

PITCH_WEIGHTS = {
    'stepwise': 0.0,
    'arch': 1.5,         # 启用
    'end_tonic': 0.0,
}
```

### 示例3: 测试不同权重比例

```python
RHYTHM_WEIGHTS = {
    'basic': 1.0,        # 相同权重
    'legato': 1.0,       # 相同权重
    'balanced': 0.0,
}

PITCH_WEIGHTS = {
    'stepwise': 3.0,     # 强调级进
    'arch': 0.5,         # 轻微拱形
    'end_tonic': 0.5,    # 轻微终止
}
```

---

## 📊 辅助工具函数

在 `config.py` 中提供了便捷函数：

### 启用单个函数

```python
from config import enable_single_rhythm_function, enable_single_pitch_function

# 只启用一个节奏函数
enable_single_rhythm_function('basic', weight=1.0)

# 只启用一个音高函数
enable_single_pitch_function('stepwise', weight=2.0)
```

### 恢复默认配置

```python
from config import reset_to_default_weights

reset_to_default_weights()
```

---

## 🎯 研究问题示例

消融实验可以回答以下问题：

### 问题1: 哪个函数最重要？

**实验**：分别测试每个函数的单独效果
**方法**：比较实验2-7的音乐质量
**指标**：主观评价（流畅度、结构性、完整感）

### 问题2: 节奏vs音高，谁更重要？

**实验**：
- 实验A：启用所有节奏，禁用所有音高
- 实验B：禁用所有节奏，启用所有音高

**方法**：
```python
# 实验A
RHYTHM_WEIGHTS = {'basic': 1.0, 'legato': 1.0, 'balanced': 1.0}
PITCH_WEIGHTS = {'stepwise': 0.0, 'arch': 0.0, 'end_tonic': 0.0}

# 实验B
RHYTHM_WEIGHTS = {'basic': 0.0, 'legato': 0.0, 'balanced': 0.0}
PITCH_WEIGHTS = {'stepwise': 2.0, 'arch': 1.5, 'end_tonic': 1.5}
```

### 问题3: 权重敏感性分析

**实验**：测试不同权重值的影响
```python
for weight in [0.5, 1.0, 2.0, 4.0]:
    PITCH_WEIGHTS['stepwise'] = weight
    # 运行并生成音乐
```

### 问题4: 最小有效组合

**实验**：找出最少的函数组合仍能生成好听的音乐

例如：
- 只用 `basic + stepwise`
- 只用 `legato + arch`
- 只用 `balanced + end_tonic`

---

## 📈 评估指标

### 定量指标（可计算）

1. **适应度分数** - 记录每个实验的最终分数
2. **音符数量** - 生成的音符数量
3. **音域范围** - max(pitch) - min(pitch)
4. **节奏多样性** - unique rhythm patterns

### 定性指标（主观评价）

1. **流畅度** (1-5分) - 旋律是否流畅
2. **结构性** (1-5分) - 是否有明确结构
3. **完整感** (1-5分) - 是否感觉完整
4. **音乐性** (1-5分) - 整体音乐质量

---

## 📁 输出文件组织

```
results/
├── ablation_01_baseline_all_zero.mid
├── ablation_02_rhythm_only_basic.mid
├── ablation_03_rhythm_only_legato.mid
├── ablation_04_rhythm_only_balanced.mid
├── ablation_05_pitch_only_stepwise.mid
├── ablation_06_pitch_only_arch.mid
├── ablation_07_pitch_only_end_tonic.mid
└── ablation_08_full_combination.mid
```

---

## 🔄 恢复正常使用

完成消融实验后，恢复默认配置：

### 方法1: 使用函数
```python
from config import reset_to_default_weights
reset_to_default_weights()
```

### 方法2: 手动编辑 config.py
```python
RHYTHM_WEIGHTS = {
    'basic': 1.5,
    'legato': 1.2,
    'balanced': 1.0,
}

PITCH_WEIGHTS = {
    'stepwise': 2.0,
    'arch': 1.5,
    'end_tonic': 1.5,
}
```

---

## 💡 提示

1. **每次实验生成独立文件** - 便于对比
2. **记录实验参数** - 在文件名中体现配置
3. **多次运行** - 遗传算法有随机性，建议每个配置运行3次
4. **盲测** - 让他人在不知道配置的情况下评价音乐质量

---

## 📚 相关论文参考

消融实验是论文中常见的分析方法，可参考：

- "Ablation Studies in Artificial Neural Networks" 
- "Understanding Black-box Predictions via Influence Functions"

在音乐生成领域，消融实验可以帮助理解：
- 哪些音乐理论规则最重要
- 不同维度（节奏、音高）的相对重要性
- 最小有效配置

---

*生成日期: 2024*  
*项目: 音乐与数学 - 遗传算法音乐生成系统*

