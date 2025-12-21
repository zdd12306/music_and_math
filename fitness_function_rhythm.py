"""
节奏适应度函数库
Rhythm Fitness Functions

节奏适应度函数：
1. rhythm_fitness_parity - 节奏奇性（避免对称的起拍）
2. rhythm_fitness_density - 节奏密度（控制音符密度）
3. rhythm_fitness_syncopation - 切分音（鼓励节奏变化）
4. rhythm_fitness_rest - 休止符分布（鼓励适当的休止）
5. rhythm_fitness_pattern - 节奏模式（鼓励有规律的节奏）
"""

# 导入配置
try:
    from config import RHYTHM_WEIGHTS
except ImportError:
    RHYTHM_WEIGHTS = {
        'parity': 1.0,
        'density': 1.0,
        'syncopation': 1.0,
        'rest': 1.0,
        'pattern': 1.0,
    }


def rhythm_fitness_parity(melody):
    """
    节奏奇性（最基础的节奏适应度函数）
    
    定义：起拍的对径点不要是起拍
    
    原理：
    - 在节奏序列中，如果位置 i 是起拍（rhythm[i] == 1），
      那么它的对径点位置（序列另一端的对称位置）不应该也是起拍
    - 这样可以避免节奏过于对称和单调，增加节奏的多样性
    
    评分规则：
    - 对于每一对对径点(i, mirror_i)：
      * 如果都是起拍（1） → -30分（惩罚对称）
      * 如果不对称 → +10分（奖励多样性）
    
    例如：
    序列长度为16: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    - 位置0的对径点是位置15
    - 位置1的对径点是位置14
    - 位置7的对径点是位置8
    """
    if not hasattr(melody, 'rhythm_genes') or not melody.rhythm_genes:
        return 0
    
    rhythm = melody.rhythm_genes
    n = len(rhythm)
    score = 0
    
    # 检查每个位置及其对径点
    # 只需要检查前半部分，避免重复计算
    for i in range(n // 2):
        mirror_i = i + (n // 2) # 对径点位置
        
        # 如果当前位置是起拍（发声）
        if rhythm[i] == 1:
            # 检查对径点
            if rhythm[mirror_i] == 1:
                # 对径点也是起拍 → 惩罚（过于对称）
                score -= 30
            else:
                # 对径点不是起拍 → 奖励（满足奇性）
                score += 10
        
        # 如果当前位置不是起拍，但对径点是起拍
        elif rhythm[mirror_i] == 1:
            # 这种情况下奇性也满足 → 奖励
            score += 10
    
    # 如果序列长度是奇数，中心点不需要检查对径
    # （因为它自己就是自己的对径点）
    
    return score


def rhythm_fitness_density(melody):
    """
    节奏密度
    评估音符密度是否适中
    
    评分规则：
    - 统计起拍（1）、延长（2）、休止（0）的比例
    - 理想比例：起拍 40-55%（相对密集但不过分）
    - 太密（>65%）：-20分
    - 太疏（<30%）：-20分
    - 适中（40-55%）：+20分
    - 稍偏离（30-40%或55-65%）：+10分
    
    设计理念：
    - 避免过于密集或稀疏的节奏
    - 鼓励有呼吸感的节奏分布
    - 对于32个位置，40-55%起拍意味着13-18个音符
    """
    if not hasattr(melody, 'rhythm_genes') or not melody.rhythm_genes:
        return 0
    
    rhythm = melody.rhythm_genes
    n = len(rhythm)
    
    # 统计起拍数量
    note_count = rhythm.count(1)
    note_ratio = note_count / n
    
    # 根据密度评分
    if 0.40 <= note_ratio <= 0.55:  # 最理想（40-55%）
        score = 20
    elif 0.30 <= note_ratio < 0.40 or 0.55 < note_ratio <= 0.65:  # 稍偏离
        score = 10
    elif note_ratio > 0.65:  # 太密
        score = -20
    elif note_ratio < 0.30:  # 太疏
        score = -20
    else:
        score = 0
    
    return score


def rhythm_fitness_syncopation(melody):
    """
    切分音评估
    鼓励节奏变化，避免过于规律
    
    评分规则：
    - 检查连续的起拍之间的间隔
    - 间隔多样化 → 高分（有切分感）
    - 间隔单一 → 低分（过于规律）
    
    归一化：
    - 间隔种类数 / 理论最大种类数 × 20
    
    设计理念：
    - 鼓励不同长度的音符
    - 避免机械般规律的节奏
    """
    if not hasattr(melody, 'rhythm_genes') or not melody.rhythm_genes:
        return 0
    
    rhythm = melody.rhythm_genes
    
    # 找到所有起拍的位置
    note_positions = [i for i, r in enumerate(rhythm) if r == 1]
    
    if len(note_positions) < 2:
        return 0
    
    # 计算连续起拍之间的间隔
    intervals = []
    for i in range(len(note_positions) - 1):
        interval = note_positions[i+1] - note_positions[i]
        intervals.append(interval)
    
    # 计算间隔的多样性
    unique_intervals = len(set(intervals))
    max_possible = min(len(intervals), 8)  # 理论最大种类数
    
    if max_possible > 0:
        diversity_ratio = unique_intervals / max_possible
        score = diversity_ratio * 20
    else:
        score = 0
    
    return score


def rhythm_fitness_rest(melody):
    """
    休止符分布
    评估休止符是否合理分布
    
    评分规则：
    - 休止符数量适中（2-4个）→ +20分（最理想）
    - 休止符稍多（5-6个）→ +10分
    - 休止符过多（>6）→ -10分
    - 没有休止符 → -15分（完全没有呼吸）
    - 休止符分散（不连续）→ +5分
    
    设计理念：
    - 鼓励少量适当的休止（音乐需要呼吸）
    - 避免过多休止（太空）或没有休止（太满）
    - 对于32个位置，2-4个休止符约占6-12%，比较合理
    """
    if not hasattr(melody, 'rhythm_genes') or not melody.rhythm_genes:
        return 0
    
    rhythm = melody.rhythm_genes
    
    # 统计休止符数量
    rest_count = rhythm.count(0)
    
    score = 0
    
    # 根据休止符数量评分（更严格的标准）
    if 2 <= rest_count <= 4:  # 最理想（6-12%）
        score += 20
    elif 5 <= rest_count <= 6:  # 稍多但可接受
        score += 10
    elif rest_count > 6:  # 太多
        score -= 10
    elif rest_count == 0:  # 没有
        score -= 15
    
    # 检查休止符是否分散（不连续）
    consecutive_rests = 0
    max_consecutive = 0
    for r in rhythm:
        if r == 0:
            consecutive_rests += 1
            max_consecutive = max(max_consecutive, consecutive_rests)
        else:
            consecutive_rests = 0
    
    # 如果休止符分散（最长连续不超过2个）
    if rest_count > 0 and max_consecutive <= 2:
        score += 5
    
    return score


def rhythm_fitness_pattern(melody):
    """
    节奏模式
    评估节奏是否有一定的规律性
    
    评分规则：
    - 将节奏序列分成前半段和后半段
    - 如果有部分相似的模式 → +10分
    - 检测简单的重复模式（如 [1,2,0] 重复）→ +15分
    
    设计理念：
    - 鼓励节奏有一定的规律感
    - 但不要过于机械重复
    """
    if not hasattr(melody, 'rhythm_genes') or not melody.rhythm_genes:
        return 0
    
    rhythm = melody.rhythm_genes
    n = len(rhythm)
    
    score = 0
    
    # 检测2-4拍的重复模式
    for pattern_len in [2, 3, 4]:
        if n >= pattern_len * 2:
            # 检查是否有重复的模式
            patterns = []
            for i in range(n - pattern_len + 1):
                pattern = tuple(rhythm[i:i+pattern_len])
                patterns.append(pattern)
            
            # 如果某个模式出现2次以上
            from collections import Counter
            pattern_counts = Counter(patterns)
            if pattern_counts.most_common(1)[0][1] >= 2:
                score += 10
                break  # 找到一个就够了
    
    return score


def rhythm_fitness_overall(melody):
    """
    综合节奏适应度
    所有节奏适应度函数的简单相加（根据权重决定是否启用）
    权重=0表示不使用该函数，>0表示使用
    """
    total_score = 0
    
    # 根据权重决定是否计算每个函数
    if RHYTHM_WEIGHTS.get('parity', 0) != 0:
        total_score += rhythm_fitness_parity(melody)
    
    if RHYTHM_WEIGHTS.get('density', 0) != 0:
        total_score += rhythm_fitness_density(melody)
    
    if RHYTHM_WEIGHTS.get('syncopation', 0) != 0:
        total_score += rhythm_fitness_syncopation(melody)
    
    if RHYTHM_WEIGHTS.get('rest', 0) != 0:
        total_score += rhythm_fitness_rest(melody)
    
    if RHYTHM_WEIGHTS.get('pattern', 0) != 0:
        total_score += rhythm_fitness_pattern(melody)
    
    return total_score


# ============================================================
# 导出函数列表
# ============================================================

rhythm_fitness_funcs = [
    rhythm_fitness_parity,
    rhythm_fitness_density,
    rhythm_fitness_syncopation,
    rhythm_fitness_rest,
    rhythm_fitness_pattern,
    rhythm_fitness_overall,
]

print(f"✓ 已加载 {len(rhythm_fitness_funcs)} 个节奏适应度函数")
