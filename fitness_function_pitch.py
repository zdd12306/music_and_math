"""
音高适应度函数库
Pitch Fitness Functions

音高适应度函数：
1. pitch_fitness_stepwise - 级进流畅（鼓励小音程）
2. pitch_fitness_consonance - 音程协和度（鼓励协和音程）
3. pitch_fitness_range - 音域平衡（鼓励适中的音域范围）
4. pitch_fitness_direction - 旋律方向变化（避免单一方向）
5. pitch_fitness_climax - 旋律高潮（鼓励有明显的最高/最低音）
"""

# 导入配置
try:
    from config import PITCH_WEIGHTS
except ImportError:
    PITCH_WEIGHTS = {
        'stepwise': 1.0,
        'consonance': 1.0,
        'range': 1.0,
        'direction': 1.0,
        'climax': 1.0,
    }


def pitch_fitness_stepwise(melody):
    """
    级进流畅旋律（归一化版本）
    鼓励相邻音符以小音程连接，创造流畅、易唱的旋律
    
    评分规则：
    - 大二度以内（间隔≤2）：+20分
    - 小三度到大三度（间隔3-4）：+5分
    - 大跳（间隔>4）：-10分
    
    归一化：
    - 得分除以音程数量，避免音符数量影响得分
    - 返回平均音程质量分数
    """
    if not melody.notes or len(melody.notes) < 2:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    
    # 计算音程质量得分
    interval_score = 0
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        if interval <= 2:  # 大二度以内（级进）
            interval_score += 20
        elif interval <= 4:  # 小三度到大三度（小跳）
            interval_score += 5
        else:  # 大跳
            interval_score -= 10
    
    # 归一化：除以音程数量，得到平均质量
    num_intervals = len(pitches) - 1
    if num_intervals > 0:
        normalized_score = interval_score / num_intervals
    else:
        normalized_score = 0
    
    return normalized_score


def pitch_fitness_consonance(melody):
    """
    音程协和度评估（归一化版本 - 平衡评分）
    根据音乐理论，评估相邻音符之间音程的协和程度
    
    评分设计：使各种协和音程得分接近，鼓励音程多样性
    
    音程分类（半音数）：
    
    特殊情况：
    - 相邻音符相同 (0)：-15分（惩罚，避免单调重复）
    
    协和音程（Consonance） - 平衡评分：
    - 纯八度 (12)：+12分（降低，避免偏向八度）
    - 纯五度 (7)：+12分（提高，鼓励使用）
    - 纯四度 (5)：+12分（提高，鼓励使用）
    - 大三度 (4)：+12分（提高，鼓励使用）
    - 小三度 (3)：+12分（提高，鼓励使用）
    - 大六度 (9)：+10分（稍微提高）
    - 小六度 (8)：+10分（稍微提高）
    
    不协和音程（Dissonance）：
    - 大二度 (2)：+5分（轻微不协和，可接受）
    - 小二度 (1)：-5分（较强不协和）
    - 三全音 (6)：-10分（最强不协和）
    - 小七度 (10)：-5分
    - 大七度 (11)：-10分
    
    超过八度的音程：
    - 按照取模12后的音程计算
    
    归一化：
    - 得分除以音程数量，返回平均协和度
    
    设计理念：
    - 所有主要协和音程（八度、五度、四度、三度）得分相同（12分）
    - 避免遗传算法只选择八度音程
    - 鼓励使用多样化的协和音程
    """
    if not melody.notes or len(melody.notes) < 2:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    
    # 计算协和度得分
    consonance_score = 0
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        
        # 将大于12的音程归约到一个八度内
        interval_class = interval % 12
        
        # 根据音程类型评分（平衡版本）
        if interval == 0:  # 相邻音符相同（重复音）
            consonance_score -= 15  # 惩罚，避免单调
        elif interval_class == 12 or interval == 12:  # 纯八度
            consonance_score += 12  # 降低，避免偏向
        elif interval_class == 7:  # 纯五度
            consonance_score += 12  # 提高，鼓励
        elif interval_class == 5:  # 纯四度
            consonance_score += 12  # 提高，鼓励
        elif interval_class in [3, 4]:  # 小三度、大三度
            consonance_score += 12  # 提高，鼓励
        elif interval_class in [8, 9]:  # 小六度、大六度
            consonance_score += 10  # 稍微提高
        elif interval_class == 2:  # 大二度
            consonance_score += 5
        elif interval_class == 1:  # 小二度
            consonance_score -= 5
        elif interval_class == 6:  # 三全音（增四度/减五度）
            consonance_score -= 10
        elif interval_class == 10:  # 小七度
            consonance_score -= 5
        elif interval_class == 11:  # 大七度
            consonance_score -= 10
    
    # 归一化：除以音程数量，得到平均协和度
    num_intervals = len(pitches) - 1
    if num_intervals > 0:
        normalized_score = consonance_score / num_intervals
    else:
        normalized_score = 0
    
    return normalized_score


def pitch_fitness_range(melody):
    """
    音域平衡（归一化版本）
    评估旋律的音域范围是否适中
    
    评分规则：
    - 理想音域范围：8-16个半音（约1-1.5个八度）
    - 太窄（<6）：单调，-10分
    - 适中（6-18）：+20分
    - 太宽（>18）：难唱，-5分
    
    设计理念：
    - 鼓励适中的音域范围
    - 避免音域过窄（单调）或过宽（难演唱）
    """
    if not melody.notes or len(melody.notes) < 2:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    
    # 计算音域范围（最高音 - 最低音）
    pitch_range = max(pitches) - min(pitches)
    
    # 根据音域范围评分
    if pitch_range < 6:  # 太窄（小于半个八度）
        score = -10
    elif 6 <= pitch_range <= 18:  # 适中（0.5 - 1.5个八度）
        score = 20
    else:  # 太宽（大于1.5个八度）
        score = -5
    
    return score


def pitch_fitness_direction(melody):
    """
    旋律方向变化（归一化版本）
    评估旋律的方向变化是否丰富
    
    评分规则：
    - 统计方向变化次数（上行→下行，下行→上行）
    - 方向变化多 = 旋律起伏丰富 → 高分
    - 单一方向 = 单调 → 低分
    
    归一化：
    - 方向变化比例 × 20
    
    设计理念：
    - 鼓励旋律有起伏变化
    - 避免持续上行或下行
    """
    if not melody.notes or len(melody.notes) < 3:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    
    # 计算每个音程的方向（+1上行，-1下行，0持平）
    directions = []
    for i in range(len(pitches) - 1):
        diff = pitches[i+1] - pitches[i]
        if diff > 0:
            directions.append(1)  # 上行
        elif diff < 0:
            directions.append(-1)  # 下行
        else:
            directions.append(0)  # 持平
    
    # 统计方向变化次数
    direction_changes = 0
    for i in range(len(directions) - 1):
        # 方向发生变化（上→下 或 下→上）
        if directions[i] != 0 and directions[i+1] != 0:
            if directions[i] != directions[i+1]:
                direction_changes += 1
    
    # 归一化：方向变化比例
    if len(directions) > 1:
        change_ratio = direction_changes / (len(directions) - 1)
        score = change_ratio * 20  # 满分20
    else:
        score = 0
    
    return score


def pitch_fitness_climax(melody):
    """
    旋律高潮（归一化版本）
    评估旋律是否有明显的高潮点（最高音或最低音）
    
    评分规则：
    - 最高音/最低音不在开头或结尾 → +15分（有高潮）
    - 最高音和最低音都在中间 → +25分（最优）
    - 最高音/最低音在开头或结尾 → 0分（平淡）
    
    设计理念：
    - 鼓励旋律有明显的高潮点
    - 避免开头或结尾就是极值（缺乏张力）
    """
    if not melody.notes or len(melody.notes) < 4:
        return 0
    
    pitches = [n[0] for n in melody.notes]
    n = len(pitches)
    
    # 找到最高音和最低音的位置
    max_pitch_idx = pitches.index(max(pitches))
    min_pitch_idx = pitches.index(min(pitches))
    
    score = 0
    
    # 检查最高音位置（不在开头或结尾）
    if 0 < max_pitch_idx < n - 1:
        score += 12.5
    
    # 检查最低音位置（不在开头或结尾）
    if 0 < min_pitch_idx < n - 1:
        score += 12.5
    
    return score


def pitch_fitness_overall(melody):
    """
    综合音高适应度
    所有音高适应度函数的简单相加（根据权重决定是否启用）
    权重=0表示不使用该函数，>0表示使用
    """
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


# ============================================================
# 导出函数列表
# ============================================================

pitch_fitness_funcs = [
    pitch_fitness_stepwise,
    pitch_fitness_consonance,
    pitch_fitness_range,
    pitch_fitness_direction,
    pitch_fitness_climax,
    pitch_fitness_overall,
]

print(f"✓ 已加载 {len(pitch_fitness_funcs)} 个音高适应度函数")
