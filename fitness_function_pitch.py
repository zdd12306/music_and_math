"""
音高适应度函数库
Pitch Fitness Functions

每个函数接收一个 MelodyAdapter 对象，该对象包含：
- melody.pitch_genes: 长度16的音高基因列表 [索引值对应调式内的音]
- melody.notes: 解码后的音符列表 [(pitch, start_time, duration), ...]
"""

def pitch_fitness_stepwise(melody):
    """
    级进旋律：鼓励相邻音程小
    适合：流畅、易唱的旋律
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    score = 0
    
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        if interval <= 2:  # 大二度以内
            score += 20
        elif interval <= 4:  # 小三度到大三度
            score += 5
        else:  # 大跳
            score -= 10
    
    return score


def pitch_fitness_leap(melody):
    """
    跳跃旋律：鼓励较大音程
    适合：戏剧性、张力强的旋律
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    score = 0
    
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        if interval >= 5:  # 纯四度及以上
            score += 25
        elif interval >= 3:  # 小三度及以上
            score += 10
        else:  # 级进
            score -= 5
    
    return score


def pitch_fitness_arch(melody):
    """
    拱形轮廓：前半上升，后半下降
    适合：经典的乐句形状
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    if len(pitches) < 4:
        return 0
    
    score = 0
    mid = len(pitches) // 2
    
    # 前半段奖励上升
    for i in range(mid - 1):
        if pitches[i+1] >= pitches[i]:
            score += 15
    
    # 后半段奖励下降
    for i in range(mid, len(pitches) - 1):
        if pitches[i+1] <= pitches[i]:
            score += 15
    
    # 中点应该是最高点
    if pitches[mid] == max(pitches):
        score += 50
    
    return score


def pitch_fitness_wave(melody):
    """
    波浪形：上下起伏
    适合：富有动感的旋律线条
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    score = 0
    
    # 检测方向变化
    direction_changes = 0
    for i in range(1, len(pitches) - 1):
        # 检测峰值或谷值
        if (pitches[i] > pitches[i-1] and pitches[i] > pitches[i+1]) or \
           (pitches[i] < pitches[i-1] and pitches[i] < pitches[i+1]):
            direction_changes += 1
    
    # 鼓励2-4次方向变化
    if 2 <= direction_changes <= 4:
        score += 100
    else:
        score += direction_changes * 10
    
    return score


def pitch_fitness_narrow_range(melody):
    """
    窄音域：控制在小范围内
    适合：平和、内敛的情绪
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    pitch_range = max(pitches) - min(pitches)
    
    score = 0
    
    # 音域在5个半音内（纯四度）
    if pitch_range <= 5:
        score += 100
    elif pitch_range <= 7:
        score += 50
    else:
        score -= (pitch_range - 7) * 10
    
    return score


def pitch_fitness_wide_range(melody):
    """
    宽音域：鼓励跨度大
    适合：展现音域的炫技式旋律
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    pitch_range = max(pitches) - min(pitches)
    
    score = 0
    
    # 音域在八度以上
    if pitch_range >= 12:
        score += 100
    elif pitch_range >= 7:
        score += 50
    else:
        score -= (7 - pitch_range) * 10
    
    return score


def pitch_fitness_end_tonic(melody):
    """
    结束主音：最后音落在主音（调式第一音）
    适合：传统、完满的终止感
    """
    if not melody.notes:
        return 0
    
    # 获取最后一个音符的实际音高（MIDI值）
    last_pitch = melody.notes[-1][0]
    
    # 计算其在12平均律中的音级（0=C, 1=C#, 2=D, ...）
    pitch_class = last_pitch % 12
    
    # 主音的音级（假设调式音阶第一个音是主音）
    # 例如C大调的主音是C(0)，D大调是D(2)，A小调是A(9)
    # 我们需要从scale的第一个音推断主音
    # 但这个信息在这里不可用，所以改用通用方法：
    # 奖励结束在任何八度的主音位置
    
    # 简化版本：检查是否结束在C, D, E, F, G, A这些常见主音上
    # 更好的方法是检查音高基因，看是否指向音阶的前几个音
    if hasattr(melody, 'pitch_genes') and melody.pitch_genes:
        last_pitch_gene = melody.pitch_genes[-1]
        # 假设音阶是按音高排序的
        # 前几个索引对应低音区的主音、三音、五音
        relative_position = last_pitch_gene % 7  # 获取在音阶内的相对位置
        
        if relative_position == 0:  # 主音（任何八度）
            return 100
        elif relative_position == 2:  # 三音
            return 50
        elif relative_position == 4:  # 五音
            return 30
        else:
            return -20
    
    return 0


def pitch_fitness_avoid_repetition(melody):
    """
    避免重复：惩罚相同音高连续出现
    适合：追求变化的现代风格
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    score = 0
    
    for i in range(len(pitches) - 1):
        if pitches[i] == pitches[i+1]:
            score -= 15  # 惩罚重复
        else:
            score += 5   # 奖励变化
    
    return score


def pitch_fitness_variety(melody):
    """
    音高多样性：使用更多不同音高
    适合：丰富多彩的音色组合
    """
    if not melody.pitch_genes:
        return 0
    
    unique_pitches = len(set(melody.pitch_genes))
    
    # 鼓励使用5个以上不同音高
    if unique_pitches >= 8:
        return 120
    elif unique_pitches >= 5:
        return 100
    elif unique_pitches >= 4:
        return 50
    else:
        return unique_pitches * 10


def pitch_fitness_ascending(melody):
    """
    上行旋律：整体趋势向上
    适合：积极、向上的情绪
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    score = 0
    
    # 起点和终点
    if len(pitches) >= 2:
        if pitches[-1] > pitches[0]:
            score += 50
    
    # 统计上行音程
    ascending = 0
    for i in range(len(pitches) - 1):
        if pitches[i+1] > pitches[i]:
            ascending += 1
    
    score += ascending * 15
    
    return score


def pitch_fitness_descending(melody):
    """
    下行旋律：整体趋势向下
    适合：舒缓、放松的情绪
    """
    if not melody.notes:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    score = 0
    
    # 起点和终点
    if len(pitches) >= 2:
        if pitches[-1] < pitches[0]:
            score += 50
    
    # 统计下行音程
    descending = 0
    for i in range(len(pitches) - 1):
        if pitches[i+1] < pitches[i]:
            descending += 1
    
    score += descending * 15
    
    return score


def pitch_fitness_center_focus(melody):
    """
    中心音聚焦：围绕某个中心音运动
    适合：稳定、回旋式的旋律
    """
    if not melody.pitch_genes:
        return 0
    
    # 找出最常出现的音高
    from collections import Counter
    counter = Counter(melody.pitch_genes)
    most_common_pitch, count = counter.most_common(1)[0]
    
    score = 0
    
    # 如果某个音出现频率高
    if count >= 4:
        score += count * 15
    
    # 如果中心音在音阶的主音位置（通过模运算检查相对位置）
    relative_position = most_common_pitch % 7
    if relative_position in [0, 2, 4]:  # 主音、三音或五音
        score += 50
    
    return score


def pitch_fitness_pentatonic_feel(melody):
    """
    五声音阶感：避免使用半音
    适合：民族风格、简朴的旋律
    """
    if not melody.notes or len(melody.notes) < 2:
        return 0
    
    score = 0
    pitches = [n[0] for n in melody.notes]
    
    # 统计半音进行（相邻音符相差1个半音）
    semitone_count = 0
    for i in range(len(pitches) - 1):
        if abs(pitches[i] - pitches[i+1]) == 1:
            semitone_count += 1
    
    # 惩罚半音进行（五声音阶避免半音）
    score -= semitone_count * 20
    
    # 奖励全音和大三度进行（五声特征）
    whole_tone_count = 0
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        if interval in [2, 4]:  # 全音或大三度
            whole_tone_count += 1
    score += whole_tone_count * 10
    
    return score


def pitch_fitness_overall(melody):
    """
    综合音高适应度：多个音高函数的加权组合
    这是推荐的默认音高评分函数
    """
    score = 0
    
    # 级进为主 (权重: 2.0)
    score += pitch_fitness_stepwise(melody) * 2.0
    
    # 少量跳跃 (权重: 0.5)
    score += pitch_fitness_leap(melody) * 0.5
    
    # 拱形轮廓 (权重: 1.5)
    score += pitch_fitness_arch(melody) * 1.5
    
    # 波浪起伏 (权重: 1.0)
    score += pitch_fitness_wave(melody) * 1.0
    
    # 中等音域 (权重: 0.8)
    # 同时考虑窄音域和宽音域，取平衡
    narrow_score = pitch_fitness_narrow_range(melody)
    wide_score = pitch_fitness_wide_range(melody)
    score += (narrow_score * 0.3 + wide_score * 0.5)
    
    # 结束在主音 (权重: 1.5)
    score += pitch_fitness_end_tonic(melody) * 1.5
    
    # 避免过度重复 (权重: 1.0)
    score += pitch_fitness_avoid_repetition(melody) * 1.0
    
    # 音高多样性 (权重: 1.2)
    score += pitch_fitness_variety(melody) * 1.2
    
    # 轻微上行倾向 (权重: 0.3)
    score += pitch_fitness_ascending(melody) * 0.3
    
    # 中心音聚焦 (权重: 0.5)
    score += pitch_fitness_center_focus(melody) * 0.5
    
    # 避免半音进行 (权重: 0.8)
    score += pitch_fitness_pentatonic_feel(melody) * 0.8
    
    return score


# ============================================================
# 导出函数列表
# ============================================================

pitch_fitness_funcs = [
    pitch_fitness_stepwise,
    pitch_fitness_leap,
    pitch_fitness_arch,
    pitch_fitness_wave,
    pitch_fitness_narrow_range,
    pitch_fitness_wide_range,
    pitch_fitness_end_tonic,
    pitch_fitness_avoid_repetition,
    pitch_fitness_variety,
    pitch_fitness_ascending,
    pitch_fitness_descending,
    pitch_fitness_center_focus,
    pitch_fitness_pentatonic_feel,
    pitch_fitness_overall,  # 综合函数
]

print(f"✓ 已加载 {len(pitch_fitness_funcs)} 个音高适应度函数（含1个综合函数）")

