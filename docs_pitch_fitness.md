# 音高适应度函数详解

本文档详细介绍所有音高适应度函数的作用、原理和音乐效果。

---

## 目录

1. [pitch_fitness_stepwise](#1-pitch_fitness_stepwise---级进旋律)
2. [pitch_fitness_leap](#2-pitch_fitness_leap---跳跃旋律)
3. [pitch_fitness_arch](#3-pitch_fitness_arch---拱形轮廓)
4. [pitch_fitness_wave](#4-pitch_fitness_wave---波浪起伏)
5. [pitch_fitness_narrow_range](#5-pitch_fitness_narrow_range---窄音域)
6. [pitch_fitness_wide_range](#6-pitch_fitness_wide_range---宽音域)
7. [pitch_fitness_end_tonic](#7-pitch_fitness_end_tonic---结束主音)
8. [pitch_fitness_avoid_repetition](#8-pitch_fitness_avoid_repetition---避免重复)
9. [pitch_fitness_variety](#9-pitch_fitness_variety---音高多样性)
10. [pitch_fitness_ascending](#10-pitch_fitness_ascending---上行旋律)
11. [pitch_fitness_descending](#11-pitch_fitness_descending---下行旋律)
12. [pitch_fitness_center_focus](#12-pitch_fitness_center_focus---中心音聚焦)
13. [pitch_fitness_pentatonic_feel](#13-pitch_fitness_pentatonic_feel---五声音阶感)
14. [pitch_fitness_overall](#14-pitch_fitness_overall---综合音高推荐)

---

## 1. pitch_fitness_stepwise - 级进旋律

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
```

### 音乐特征
- ✅ 相邻音符距离近
- ✅ 容易演唱
- ✅ 流畅自然
- ❌ 可能缺少戏剧性

### 音程分类

| 音程 | 半音数 | 评分 | 示例 |
|------|--------|------|------|
| 小二度 | 1 | +20 | C→C# |
| 大二度 | 2 | +20 | C→D |
| 小三度 | 3 | +5 | C→Eb |
| 大三度 | 4 | +5 | C→E |
| 纯四度+ | 5+ | -10 | C→F及以上 |

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
```

---

## 2. pitch_fitness_leap - 跳跃旋律

### 作用
创造富有张力、戏剧性的跳跃旋律。

### 评分规则

```python
for i in range(len(pitches) - 1):
    interval = abs(pitches[i] - pitches[i+1])
    
    if interval >= 5:      # 纯四度及以上 → +25分
        score += 25
    elif interval >= 3:    # 小三度及以上 → +10分
        score += 10
    else:                  # 级进 → -5分
        score -= 5
```

### 音乐特征
- ✅ 音程跨度大
- ✅ 戏剧性强
- ✅ 引人注目
- ❌ 较难演唱

### 音程分类

| 音程 | 半音数 | 评分 | 示例 |
|------|--------|------|------|
| 纯四度+ | 5+ | +25 | C→F, C→G |
| 小/大三度 | 3-4 | +10 | C→E |
| 大二度以下 | ≤2 | -5 | C→D |

### 适用场景
- 歌剧咏叹调
- 炫技段落
- 戏剧性配乐
- 器乐独奏

### 示例旋律
```
C → G → E → C → A → F → D
60→67→64→60→69→65→62
+7 -3 -4 +9 -4 -3  (大跳多，戏剧性强)
```

---

## 3. pitch_fitness_arch - 拱形轮廓

### 作用
创造经典的拱形乐句：前半上升，后半下降，中间最高。

### 评分规则

```python
mid = len(pitches) // 2

# 前半段奖励上升
for i in range(mid - 1):
    if pitches[i+1] >= pitches[i]:
        score += 15

# 后半段奖励下降
for i in range(mid, len(pitches) - 1):
    if pitches[i+1] <= pitches[i]:
        score += 15

# 中点是最高点
if pitches[mid] == max(pitches):
    score += 50
```

### 音乐特征
- ✅ 有明确的高潮点
- ✅ 张弛有度
- ✅ 符合自然呼吸
- ✅ 经典乐句结构

### 轮廓示例

```
音高
 ^
 |      ●●●
 |    ●     ●
 |  ●         ●
 |●             ●
 +----------------> 时间
  前半上升  后半下降
```

### 适用场景
- 古典音乐
- 艺术歌曲
- 主题旋律
- 乐句结构

### 示例旋律
```
C → D → E → G → A → G → E → D → C
60→62→64→67→69→67→64→62→60
    上升     ↑   下降
          高潮点
```

---

## 4. pitch_fitness_wave - 波浪起伏

### 作用
创造上下起伏、富有动感的旋律线条。

### 评分规则

```python
# 检测方向变化（峰值和谷值）
direction_changes = 0
for i in range(1, len(pitches) - 1):
    # 峰值：比前后都高
    is_peak = pitches[i] > pitches[i-1] and pitches[i] > pitches[i+1]
    # 谷值：比前后都低
    is_valley = pitches[i] < pitches[i-1] and pitches[i] < pitches[i+1]
    
    if is_peak or is_valley:
        direction_changes += 1

# 最佳：2-4次方向变化
if 2 <= direction_changes <= 4:
    score += 100
else:
    score += direction_changes * 10
```

### 音乐特征
- ✅ 频繁转向
- ✅ 富有动感
- ✅ 不单调
- ⚠️ 需控制变化频率

### 轮廓示例

```
音高
 ^    ●       ●
 |  ●   ●   ●   ●
 |        ●       ●
 +-------------------> 时间
  峰谷交替，波浪起伏
```

### 适用场景
- 装饰性旋律
- 器乐作品
- 活泼的段落
- 变奏曲

### 示例旋律
```
C → E → D → F → E → G → F → D
60→64→62→65→64→67→65→62
 ↗  ↘  ↗  ↘  ↗  ↘  
峰 谷 峰 谷 峰（3次变化）
```

---

## 5. pitch_fitness_narrow_range - 窄音域

### 作用
将旋律限制在小范围内，创造平和、内敛的效果。

### 评分规则

```python
pitch_range = max(pitches) - min(pitches)

if pitch_range <= 5:      # ≤纯四度 → +100分
    score += 100
elif pitch_range <= 7:    # ≤纯五度 → +50分
    score += 50
else:
    score -= (pitch_range - 7) * 10  # 每超1个半音 -10分
```

### 音乐特征
- ✅ 音域集中
- ✅ 平和安静
- ✅ 易于演唱
- ❌ 可能单调

### 音域示例

```
窄音域 (5个半音)
┌────────┐
C  D  E  F  G
60 62 64 65 67
```

### 适用场景
- 冥想音乐
- 背景音乐
- 儿童歌曲
- 简单旋律

### 示例旋律
```
C → D → E → D → C → E → F → E → D → C
60→62→64→62→60→64→65→64→62→60
音域：60-65 (5个半音) ✓
```

---

## 6. pitch_fitness_wide_range - 宽音域

### 作用
鼓励使用宽广音域，展现演唱/演奏技巧。

### 评分规则

```python
pitch_range = max(pitches) - min(pitches)

if pitch_range >= 12:     # ≥八度 → +100分
    score += 100
elif pitch_range >= 7:    # ≥纯五度 → +50分
    score += 50
else:
    score -= (7 - pitch_range) * 10  # 音域太窄扣分
```

### 音乐特征
- ✅ 音域宽广
- ✅ 展现音域
- ✅ 戏剧性强
- ❌ 技术要求高

### 音域示例

```
宽音域 (12+个半音)
┌────────────────────────┐
C3         C4         C5
48         60         72
低音区     中音区     高音区
```

### 适用场景
- 歌剧
- 炫技作品
- 器乐独奏
- 展现技巧

### 示例旋律
```
C3 → C4 → G4 → C5 → G3
48 → 60 → 67 → 72 → 55
音域：48-72 (24个半音，2个八度) ✓
```

---

## 7. pitch_fitness_end_tonic - 结束主音

### 作用
让旋律结束在主音上，创造完满的终止感。

### 评分规则

```python
last_pitch_gene = melody.pitch_genes[-1]
relative_position = last_pitch_gene % 7

if relative_position == 0:    # 主音 → +100分
    return 100
elif relative_position == 2:  # 三音 → +50分
    return 50
elif relative_position == 4:  # 五音 → +30分
    return 30
else:
    return -20                 # 其他音 → -20分
```

### 音乐特征
- ✅ 终止感强
- ✅ 符合传统和声
- ✅ 稳定、完满
- ⚠️ 过于传统

### 调式音级

```
C大调示例：
音级: 1   2   3   4   5   6   7
音名: C   D   E   F   G   A   B
位置: 0   1   2   3   4   5   6

结束在：
- 1级(C) → 最稳定 +100
- 3级(E) → 较稳定 +50
- 5级(G) → 可接受 +30
```

### 适用场景
- 古典音乐
- 传统和声
- 完整乐句
- 主题旋律

### 示例
```
...F → E → D → C
   65→64→62→60
           结束在主音C ✓
```

---

## 8. pitch_fitness_avoid_repetition - 避免重复

### 作用
惩罚相同音高连续出现，追求变化。

### 评分规则

```python
for i in range(len(pitches) - 1):
    if pitches[i] == pitches[i+1]:
        score -= 15  # 重复 → -15分
    else:
        score += 5   # 变化 → +5分
```

### 音乐特征
- ✅ 音高多变
- ✅ 避免单调
- ✅ 现代感
- ❌ 可能失去歌唱性

### 对比

```
有重复（扣分）：
C → C → C → D → E
60→60→60→62→64
   ↓  ↓
  重复 重复

无重复（加分）：
C → D → E → F → G
60→62→64→65→67
每个音都不同 ✓
```

### 适用场景
- 现代音乐
- 器乐作品
- 快速乐段
- 追求变化

---

## 9. pitch_fitness_variety - 音高多样性

### 作用
鼓励使用更多不同的音高。

### 评分规则

```python
unique_pitches = len(set(melody.pitch_genes))

if unique_pitches >= 8:    # 8种以上 → +120分
    return 120
elif unique_pitches >= 5:  # 5-7种 → +100分
    return 100
elif unique_pitches >= 4:  # 4种 → +50分
    return 50
else:
    return unique_pitches * 10
```

### 音乐特征
- ✅ 色彩丰富
- ✅ 音高多样
- ✅ 不单调
- ⚠️ 需控制使用

### 多样性示例

```
低多样性（3种音）：
C → D → C → D → C → D → C
60→62→60→62→60→62→60
只用了C和D（单调）

高多样性（7种音）：
C → D → E → F → G → A → B → C
60→62→64→65→67→69→71→72
使用了完整音阶 ✓
```

### 适用场景
- 变奏曲
- 展开部
- 完整旋律
- 丰富音色

---

## 10. pitch_fitness_ascending - 上行旋律

### 作用
创造整体向上的旋律，表达积极情绪。

### 评分规则

```python
# 起点低于终点
if pitches[-1] > pitches[0]:
    score += 50

# 统计上行音程
ascending = 0
for i in range(len(pitches) - 1):
    if pitches[i+1] > pitches[i]:
        ascending += 1

score += ascending * 15
```

### 音乐特征
- ✅ 整体上升
- ✅ 积极向上
- ✅ 激昂情绪
- ⚠️ 需要音域支持

### 上行示例

```
音高
 ^
 |             ●
 |          ●
 |       ●
 |    ●
 | ●
 +----------------> 时间
  整体趋势向上

C → D → E → G → A → C
60→62→64→67→69→72
  整体上升 +7个半音
```

### 适用场景
- 高潮前
- 激动情绪
- 问句
- 推进段落

---

## 11. pitch_fitness_descending - 下行旋律

### 作用
创造整体向下的旋律，表达舒缓情绪。

### 评分规则

```python
# 终点低于起点
if pitches[-1] < pitches[0]:
    score += 50

# 统计下行音程
descending = 0
for i in range(len(pitches) - 1):
    if pitches[i+1] < pitches[i]:
        descending += 1

score += descending * 15
```

### 音乐特征
- ✅ 整体下降
- ✅ 舒缓放松
- ✅ 安静收尾
- ⚠️ 可能显得消极

### 下行示例

```
音高
 ^
 | ●
 |    ●
 |       ●
 |          ●
 |             ●
 +----------------> 时间
  整体趋势向下

C → A → G → E → D → C
72→69→67→64→62→60
  整体下降 -12个半音
```

### 适用场景
- 尾声
- 平静段落
- 答句
- 结束部分

---

## 12. pitch_fitness_center_focus - 中心音聚焦

### 作用
让旋律围绕某个中心音运动，创造稳定感。

### 评分规则

```python
# 找出最常出现的音高
most_common_pitch, count = Counter(pitch_genes).most_common(1)[0]

# 出现频率高
if count >= 4:
    score += count * 15

# 中心音是重要音级
relative_position = most_common_pitch % 7
if relative_position in [0, 2, 4]:  # 主音、三音或五音
    score += 50
```

### 音乐特征
- ✅ 有中心点
- ✅ 稳定回旋
- ✅ 调性明确
- ⚠️ 可能重复

### 中心音示例

```
围绕G音运动：
E → G → F → G → A → G → F → G
64→67→65→67→69→67→65→67
    ↑     ↑     ↑     ↑
   中心  中心  中心  中心
G音出现4次，是旋律中心
```

### 适用场景
- 回旋曲
- 民歌
- 持续低音风格
- 调式音乐

---

## 13. pitch_fitness_pentatonic_feel - 五声音阶感

### 作用
避免半音进行，创造五声音阶（民族音乐）风格。

### 评分规则

```python
# 惩罚半音进行
semitone_count = 0
for i in range(len(pitches) - 1):
    if abs(pitches[i] - pitches[i+1]) == 1:
        semitone_count += 1
score -= semitone_count * 20

# 奖励全音和三度进行
for i in range(len(pitches) - 1):
    interval = abs(pitches[i] - pitches[i+1])
    if interval in [2, 4]:  # 全音或大三度
        score += 10
```

### 音乐特征
- ✅ 避免半音
- ✅ 民族风格
- ✅ 简朴自然
- ✅ 五声色彩

### 音程对比

```
包含半音（扣分）：
C → C# → D → D# → E
60→61→62→63→64
   ↓    ↓    ↓
  半音  半音  半音

五声感（加分）：
C → D → E → G → A → C
60→62→64→67→69→72
   全音 全音 小三度 全音 小三度
```

### 适用场景
- 中国民乐
- 亚洲音乐
- 民族风格
- 简朴旋律

---

## 14. pitch_fitness_overall - 综合音高（推荐）

### 作用
结合多个函数的优点，生成平衡、优美的旋律。

### 权重配置

在 `config.py` 中定义：

```python
PITCH_WEIGHTS = {
    'stepwise': 2.0,            # 级进为主
    'leap': 0.5,                # 少量跳跃
    'arch': 1.5,                # 拱形轮廓
    'wave': 1.0,                # 波浪起伏
    'narrow_range': 0.3,        # 窄音域
    'wide_range': 0.5,          # 宽音域
    'end_tonic': 1.5,           # 结束主音
    'avoid_repetition': 1.0,    # 避免重复
    'variety': 1.2,             # 音高多样性
    'ascending': 0.3,           # 轻微上行
    'descending': 0.0,          # 不强调下行
    'center_focus': 0.5,        # 中心音
    'pentatonic_feel': 0.8,     # 避免半音
}
```

### 计算方式

```python
score = (
    pitch_fitness_stepwise(melody) * 2.0 +        # 主要级进
    pitch_fitness_leap(melody) * 0.5 +            # 少量跳跃
    pitch_fitness_arch(melody) * 1.5 +            # 拱形轮廓
    pitch_fitness_wave(melody) * 1.0 +            # 适度起伏
    pitch_fitness_narrow_range(melody) * 0.3 +    # 音域平衡
    pitch_fitness_wide_range(melody) * 0.5 +      
    pitch_fitness_end_tonic(melody) * 1.5 +       # 完满终止
    pitch_fitness_avoid_repetition(melody) * 1.0 + # 避免重复
    pitch_fitness_variety(melody) * 1.2 +         # 音高丰富
    pitch_fitness_ascending(melody) * 0.3 +       # 轻微上行
    pitch_fitness_center_focus(melody) * 0.5 +    # 调性中心
    pitch_fitness_pentatonic_feel(melody) * 0.8   # 避免半音
)
```

### 音乐特征
- ✅ 以级进为主（流畅）
- ✅ 适量跳跃（变化）
- ✅ 拱形轮廓（结构）
- ✅ 结束主音（完满）
- ✅ 多方面平衡

### 适用场景
- **推荐作为默认选择**
- 适合大多数音乐风格
- 自然优美的旋律

### 自定义调整

**想要更流畅的旋律：**
```python
PITCH_WEIGHTS['stepwise'] = 3.0   # 增加级进
PITCH_WEIGHTS['leap'] = 0.2       # 减少跳跃
```

**想要更戏剧性的旋律：**
```python
PITCH_WEIGHTS['leap'] = 1.5       # 增加跳跃
PITCH_WEIGHTS['wide_range'] = 1.5 # 增加音域
PITCH_WEIGHTS['stepwise'] = 1.0   # 减少级进
```

**想要更民族风格：**
```python
PITCH_WEIGHTS['pentatonic_feel'] = 2.0  # 强化五声
PITCH_WEIGHTS['center_focus'] = 1.5     # 强化中心音
```

---

## 附录A：音程表

| 名称 | 半音数 | 示例(from C) | 音程性质 |
|------|--------|--------------|----------|
| 小二度 | 1 | C→C# | 紧张 |
| 大二度 | 2 | C→D | 流畅 |
| 小三度 | 3 | C→Eb | 柔和 |
| 大三度 | 4 | C→E | 明亮 |
| 纯四度 | 5 | C→F | 稳定 |
| 增四/减五 | 6 | C→F# | 不稳定 |
| 纯五度 | 7 | C→G | 和谐 |
| 小六度 | 8 | C→Ab | 哀伤 |
| 大六度 | 9 | C→A | 开阔 |
| 小七度 | 10 | C→Bb | 紧张 |
| 大七度 | 11 | C→B | 很紧张 |
| 八度 | 12 | C→C | 完全和谐 |

---

## 附录B：音高编码说明

### 基因编码

```python
pitch_genes = [0, 2, 4, 5, 2, 0, ...]
```

- 每个数字是调式内的**音级索引**
- 范围：`0` 到 `len(scale_notes)-1`
- 例如在C大调（有20+个音）：
  - `0, 7, 14` → C3, C4, C5 (不同八度的主音)
  - `2, 9, 16` → E3, E4, E5 (不同八度的三音)

### 实际音高

```python
# C大调音阶 (F3-G5范围)
scale_notes = [53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 71, 72, ...]
               F3  G3  A3  Bb3 C4  D4  E4  F4  G4  A4  B4  C5  ...

# 基因 → MIDI音高
pitch_genes[i] = 5  →  scale_notes[5] = 62 (D4)
```

---

## 附录C：调式音阶

系统支持的调式（在`config.py`中定义）：

### 大调
- C Major: C D E F G A B
- G Major: G A B C D E F#
- D Major: D E F# G A B C#
- A Major: A B C# D E F# G#
- E Major: E F# G# A B C# D#
- F Major: F G A Bb C D E

### 小调（自然小调）
- A Minor: A B C D E F G
- E Minor: E F# G A B C D
- D Minor: D E F G A Bb C

每个调式在F3(53)到G5(79)的范围内都有20+个音可用。

---

## 总结对比表

| 函数 | 音程特征 | 音域 | 结构性 | 适用性 |
|------|----------|------|--------|--------|
| stepwise | 小音程 | 中 | 低 | ⭐⭐⭐⭐⭐ |
| leap | 大音程 | 宽 | 低 | ⭐⭐⭐ |
| arch | 上升+下降 | 中 | 高 | ⭐⭐⭐⭐ |
| wave | 起伏 | 中 | 中 | ⭐⭐⭐⭐ |
| narrow_range | 集中 | 窄 | 低 | ⭐⭐⭐ |
| wide_range | 分散 | 宽 | 低 | ⭐⭐⭐ |
| end_tonic | 任意 | 任意 | 高 | ⭐⭐⭐⭐⭐ |
| avoid_repetition | 多变 | 任意 | 低 | ⭐⭐⭐ |
| variety | 多样 | 任意 | 低 | ⭐⭐⭐⭐ |
| ascending | 上行 | 上升 | 中 | ⭐⭐⭐ |
| descending | 下行 | 下降 | 中 | ⭐⭐⭐ |
| center_focus | 回旋 | 中 | 中 | ⭐⭐⭐ |
| pentatonic_feel | 无半音 | 任意 | 低 | ⭐⭐⭐ |
| **overall** | **平衡** | **中** | **高** | **⭐⭐⭐⭐⭐** |

---

*生成日期: 2024*  
*项目: 音乐与数学 - 遗传算法音乐生成系统*

