"""
音高适应度函数库
Pitch Fitness Functions

每个函数接收一个 MelodyAdapter 对象，该对象包含：
- melody.pitch_genes: 长度16的音高基因列表 [0-6对应调式内的7个音]
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
    if not melody.notes or not melody.pitch_genes:
        return 0
    
    # 检查最后一个音高基因是否为0（主音）
    last_pitch_gene = melody.pitch_genes[-1]
    
    if last_pitch_gene == 0:
        return 100
    elif last_pitch_gene == 2:  # 三音也可以
        return 50
    elif last_pitch_gene == 4:  # 五音也行
        return 30
    else:
        return -20


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
    
    # 鼓励使用5-7个不同音高
    if unique_pitches >= 5:
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
    
    # 如果中心音是主音、三音或五音
    if most_common_pitch in [0, 2, 4]:
        score += 50
    
    return score


def pitch_fitness_pentatonic_feel(melody):
    """
    五声音阶感：主要使用调式中的前5音
    适合：民族风格、简朴的旋律
    """
    if not melody.pitch_genes:
        return 0
    
    score = 0
    
    # 统计前5音的使用
    pentatonic_notes = [0, 1, 2, 4, 5]  # 对应五声音阶常用音级
    pentatonic_count = sum(1 for p in melody.pitch_genes if p in pentatonic_notes)
    
    # 鼓励多用五声音阶
    score += pentatonic_count * 10
    
    # 惩罚使用6音（导音）
    avoid_count = melody.pitch_genes.count(6)
    score -= avoid_count * 15
    
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
]

print(f"✓ 已加载 {len(pitch_fitness_funcs)} 个音高适应度函数")

