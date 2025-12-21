"""
节奏适应度函数库
Rhythm Fitness Functions

每个函数接收一个 MelodyAdapter 对象，该对象包含：
- melody.rhythm_genes: 长度16的节奏基因列表
  [0=休止符, 1=发声, 2=延长]
- melody.notes: 解码后的音符列表 [(pitch, start_time, duration), ...]
"""

def rhythm_fitness_basic(melody):
    """
    基础节奏评分：鼓励多样性
    适合：均衡的节奏模式
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    # 统计各类型数量
    note_count = rhythm.count(1)  # RHYTHM_NOTE
    hold_count = rhythm.count(2)  # RHYTHM_HOLD
    rest_count = rhythm.count(0)  # RHYTHM_REST
    
    # 鼓励平衡的节奏分布
    if 4 <= note_count <= 8:
        score += 50
    if 2 <= rest_count <= 5:
        score += 30
    if hold_count >= 2:
        score += 20
    
    return score


def rhythm_fitness_active(melody):
    """
    活跃节奏：鼓励更多发声
    适合：快速、密集的音乐风格
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    note_count = rhythm.count(1)
    rest_count = rhythm.count(0)
    
    # 高密度音符
    score += note_count * 15
    # 惩罚过多休止
    score -= rest_count * 10
    
    # 奖励连续的音符
    consecutive_notes = 0
    for i in range(len(rhythm) - 1):
        if rhythm[i] == 1 and rhythm[i+1] == 1:
            consecutive_notes += 1
    score += consecutive_notes * 5
    
    return score


def rhythm_fitness_legato(melody):
    """
    连贯节奏：鼓励长音符（更多HOLD）
    适合：抒情、连贯的旋律
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    hold_count = rhythm.count(2)
    note_count = rhythm.count(1)
    
    # 鼓励延长记号
    score += hold_count * 20
    
    # 计算平均音符长度
    if note_count > 0:
        avg_length = (note_count + hold_count) / note_count
        if avg_length >= 2:
            score += 50
    
    # 惩罚过于碎片化
    fragment_count = 0
    for i in range(len(rhythm) - 1):
        if rhythm[i] == 1 and rhythm[i+1] != 2:
            fragment_count += 1
    score -= fragment_count * 5
    
    return score


def rhythm_fitness_syncopated(melody):
    """
    切分节奏：鼓励强弱位对比
    适合：爵士、摇摆风格
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    # 检查强拍位置（0, 4, 8, 12 是每拍的开始）
    strong_beats = [0, 4, 8, 12]
    weak_beats = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]
    
    # 弱拍上有音符（切分音）
    syncopation = 0
    for pos in weak_beats:
        if rhythm[pos] == 1:
            syncopation += 1
    score += syncopation * 10
    
    # 强拍上的休止（反常规）
    for pos in strong_beats:
        if rhythm[pos] == 0:
            score += 15
    
    return score


def rhythm_fitness_balanced(melody):
    """
    平衡节奏：避免极端
    适合：自然、舒适的节奏感
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    note_count = rhythm.count(1)
    hold_count = rhythm.count(2)
    rest_count = rhythm.count(0)
    
    # 鼓励均衡分布
    total = len(rhythm)
    ideal_notes = total * 0.4
    ideal_holds = total * 0.3
    ideal_rests = total * 0.3
    
    # 距离理想值越近得分越高
    score -= abs(note_count - ideal_notes) * 5
    score -= abs(hold_count - ideal_holds) * 3
    score -= abs(rest_count - ideal_rests) * 3
    
    # 鼓励交替模式
    alternations = 0
    for i in range(len(rhythm) - 1):
        if rhythm[i] != rhythm[i+1]:
            alternations += 1
    score += alternations * 2
    
    return score


def rhythm_fitness_sparse(melody):
    """
    稀疏节奏：鼓励更多休止符
    适合：留白、呼吸感强的音乐
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    rest_count = rhythm.count(0)
    note_count = rhythm.count(1)
    
    # 鼓励休止符
    score += rest_count * 15
    
    # 惩罚过密
    if note_count > 6:
        score -= (note_count - 6) * 10
    
    # 鼓励休止符分散在不同位置
    rest_positions = [i for i, r in enumerate(rhythm) if r == 0]
    if len(rest_positions) >= 2:
        # 计算休止符之间的间距
        gaps = [rest_positions[i+1] - rest_positions[i] for i in range(len(rest_positions)-1)]
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        if avg_gap >= 3:  # 休止符分散开
            score += 30
    
    return score


def rhythm_fitness_march(melody):
    """
    进行曲节奏：强调强拍
    适合：庄严、有力的风格
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    # 强拍位置（每拍开始）
    strong_beats = [0, 4, 8, 12]
    
    # 强拍上应该有音符
    for pos in strong_beats:
        if rhythm[pos] == 1:
            score += 30
        elif rhythm[pos] == 2:  # 延长也可以
            score += 15
    
    # 鼓励规律的节奏模式
    # 检查是否有重复的4拍模式
    pattern1 = rhythm[0:4]
    pattern2 = rhythm[4:8]
    pattern3 = rhythm[8:12]
    pattern4 = rhythm[12:16]
    
    if pattern1 == pattern2 or pattern2 == pattern3 or pattern3 == pattern4:
        score += 40
    
    return score


def rhythm_fitness_varied(melody):
    """
    变化节奏：鼓励复杂的节奏组合
    适合：现代、实验性音乐
    """
    rhythm = melody.rhythm_genes
    score = 0
    
    # 检查所有2音符子序列的多样性
    pairs = [tuple(rhythm[i:i+2]) for i in range(len(rhythm)-1)]
    unique_pairs = len(set(pairs))
    score += unique_pairs * 10
    
    # 检查所有3音符子序列的多样性
    triplets = [tuple(rhythm[i:i+3]) for i in range(len(rhythm)-2)]
    unique_triplets = len(set(triplets))
    score += unique_triplets * 8
    
    # 避免长重复
    for i in range(len(rhythm) - 3):
        if rhythm[i] == rhythm[i+1] == rhythm[i+2] == rhythm[i+3]:
            score -= 20
    
    return score


# ============================================================
# 导出函数列表
# ============================================================

rhythm_fitness_funcs = [
    rhythm_fitness_basic,
    rhythm_fitness_active,
    rhythm_fitness_legato,
    rhythm_fitness_syncopated,
    rhythm_fitness_balanced,
    rhythm_fitness_sparse,
    rhythm_fitness_march,
    rhythm_fitness_varied,
]

print(f"✓ 已加载 {len(rhythm_fitness_funcs)} 个节奏适应度函数")

