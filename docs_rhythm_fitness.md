# 节奏适应度函数详解

本文档详细介绍所有节奏适应度函数的作用、原理和音乐效果。

---

## 目录

1. [rhythm_fitness_basic](#1-rhythm_fitness_basic---基础平衡节奏)
2. [rhythm_fitness_active](#2-rhythm_fitness_active---活跃密集节奏)
3. [rhythm_fitness_legato](#3-rhythm_fitness_legato---连贯流畅节奏)
4. [rhythm_fitness_syncopated](#4-rhythm_fitness_syncopated---切分音节奏)
5. [rhythm_fitness_balanced](#5-rhythm_fitness_balanced---均衡节奏)
6. [rhythm_fitness_sparse](#6-rhythm_fitness_sparse---稀疏留白节奏)
7. [rhythm_fitness_march](#7-rhythm_fitness_march---进行曲节奏)
8. [rhythm_fitness_varied](#8-rhythm_fitness_varied---多变复杂节奏)
9. [rhythm_fitness_overall](#9-rhythm_fitness_overall---综合节奏推荐)

---

## 1. rhythm_fitness_basic - 基础平衡节奏

### 作用
创建平衡、自然的节奏模式，适合大多数音乐风格。

### 评分规则

```python
# 统计各类型数量
note_count = rhythm.count(1)   # 发声数量
hold_count = rhythm.count(2)   # 延长数量
rest_count = rhythm.count(0)   # 休止数量

# 评分标准
if 4 <= note_count <= 8:   # 4-8个发声 → +50分
if 2 <= rest_count <= 5:   # 2-5个休止 → +30分
if hold_count >= 2:         # 至少2个延长 → +20分
```

### 音乐特征
- ✅ 适度的音符密度（不太密集也不太稀疏）
- ✅ 有呼吸空间（休止符）
- ✅ 音符有长有短（延长记号）

### 适用场景
- 通用音乐风格
- 初学者友好
- 作为基础评分标准

### 示例节奏模式
```
[1, 2, 0, 1, 1, 2, 2, 0, 1, 0, 1, 2, 0, 1, 1, 0]
 发 延 休 发 发 延 延 休 发 休 发 延 休 发 发 休
```
- 发声：6个 ✓
- 休止：4个 ✓
- 延长：4个 ✓

---

## 2. rhythm_fitness_active - 活跃密集节奏

### 作用
生成高能量、密集的节奏，适合快节奏音乐。

### 评分规则

```python
score += note_count * 15         # 每个发声 +15分
score -= rest_count * 10         # 每个休止 -10分（惩罚）

# 奖励连续音符
for i in range(len(rhythm) - 1):
    if rhythm[i] == 1 and rhythm[i+1] == 1:
        score += 5  # 连续发声 +5分
```

### 音乐特征
- ✅ 高密度音符
- ✅ 减少休止符
- ✅ 连续的音符攻击
- ❌ 缺少呼吸感

### 适用场景
- 快速乐曲
- 激昂、激动人心的段落
- 技巧展示

### 示例节奏模式
```
[1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1]
 发 发 发 延 发 发 发 发 延 发 发 发 发 延 发 发
```
- 发声密集（12个）
- 很少休止
- 连续发声多

---

## 3. rhythm_fitness_legato - 连贯流畅节奏

### 作用
创造长音符、连贯的节奏，适合抒情音乐。

### 评分规则

```python
score += hold_count * 20  # 延长记号越多越好

# 计算平均音符长度
avg_length = (note_count + hold_count) / note_count
if avg_length >= 2:  # 平均长度≥2 → +50分

# 惩罚碎片化（音符后不接延长）
for i in range(len(rhythm) - 1):
    if rhythm[i] == 1 and rhythm[i+1] != 2:
        score -= 5
```

### 音乐特征
- ✅ 长音符为主
- ✅ 流畅连贯
- ✅ 减少音符攻击点
- ❌ 可能缺少节奏变化

### 适用场景
- 抒情歌曲
- 慢板乐章
- 圣咏、颂歌

### 示例节奏模式
```
[1, 2, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 2, 0, 1, 2]
 发 延 延 延 休 发 延 延 休 发 延 延 延 休 发 延
```
- 音符很长（多个延长）
- 攻击点少（4个发声）
- 连贯流畅

---

## 4. rhythm_fitness_syncopated - 切分音节奏

### 作用
创造爵士、拉丁风格的切分节奏。

### 评分规则

```python
strong_beats = [0, 4, 8, 12]    # 强拍位置
weak_beats = [1,2,3, 5,6,7, 9,10,11, 13,14,15]  # 弱拍

# 弱拍上有音符（切分）
for pos in weak_beats:
    if rhythm[pos] == 1:
        score += 10

# 强拍上休止（反常规）
for pos in strong_beats:
    if rhythm[pos] == 0:
        score += 15
```

### 音乐特征
- ✅ 强弱拍颠倒
- ✅ 不规则重音
- ✅ 摇摆感
- ❌ 可能不稳定

### 适用场景
- 爵士乐
- 拉丁音乐
- 摇摆舞曲
- 现代流行

### 示例节奏模式
```
位置: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
     [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0]
强拍: ↑        ↑        ↑              ↑
      休       休       休             休
```
- 强拍休止（反常规）
- 弱拍发声（切分）

---

## 5. rhythm_fitness_balanced - 均衡节奏

### 作用
避免极端，创造最自然、平衡的节奏。

### 评分规则

```python
# 理想分布
ideal_notes = 16 * 0.4  # 40% 发声
ideal_holds = 16 * 0.3  # 30% 延长
ideal_rests = 16 * 0.3  # 30% 休止

# 距离理想值越近越好
score -= abs(note_count - ideal_notes) * 5
score -= abs(hold_count - ideal_holds) * 3
score -= abs(rest_count - ideal_rests) * 3

# 奖励交替变化
for i in range(len(rhythm) - 1):
    if rhythm[i] != rhythm[i+1]:
        score += 2
```

### 音乐特征
- ✅ 三种类型均衡分布
- ✅ 频繁变化
- ✅ 自然流畅
- ✅ 无极端情况

### 适用场景
- 古典音乐
- 民谣
- 通用伴奏

### 示例节奏模式
```
[1, 2, 0, 1, 0, 2, 1, 0, 2, 1, 0, 1, 2, 0, 1, 2]
```
- 发声：6个 (37.5%)
- 延长：5个 (31.2%)
- 休止：5个 (31.2%)
- 变化频繁

---

## 6. rhythm_fitness_sparse - 稀疏留白节奏

### 作用
创造留白、呼吸感强的节奏，类似中国山水画的"计白当黑"。

### 评分规则

```python
score += rest_count * 15  # 休止符越多越好

# 惩罚过密
if note_count > 6:
    score -= (note_count - 6) * 10

# 休止符分散（不是连续休止）
rest_positions = [i for i in range(16) if rhythm[i] == 0]
gaps = [rest_positions[i+1] - rest_positions[i] 
        for i in range(len(rest_positions)-1)]
avg_gap = sum(gaps) / len(gaps)
if avg_gap >= 3:
    score += 30
```

### 音乐特征
- ✅ 大量留白
- ✅ 音符稀疏
- ✅ 呼吸感强
- ❌ 可能显得空洞

### 适用场景
- 环境音乐
- 冥想音乐
- 极简主义
- 前奏、间奏

### 示例节奏模式
```
[1, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
 发 延 休 休 休 发 休 休 发 休 休 休 发 休 休 休
```
- 发声少（4个）
- 休止多（10个）
- 分散开

---

## 7. rhythm_fitness_march - 进行曲节奏

### 作用
创造规律、有力的进行曲节奏。

### 评分规则

```python
strong_beats = [0, 4, 8, 12]  # 每拍开始

# 强拍上应该有音符
for pos in strong_beats:
    if rhythm[pos] == 1:      # 发声 +30分
        score += 30
    elif rhythm[pos] == 2:    # 延长 +15分
        score += 15

# 检查4拍模式是否重复
pattern1 = rhythm[0:4]
pattern2 = rhythm[4:8]
pattern3 = rhythm[8:12]
pattern4 = rhythm[12:16]

if pattern1 == pattern2 or pattern2 == pattern3 or pattern3 == pattern4:
    score += 40  # 有重复模式
```

### 音乐特征
- ✅ 强拍有重音
- ✅ 规律重复
- ✅ 有力、稳定
- ❌ 可能单调

### 适用场景
- 进行曲
- 舞曲
- 军乐
- 背景音乐

### 示例节奏模式
```
[1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0]
 ↑        ↑        ↑        ↑
强拍发声  强拍发声  强拍发声  强拍发声
```
- 4拍模式完全重复
- 强拍都有音符

---

## 8. rhythm_fitness_varied - 多变复杂节奏

### 作用
创造复杂、富有变化的现代节奏。

### 评分规则

```python
# 检查2音符子序列多样性
pairs = [tuple(rhythm[i:i+2]) for i in range(15)]
unique_pairs = len(set(pairs))
score += unique_pairs * 10

# 检查3音符子序列多样性
triplets = [tuple(rhythm[i:i+3]) for i in range(14)]
unique_triplets = len(set(triplets))
score += unique_triplets * 8

# 惩罚长重复
for i in range(12):
    if rhythm[i] == rhythm[i+1] == rhythm[i+2] == rhythm[i+3]:
        score -= 20
```

### 音乐特征
- ✅ 高度复杂
- ✅ 不重复
- ✅ 现代感强
- ❌ 可能混乱

### 适用场景
- 现代音乐
- 实验音乐
- 自由爵士
- 前卫作品

### 示例节奏模式
```
[1, 0, 2, 1, 0, 1, 2, 0, 1, 2, 1, 0, 2, 0, 1, 1]
```
- 很少重复模式
- 高度变化
- 复杂组合

---

## 9. rhythm_fitness_overall - 综合节奏（推荐）

### 作用
结合多个函数的优点，生成平衡、优美的节奏。

### 权重配置

在 `config.py` 中定义：

```python
RHYTHM_WEIGHTS = {
    'basic': 1.5,        # 基础平衡
    'active': 1.0,       # 适度活跃
    'legato': 1.2,       # 较多连贯
    'syncopated': 0.5,   # 少量切分
    'balanced': 1.0,     # 保持均衡
    'sparse': 0.3,       # 轻微留白
    'march': 0.8,        # 一定规律
    'varied': 0.7,       # 适度变化
}
```

### 计算方式

```python
score = (
    rhythm_fitness_basic(melody) * 1.5 +
    rhythm_fitness_active(melody) * 1.0 +
    rhythm_fitness_legato(melody) * 1.2 +
    rhythm_fitness_syncopated(melody) * 0.5 +
    rhythm_fitness_balanced(melody) * 1.0 +
    rhythm_fitness_sparse(melody) * 0.3 +
    rhythm_fitness_march(melody) * 0.8 +
    rhythm_fitness_varied(melody) * 0.7
)
```

### 音乐特征
- ✅ 多方面平衡
- ✅ 自然流畅
- ✅ 适度变化
- ✅ 符合大多数审美

### 适用场景
- **推荐作为默认选择**
- 适合99%的音乐生成需求

### 自定义调整

如果你想要更活跃的节奏：
```python
RHYTHM_WEIGHTS['active'] = 2.0    # 增加活跃度
RHYTHM_WEIGHTS['legato'] = 0.5    # 减少连贯度
```

如果你想要更舒缓的节奏：
```python
RHYTHM_WEIGHTS['legato'] = 2.0    # 增加连贯度
RHYTHM_WEIGHTS['sparse'] = 1.0    # 增加留白
RHYTHM_WEIGHTS['active'] = 0.3    # 减少活跃度
```

---

## 附录：节奏编码说明

```
0 = 休止符 (RHYTHM_REST)  - 静音
1 = 发声   (RHYTHM_NOTE)  - 新音符开始
2 = 延长   (RHYTHM_HOLD)  - 延续当前音符
```

### 时间计算

- 每个基因位 = 1个八分音符 = 0.5拍
- 16个基因位 = 8拍 = 2小节（4/4拍）

### 音符长度示例

```
[1, 0, 0, 0]  → 1个八分音符（0.5拍）
[1, 2, 0, 0]  → 1个四分音符（1拍）
[1, 2, 2, 0]  → 1个附点四分音符（1.5拍）
[1, 2, 2, 2]  → 1个二分音符（2拍）
```

---

## 总结对比表

| 函数 | 密度 | 变化性 | 规律性 | 适用性 |
|------|------|--------|--------|--------|
| basic | 中 | 中 | 中 | ⭐⭐⭐⭐⭐ |
| active | 高 | 中 | 低 | ⭐⭐⭐ |
| legato | 低 | 低 | 高 | ⭐⭐⭐ |
| syncopated | 中 | 高 | 低 | ⭐⭐ |
| balanced | 中 | 高 | 中 | ⭐⭐⭐⭐ |
| sparse | 低 | 低 | 低 | ⭐⭐ |
| march | 高 | 低 | 高 | ⭐⭐⭐ |
| varied | 中 | 高 | 低 | ⭐⭐ |
| **overall** | **中** | **中高** | **中** | **⭐⭐⭐⭐⭐** |

---

*生成日期: 2024*  
*项目: 音乐与数学 - 遗传算法音乐生成系统*

