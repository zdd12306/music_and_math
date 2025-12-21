"""
节奏适应度函数库（精简版）
Rhythm Fitness Functions (Simplified)

只保留3个最核心的节奏函数：
1. rhythm_fitness_basic - 基础平衡
2. rhythm_fitness_legato - 连贯流畅  
3. rhythm_fitness_balanced - 均衡自然
"""

# 导入配置
try:
    from config import RHYTHM_WEIGHTS
except ImportError:
    RHYTHM_WEIGHTS = {
        'basic': 1.5,
        'legato': 1.2,
        'balanced': 1.0,
    }


def rhythm_fitness_basic(melody):
    """
    基础平衡节奏
    创建平衡、自然的节奏模式
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


def rhythm_fitness_legato(melody):
    """
    连贯流畅节奏
    鼓励长音符、连贯的节奏，适合抒情音乐
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


def rhythm_fitness_balanced(melody):
    """
    均衡自然节奏
    避免极端，创造最自然、平衡的节奏
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


def rhythm_fitness_overall(melody):
    """
    综合节奏适应度（精简版）
    结合3个核心函数的加权组合
    """
    score = 0
    
    score += rhythm_fitness_basic(melody) * RHYTHM_WEIGHTS['basic']
    score += rhythm_fitness_legato(melody) * RHYTHM_WEIGHTS['legato']
    score += rhythm_fitness_balanced(melody) * RHYTHM_WEIGHTS['balanced']
    
    return score


# ============================================================
# 导出函数列表
# ============================================================

rhythm_fitness_funcs = [
    rhythm_fitness_basic,
    rhythm_fitness_legato,
    rhythm_fitness_balanced,
    rhythm_fitness_overall,
]

print(f"✓ 已加载 {len(rhythm_fitness_funcs)} 个节奏适应度函数（精简版）")
