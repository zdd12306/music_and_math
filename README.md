# 音乐与数学 - 基于遗传算法的旋律生成系统

## 项目简介

这是一个使用遗传算法生成音乐旋律的系统，采用**双基因编码**：
- **节奏基因**：独立控制音符的时值和休止符
- **音高基因**：独立控制音符在调式内的音高选择

两个基因序列独立进化，通过不同的适应度函数组合，可以生成丰富多样的音乐风格。

## 核心特性

✨ **节奏与音高分离** - 独立的基因编码和进化机制  
🎼 **多调式支持** - 支持9种大调和小调，用户可选择  
🧬 **双适应度函数** - 节奏和音高各自独立评分  
🎵 **16拍标准长度** - 4小节，包含起拍与休止符  
🔄 **音乐变换** - 移调、倒影、逆行、增值、减值  

## 环境配置

### 创建环境

```bash
conda create -n mm python=3.10
conda activate mm
```

### 安装依赖

```bash
pip install midiutil numpy pygame pretty_midi pypianoroll music21
```

## 文件结构

```
music_and_math/
├── main.py                        # 主程序：遗传算法引擎
├── fitness_function_rhythm.py     # 节奏适应度函数库（8个函数）
├── fitness_function_pitch.py      # 音高适应度函数库（13个函数）
├── playmid.py                     # MIDI播放器
├── evaluatemid.py                 # MIDI分析工具
├── visualmid.py                   # 可视化工具（钢琴卷帘图）
├── visualmid2.py                  # 可视化工具（五线谱）
└── README.md                      # 本文件
```

## 使用方法

### 1. 运行主程序生成音乐

```bash
python main.py
```

程序会提示你选择调式：
```
可用调式:
  1. C_major    5. E_major    9. D_minor
  2. G_major    6. F_major
  3. D_major    7. A_minor
  4. A_major    8. E_minor

请选择调式编号 (1-9，直接回车默认C大调): 
```

程序将：
- 运行所有节奏×音高适应度函数组合（8×13=104种）
- 每个组合进化1024代
- 自动保存MIDI文件到当前目录

**输出文件命名格式**：  
`output_<调式>_<节奏函数名>_<音高函数名>.mid`

例如：`output_C_major_rhythm_fitness_active_pitch_fitness_stepwise.mid`

### 2. 播放生成的音乐

```bash
python playmid.py
```

自动扫描并播放所有`.mid`文件，按 `Ctrl+C` 跳过当前曲目。

### 3. 可视化分析

```bash
python visualmid.py      # 生成钢琴卷帘图
python evaluatemid.py    # 输出音高范围、时长等统计信息
```

## 编码方案

### 节奏基因（16位）

每个位置表示一个八分音符的节奏类型：
- `0` = 休止符（RHYTHM_REST）
- `1` = 发声/起拍（RHYTHM_NOTE）
- `2` = 延长记号（RHYTHM_HOLD）

**示例**：`[1, 2, 0, 1, 1, 2, 2, 0, ...]`  
表示：发声-延长-休止-发声-发声-延长-延长-休止...

### 音高基因（16位）

每个位置表示调式内的音级（0-6对应调式的7个音）：
- 在 C 大调中：`0`=C, `1`=D, `2`=E, `3`=F, `4`=G, `5`=A, `6`=B
- 在 A 小调中：`0`=A, `1`=B, `2`=C, `3`=D, `4`=E, `5`=F, `6`=G

**示例**：`[0, 2, 4, 2, 0, ...]`  
在C大调中表示：C-E-G-E-C...

### 解码机制

两个基因序列通过 `to_notes()` 方法合并解码：
- 只有节奏基因为 `1`（发声）的位置才会产生新音符
- 音符的音高由对应位置的音高基因决定
- `2`（延长）会延长当前音符
- `0`（休止）会产生休止符

## 适应度函数

### 节奏适应度函数（8个）

| 函数名 | 特点 | 适合风格 |
|--------|------|----------|
| `rhythm_fitness_basic` | 均衡分布 | 通用 |
| `rhythm_fitness_active` | 密集发声 | 快速、活泼 |
| `rhythm_fitness_legato` | 长音符 | 抒情、连贯 |
| `rhythm_fitness_syncopated` | 切分音 | 爵士、摇摆 |
| `rhythm_fitness_balanced` | 避免极端 | 自然、舒适 |
| `rhythm_fitness_sparse` | 多休止 | 留白、呼吸感 |
| `rhythm_fitness_march` | 强拍规律 | 进行曲 |
| `rhythm_fitness_varied` | 复杂多变 | 现代、实验 |

### 音高适应度函数（13个）

| 函数名 | 特点 | 适合风格 |
|--------|------|----------|
| `pitch_fitness_stepwise` | 级进运动 | 流畅、易唱 |
| `pitch_fitness_leap` | 跳跃音程 | 戏剧性 |
| `pitch_fitness_arch` | 拱形轮廓 | 经典乐句 |
| `pitch_fitness_wave` | 波浪起伏 | 动感 |
| `pitch_fitness_narrow_range` | 窄音域 | 平和、内敛 |
| `pitch_fitness_wide_range` | 宽音域 | 展现音域 |
| `pitch_fitness_end_tonic` | 结束主音 | 传统终止 |
| `pitch_fitness_avoid_repetition` | 避免重复 | 现代风格 |
| `pitch_fitness_variety` | 音高多样 | 丰富多彩 |
| `pitch_fitness_ascending` | 上行趋势 | 积极向上 |
| `pitch_fitness_descending` | 下行趋势 | 舒缓放松 |
| `pitch_fitness_center_focus` | 中心音 | 稳定回旋 |
| `pitch_fitness_pentatonic_feel` | 五声音阶 | 民族风格 |

## 遗传算法参数

- **种群大小**：200
- **最大代数**：1024
- **精英保留**：2个
- **交叉概率**：70%
- **变异概率**：5%
- **特殊变换概率**：3%

## 自定义适应度函数

### 添加节奏适应度函数

编辑 `fitness_function_rhythm.py`：

```python
def rhythm_fitness_custom(melody):
    """你的节奏评分逻辑"""
    rhythm = melody.rhythm_genes  # 访问节奏基因
    score = 0
    
    # 你的评分逻辑...
    
    return score

# 添加到导出列表
rhythm_fitness_funcs.append(rhythm_fitness_custom)
```

### 添加音高适应度函数

编辑 `fitness_function_pitch.py`：

```python
def pitch_fitness_custom(melody):
    """你的音高评分逻辑"""
    pitches = [n[0] for n in melody.notes]  # 获取所有音高
    pitch_genes = melody.pitch_genes         # 访问音高基因
    score = 0
    
    # 你的评分逻辑...
    
    return score

# 添加到导出列表
pitch_fitness_funcs.append(pitch_fitness_custom)
```

## 技术细节

### 遗传操作

1. **选择**：轮盘赌选择（基于总适应度）
2. **交叉**：单点交叉（节奏和音高独立交叉）
3. **变异**：
   - 节奏变异：随机改变节奏类型
   - 音高变异：随机改变音级
4. **特殊变换**：
   - 音高：移调、倒影、逆行
   - 节奏：增值、减值、逆行

### 适应度计算

每个个体的总适应度 = 节奏适应度 + 音高适应度

两个分数独立计算，便于观察各自的进化效果。

## 示例输出

运行完成后，你会得到类似以下的输出：

```
============================================================
  音乐遗传算法 - 节奏与音高独立进化
============================================================

已选择: C_major
音阶: [60, 62, 64, 65, 67, 69, 71]

[1/104] 组合: rhythm_fitness_basic_pitch_fitness_stepwise
============================================================
开始运行: rhythm_fitness_basic_pitch_fitness_stepwise
调式: [60, 62, 64, 65, 67, 69, 71]
============================================================
  第   0代: 总分= 245.00 (节奏= 50.00, 音高=195.00)
  第 200代: 总分= 380.00 (节奏= 80.00, 音高=300.00)
  第 400代: 总分= 425.00 (节奏=100.00, 音高=325.00)
  ...
✓ 已保存: output_C_major_rhythm_fitness_basic_pitch_fitness_stepwise.mid
```

## 常见问题

**Q: 如何只运行特定的适应度函数组合？**  
A: 在 `fitness_function_rhythm.py` 或 `fitness_function_pitch.py` 中，只保留你想要的函数在 `*_fitness_funcs` 列表中。

**Q: 如何调整进化速度？**  
A: 修改 `main.py` 中的 `MAX_GEN`（代数）或 `POP_SIZE`（种群大小）。

**Q: 生成的音乐太随机怎么办？**  
A: 增加适应度函数的权重，或者减少变异概率。

**Q: 如何添加更多调式？**  
A: 在 `main.py` 的 `SCALES` 字典中添加你想要的调式音阶。

## 许可证

本项目仅供学习和研究使用。

## 致谢

本项目结合了遗传算法、音乐理论和计算机音乐生成技术，感谢所有相关领域的研究成果。
