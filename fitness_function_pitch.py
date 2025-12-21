"""
音高适应度函数库（精简版）
Pitch Fitness Functions (Simplified)

只保留3个最核心的音高函数：
1. pitch_fitness_stepwise - 级进流畅
2. pitch_fitness_arch - 拱形轮廓
3. pitch_fitness_end_tonic - 结束主音
"""

# 导入配置
try:
    from config import PITCH_WEIGHTS
except ImportError:
    PITCH_WEIGHTS = {
        'stepwise': 2.0,
        'arch': 1.5,
        'end_tonic': 1.5,
    }


def pitch_fitness_stepwise(melody):
    """
    级进流畅旋律
    鼓励相邻音符以小音程连接，创造流畅、易唱的旋律
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


def pitch_fitness_arch(melody):
    """
    拱形轮廓旋律
    创造经典的拱形乐句：前半上升，后半下降，中间最高
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


def pitch_fitness_end_tonic(melody):
    """
    结束主音
    让旋律结束在主音上，创造完满的终止感
    """
    if not melody.notes:
        return 0
    
    # 检查音高基因
    if hasattr(melody, 'pitch_genes') and melody.pitch_genes:
        last_pitch_gene = melody.pitch_genes[-1]
        # 获取在音阶内的相对位置
        relative_position = last_pitch_gene % 7
        
        if relative_position == 0:  # 主音（任何八度）
            return 100
        elif relative_position == 2:  # 三音
            return 50
        elif relative_position == 4:  # 五音
            return 30
        else:
            return -20
    
    return 0


def pitch_fitness_overall(melody):
    """
    综合音高适应度（精简版）
    结合3个核心函数的加权组合
    """
    score = 0
    
    score += pitch_fitness_stepwise(melody) * PITCH_WEIGHTS['stepwise']
    score += pitch_fitness_arch(melody) * PITCH_WEIGHTS['arch']
    score += pitch_fitness_end_tonic(melody) * PITCH_WEIGHTS['end_tonic']
    
    return score


# ============================================================
# 导出函数列表
# ============================================================

pitch_fitness_funcs = [
    pitch_fitness_stepwise,
    pitch_fitness_arch,
    pitch_fitness_end_tonic,
    pitch_fitness_overall,
]

print(f"✓ 已加载 {len(pitch_fitness_funcs)} 个音高适应度函数（精简版）")
