# 音高适应度函数详解

本文档详细介绍当前系统中所有音高适应度函数的作用、原理和音乐效果。

**当前版本：5个音高适应度函数**

---

## 目录

1. [pitch_fitness_stepwise](#1-pitch_fitness_stepwise---级进流畅)
2. [pitch_fitness_consonance](#2-pitch_fitness_consonance---音程协和度)
3. [pitch_fitness_range](#3-pitch_fitness_range---音域平衡)
4. [pitch_fitness_direction](#4-pitch_fitness_direction---旋律方向变化)
5. [pitch_fitness_climax](#5-pitch_fitness_climax---旋律高潮)
6. [pitch_fitness_overall](#6-pitch_fitness_overall---综合音高适应度)

---

## 1. pitch_fitness_stepwise - 级进流畅

### 作用
创造流畅、易唱的旋律，相邻音符以小音程连接。

### 评分规则

```python
for i in range(len(pitches) - 1):
    interval = abs(pitches[i] - pitches[i+1])
    
    if interval <= 2:      # 大二度以内 → +20分
        score += 20
    elif interval <= 4:    # 小三度到大三度 → +5分
        score += 5
    else:                  # 大跳 → -10分
        score -= 10

# 归一化：除以音程数量
normalized_score = score / num_intervals
```

### 音乐特征
- ✅ 相邻音符距离近
- ✅ 容易演唱
- ✅ 流畅自然
- ⚠️ 可能缺少戏剧性

### 音程分类

| 音程 | 半音数 | 评分 | 示例 |
|------|--------|------|------|
| 小二度 | 1 | +20 | C→C# |
| 大二度 | 2 | +20 | C→D |
| 小三度 | 3 | +5 | C→Eb |
| 大三度 | 4 | +5 | C→E |
| 纯四度+ | 5+ | -10 | C→F及以上 |

### 归一化说明

- **关键改进**：得分除以音程数量，避免音符数量影响得分
- 8个音符和16个音符如果都是级进，得分相同（都约20分）
- 体现的是**音程质量**而非数量

### 适用场景
- 民歌
- 圣咏
- 儿童歌曲
- 抒情旋律

### 示例旋律
```
C → D → E → F → E → D → C
60→62→64→65→64→62→60
+2 +2 +1 -1 -2 -2  (都是小音程，流畅)
归一化得分: (20+20+20+20+20+20)/6 ≈ 20分
```

---

## 2. pitch_fitness_consonance - 音程协和度

### 作用
根据音乐理论，评估相邻音符之间音程的协和程度，鼓励使用协和音程。

### 评分规则

```python
for i in range(len(pitches) - 1):
    interval = abs(pitches[i] - pitches[i+1])
    interval_class = interval % 12  # 归约到一个八度内
    
    if interval == 0:              # 相邻音符相同 → -15分 (惩罚重复)
        score -= 15
    elif interval == 12:           # 纯八度 → +12分
        score += 12
    elif interval_class == 7:      # 纯五度 → +12分
        score += 12
    elif interval_class == 5:      # 纯四度 → +12分
        score += 12
    elif interval_class in [3, 4]: # 小/大三度 → +12分
        score += 12
    elif interval_class in [8, 9]: # 小/大六度 → +10分
        score += 10
    elif interval_class == 2:      # 大二度 → +5分
        score += 5
    elif interval_class == 1:      # 小二度 → -5分
        score -= 5
    elif interval_class == 6:      # 三全音 → -10分
        score -= 10
    elif interval_class in [10, 11]: # 小/大七度 → -5/-10分
        score -= 5 或 -10

# 归一化
normalized_score = score / num_intervals
```

### 音程协和度分类

| 音程类型 | 半音数 | 评分 | 协和性 |
|---------|--------|------|--------|
| **重复音** | 0 | **-15** | ❌ 单调 |
| **纯八度** | 12 | +12 | ⭐⭐⭐ |
| **纯五度** | 7 | +12 | ⭐⭐⭐ |
| **纯四度** | 5 | +12 | ⭐⭐⭐ |
| **大/小三度** | 3-4 | +12 | ⭐⭐⭐ |
| **大/小六度** | 8-9 | +10 | ⭐⭐ |
| **大二度** | 2 | +5 | ⭐ |
| **小二度** | 1 | -5 | ❌ |
| **三全音** | 6 | -10 | ❌❌ |
| **七度** | 10-11 | -5/-10 | ❌ |

### 设计理念

**平衡评分**：
- 所有主要协和音程（八度、五度、四度、三度）得分相同（12分）
- 避免遗传算法只选择某一种音程
- 惩罚重复音（-15分），鼓励旋律变化

### 音乐特征
- ✅ 音程协和悦耳
- ✅ 音响效果好
- ✅ 避免单调重复
- ⚠️ 可能有跳跃

### 示例旋律

**协和旋律（高分）：**
```
C → E → G → C' (三和弦分解)
60→64→67→72
+4(大三度,+12) +3(小三度,+12) +5(纯四度,+12)
平均得分: 12分
```

**不协和旋律（低分）：**
```
C → C# → D → D# (半音阶)
60→61→62→63
+1(小二度,-5) +1(-5) +1(-5)
平均得分: -5分
```

### 适用场景
- 和声为主的音乐
- 三和弦分解
- 跳跃旋律
- 器乐作品

---

## 3. pitch_fitness_range - 音域平衡

### 作用
评估旋律的音域范围是否适中，避免过窄（单调）或过宽（难唱）。

### 评分规则

```python
pitches = [n[0] for n in melody.notes]
pitch_range = max(pitches) - min(pitches)  # 最高音 - 最低音

if pitch_range < 6:              # 太窄（<半个八度）→ -10分
    score = -10
elif 6 <= pitch_range <= 18:    # 适中（0.5-1.5个八度）→ +20分
    score = 20
else:                            # 太宽（>1.5个八度）→ -5分
    score = -5
```

### 音域分类

| 音域（半音数） | 八度数 | 评分 | 说明 |
|--------------|--------|------|------|
| <6 | <0.5 | -10 | 太窄，单调 |
| 6-12 | 0.5-1.0 | +20 | ✅ 理想 |
| 13-18 | 1.0-1.5 | +20 | ✅ 理想 |
| >18 | >1.5 | -5 | 太宽，难唱 |

### 音乐特征
- ✅ 音域适中
- ✅ 易于演唱
- ✅ 自然舒适
- ⚠️ 限制音域范围

### 示例

**适中音域（+20分）：**
```
音域: C4(60) ~ E5(76) = 16个半音 ✓
旋律: C4 → G4 → E5 → A4 → C4
     60 → 67 → 76 → 69 → 60
```

**太窄音域（-10分）：**
```
音域: C4(60) ~ E4(64) = 4个半音 ✗
旋律: C4 → D4 → E4 → D4 → C4
     60 → 62 → 64 → 62 → 60
```

### 适用场景
- 歌曲创作
- 限制音域要求
- 平衡音乐
- 自然旋律

---

## 4. pitch_fitness_direction - 旋律方向变化

### 作用
评估旋律的方向变化是否丰富，鼓励起伏变化，避免单一方向。

### 评分规则

```python
# 1. 计算每个音程的方向
directions = []
for i in range(len(pitches) - 1):
    diff = pitches[i+1] - pitches[i]
    if diff > 0:
        directions.append(1)   # 上行
    elif diff < 0:
        directions.append(-1)  # 下行
    else:
        directions.append(0)   # 持平

# 2. 统计方向变化次数
direction_changes = 0
for i in range(len(directions) - 1):
    if directions[i] != 0 and directions[i+1] != 0:
        if directions[i] != directions[i+1]:
            direction_changes += 1

# 3. 归一化
change_ratio = direction_changes / (len(directions) - 1)
score = change_ratio * 20  # 满分20
```

### 方向变化示例

**多变化（高分）：**
```
C → E → D → F → E → G → F
60→64→62→65→64→67→65
 ↗  ↘  ↗  ↘  ↗  ↘
3次方向变化，变化率 = 3/5 = 60%
得分: 0.6 × 20 = 12分
```

**单一方向（低分）：**
```
C → D → E → F → G → A
60→62→64→65→67→69
 ↗  ↗  ↗  ↗  ↗
0次方向变化，变化率 = 0%
得分: 0分
```

### 音乐特征
- ✅ 旋律起伏丰富
- ✅ 避免单调
- ✅ 有变化
- ⚠️ 过多变化可能不流畅

### 适用场景
- 装饰性旋律
- 活泼段落
- 变奏曲
- 丰富旋律线

---

## 5. pitch_fitness_climax - 旋律高潮

### 作用
评估旋律是否有明显的高潮点（最高音或最低音在中间），避免开头或结尾就是极值。

### 评分规则

```python
pitches = [n[0] for n in melody.notes]
n = len(pitches)

# 找到最高音和最低音的位置
max_pitch_idx = pitches.index(max(pitches))
min_pitch_idx = pitches.index(min(pitches))

score = 0

# 最高音不在开头或结尾
if 0 < max_pitch_idx < n - 1:
    score += 12.5

# 最低音不在开头或结尾
if 0 < min_pitch_idx < n - 1:
    score += 12.5

# 满分: 25分
```

### 高潮点位置

| 情况 | 得分 | 说明 |
|------|------|------|
| 最高音和最低音都在中间 | 25分 | ✅ 最优 |
| 只有最高音在中间 | 12.5分 | ⚠️ 一般 |
| 只有最低音在中间 | 12.5分 | ⚠️ 一般 |
| 极值在开头或结尾 | 0分 | ❌ 平淡 |

### 示例

**有高潮（+25分）：**
```
位置: 0   1   2   3   4   5   6   7
音高: C4  E4  G4  C5  A4  F4  D4  C4
     60  64  67  72  69  65  62  60
              最高↑
最高音在位置3（中间）✓
最低音在位置0和7（两端）
得分: 12.5分
```

**无高潮（0分）：**
```
位置: 0   1   2   3   4   5
音高: C5  A4  G4  E4  D4  C4
     72  69  67  64  62  60
    最高↑
最高音在开头，无高潮感
得分: 0分
```

### 音乐特征
- ✅ 有明确的高潮点
- ✅ 张弛有度
- ✅ 结构感强
- ⚠️ 可能过于规整

### 适用场景
- 主题旋律
- 完整乐句
- 经典结构
- 抒情段落

---

## 6. pitch_fitness_overall - 综合音高适应度

### 作用
将所有音高适应度函数的得分相加，得到综合评价。

### 计算方式

```python
def pitch_fitness_overall(melody):
    total_score = 0
    
    # 根据权重决定是否计算每个函数
    if PITCH_WEIGHTS.get('stepwise', 0) != 0:
        total_score += pitch_fitness_stepwise(melody)
    
    if PITCH_WEIGHTS.get('consonance', 0) != 0:
        total_score += pitch_fitness_consonance(melody)
    
    if PITCH_WEIGHTS.get('range', 0) != 0:
        total_score += pitch_fitness_range(melody)
    
    if PITCH_WEIGHTS.get('direction', 0) != 0:
        total_score += pitch_fitness_direction(melody)
    
    if PITCH_WEIGHTS.get('climax', 0) != 0:
        total_score += pitch_fitness_climax(melody)
    
    return total_score
```

### 权重配置

在 `config.py` 中定义：

```python
PITCH_WEIGHTS = {
    'stepwise': 1.0,      # 级进流畅
    'consonance': 1.0,    # 音程协和度
    'range': 1.0,         # 音域平衡
    'direction': 1.0,     # 旋律方向变化
    'climax': 1.0,        # 旋律高潮
}
```

### 得分组成

**示例旋律的总分计算：**
```
stepwise:    20分  (流畅级进)
consonance:  12分  (协和音程)
range:       20分  (音域适中)
direction:   15分  (方向多变)
climax:      12.5分 (有高潮点)
─────────────────────
总分:        79.5分
```

### 启用/禁用函数

**启用**：权重 > 0
```python
PITCH_WEIGHTS['stepwise'] = 1.0  # 启用
```

**禁用**：权重 = 0
```python
PITCH_WEIGHTS['stepwise'] = 0.0  # 禁用，不计算该函数
```

### 音乐特征
- ✅ 多方面平衡
- ✅ 综合评价
- ✅ 灵活配置
- ✅ 适合大多数场景

### 自定义调整

**强调流畅性：**
```python
PITCH_WEIGHTS['stepwise'] = 2.0    # 提高权重
PITCH_WEIGHTS['consonance'] = 0.5  # 降低权重
```

**强调协和性：**
```python
PITCH_WEIGHTS['stepwise'] = 0.5
PITCH_WEIGHTS['consonance'] = 2.0
```

**只用单个函数（消融实验）：**
```python
PITCH_WEIGHTS = {
    'stepwise': 1.0,      # 只启用这个
    'consonance': 0.0,    # 其他全部禁用
    'range': 0.0,
    'direction': 0.0,
    'climax': 0.0,
}
```

---

## 附录A：音程表

| 名称 | 半音数 | 示例(from C) | 协和度 | stepwise | consonance |
|------|--------|------------|--------|----------|------------|
| 重复音 | 0 | C→C | ❌ | +20 | -15 |
| 小二度 | 1 | C→C# | ❌ | +20 | -5 |
| 大二度 | 2 | C→D | ⭐ | +20 | +5 |
| 小三度 | 3 | C→Eb | ⭐⭐ | +5 | +12 |
| 大三度 | 4 | C→E | ⭐⭐ | +5 | +12 |
| 纯四度 | 5 | C→F | ⭐⭐⭐ | -10 | +12 |
| 三全音 | 6 | C→F# | ❌ | -10 | -10 |
| 纯五度 | 7 | C→G | ⭐⭐⭐ | -10 | +12 |
| 小六度 | 8 | C→Ab | ⭐⭐ | -10 | +10 |
| 大六度 | 9 | C→A | ⭐⭐ | -10 | +10 |
| 小七度 | 10 | C→Bb | ❌ | -10 | -5 |
| 大七度 | 11 | C→B | ❌ | -10 | -10 |
| 纯八度 | 12 | C→C' | ⭐⭐⭐ | -10 | +12 |

### 两个函数的互补关系

- **stepwise**：鼓励小音程（级进），惩罚大音程（跳跃）
- **consonance**：鼓励协和音程（任何音程只要协和），惩罚不协和音程

**组合效果**：
- 大二度（C→D）：stepwise高分(+20) + consonance低分(+5) → 整体不错
- 大三度（C→E）：stepwise低分(+5) + consonance高分(+12) → 整体不错
- 小二度（C→C#）：stepwise高分(+20) + consonance负分(-5) → 中等
- 纯五度（C→G）：stepwise负分(-10) + consonance高分(+12) → 中等

两者结合能产生**既流畅又悦耳**的旋律！

---

## 附录B：音高编码说明

### 基因编码（32个位置）

```python
pitch_genes = [0, 2, 4, 5, 2, 0, ...]  # 长度32
```

- 每个数字是调式内的**音级索引**
- 范围：`0` 到 `len(scale_notes)-1`
- 对应32个八分音符的位置（4小节，4/4拍）

### 实际音高

```python
# C大调音阶 (F3-G5范围)
scale_notes = [53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 71, 72, ...]
               F3  G3  A3  Bb3 C4  D4  E4  F4  G4  A4  B4  C5  ...

# 基因 → MIDI音高
pitch_genes[i] = 5  →  scale_notes[5] = 62 (D4)
```

### 音符生成

只有节奏基因为 `1`（起拍）的位置才会生成新音符：

```python
rhythm_genes = [1, 2, 1, 2, 0, ...]
pitch_genes  = [0, 0, 2, 2, 4, ...]
               ↓  ↓  ↓
           音符1 音符2
           (C4) (E4)
```

---

## 总结对比表

| 函数 | 关注点 | 得分范围 | 归一化 | 适用性 |
|------|--------|---------|--------|--------|
| stepwise | 音程大小 | -10~+20/音程 | ✅ | ⭐⭐⭐⭐⭐ |
| consonance | 音程协和度 | -15~+12/音程 | ✅ | ⭐⭐⭐⭐⭐ |
| range | 音域范围 | -10~+20 | ❌ | ⭐⭐⭐⭐ |
| direction | 方向变化 | 0~+20 | ✅ | ⭐⭐⭐⭐ |
| climax | 高潮位置 | 0~+25 | ❌ | ⭐⭐⭐ |
| **overall** | **综合** | **累加** | **部分** | **⭐⭐⭐⭐⭐** |

---

*生成日期: 2024年12月*  
*项目: 音乐与数学 - 遗传算法音乐生成系统*  
*版本: 5函数版本*
