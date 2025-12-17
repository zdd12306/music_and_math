import numpy as np
import math

# 尝试导入 muspy，如果没有安装，则提供降级处理或报错提示
try:
    import muspy
    MUSPY_AVAILABLE = True
except ImportError:
    MUSPY_AVAILABLE = False
    print("Warning: MusPy not installed. fitness_function_muspy will return 0.")

# === 基础乐理常量 ===
# C 大调音阶 (C, D, E, F, G, A, B)
SCALE_C_MAJOR = {0, 2, 4, 5, 7, 9, 11}
# 主和弦音 (C, E, G)
CHORD_C_MAJOR = {0, 4, 7}

# === 适应度函数定义 ===

def fitness_function_random(melody):
    return len(melody.notes)

def fitness_function_c_major(melody):
    score = 0
    # melody.notes 格式为 [(pitch, duration), ...]
    pitches = [n[0] for n in melody.notes]
    for p in pitches:
        if p % 12 in SCALE_C_MAJOR:
            score += 10 # 奖励调内音
        else:
            score -= 10 # 严厉惩罚调外音
    return score

def fitness_function_end_c(melody):
    score = fitness_function_c_major(melody) # 继承上一级规则
    
    if not melody.notes: return 0
    
    last_pitch = melody.notes[-1][0]
    # 如果结束音是 C (0, 12, 24...)
    if last_pitch % 12 == 0:
        score += 50
    else:
        score -= 20
    return score

def fitness_function_diff(melody):
    score = 0
    pitches = [n[0] for n in melody.notes]
    
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        if interval <= 2:   # 级进 (1或2个半音)
            score += 10
        elif interval > 7:  # 大跳 (>纯五度)
            score -= 10
    return score

def fitness_function_stepwise(melody):
    # 简单的加权组合
    score_tonality = fitness_function_end_c(melody)
    score_flow = fitness_function_diff(melody)
    return score_tonality + score_flow

def fitness_function_anti_boredom(melody):
    score = fitness_function_stepwise(melody) # 继承标准旋律
    pitches = [n[0] for n in melody.notes]
    
    # 惩罚重复音
    for i in range(len(pitches) - 1):
        if pitches[i] == pitches[i+1]:
            score -= 15 # 惩罚重复
    return score

def fitness_function_7(melody):
    pitches = [n[0] for n in melody.notes]
    if not pitches: return 0
    
    mid_point = len(pitches) // 2
    score = 0
    
    # 前半段奖励上升
    for i in range(mid_point):
        if i+1 < len(pitches) and pitches[i+1] > pitches[i]:
            score += 10
            
    # 后半段奖励下降
    for i in range(mid_point, len(pitches)-1):
        if pitches[i+1] < pitches[i]:
            score += 10
            
    # 叠加调性约束
    return score + fitness_function_c_major(melody)

def fitness_function_8(melody):
    score = 0
    pitches = [n[0] for n in melody.notes]
    
    # 基础调性
    score += fitness_function_c_major(melody) * 0.5 
    
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        # 3(小三度), 4(大三度), 7(纯五度), 12(八度)
        if interval in [3, 4, 7, 12]:
            score += 20 
        elif interval <= 2: # 稍微惩罚级进，鼓励跳跃
            score -= 5
            
    return score

def fitness_function_9(melody):
    pitches = [n[0] for n in melody.notes]
    if not pitches: return 0
    
    score = fitness_function_c_major(melody)
    
    # 计算音域 (Range)
    pitch_range = max(pitches) - min(pitches)
    
    # 如果音域控制在 5 个半音内 (比如 Do 到 Fa)，给高分
    if pitch_range <= 5:
        score += 100
    elif pitch_range > 12:
        score -= 50 # 惩罚大跨度
        
    return score

def fitness_function_10(melody):
    score = fitness_function_stepwise(melody) # 基础好听
    durations = [n[1] for n in melody.notes]
    
    for d in durations:
        if d == 0.5: # 八分音符
            score += 10
        elif d >= 2.0: # 二分音符以上
            score -= 5 # 惩罚太长
            
    # 奖励节奏变化：如果相邻两个音符时值不同
    for i in range(len(durations)-1):
        if durations[i] != durations[i+1]:
            score += 5
            
    return score

def fitness_function_11(melody):
    pitches = [n[0] for n in melody.notes]
    durations = [n[1] for n in melody.notes]
    
    score = 0
    
    # 1. 调性 (基础分)
    score += fitness_function_c_major(melody)
    
    # 2. 骨干音奖励 (C, E, G)
    for p in pitches:
        if p % 12 in CHORD_C_MAJOR:
            score += 5
            
    # 3. 完美的结束
    if pitches[-1] % 12 == 0: # 结束在 C
        score += 40
    elif pitches[-1] % 12 == 4: # 结束在 E (也可以)
        score += 20
        
    # 4. 惩罚过大的跳跃，但允许八度
    jumps = 0
    for i in range(len(pitches) - 1):
        interval = abs(pitches[i] - pitches[i+1])
        if interval > 8 and interval != 12:
            jumps += 1
    score -= jumps * 15
    
    # 5. 节奏多样性 (如果全是同样的节奏，扣分)
    if len(set(durations)) == 1:
        score -= 30
        
    return score

# === 辅助工具：转换为 MusPy 对象 ===

def convert_to_muspy(melody):
    """
    将自定义的 Melody 对象转换为 muspy.Music 对象
    """
    if not MUSPY_AVAILABLE:
        return None

    # 设定解析度：24 ticks = 1 quarter note (1 beat)
    # 所以 0.5 beat (eighth note) = 12 ticks
    resolution = 24 
    
    music = muspy.Music(resolution=resolution)
    track = muspy.Track(program=0, is_drum=False)
    
    current_time_ticks = 0
    
    # 确保 melody.notes 不为空
    if not melody.notes:
        return music

    for pitch, duration_beats in melody.notes:
        duration_ticks = int(duration_beats * resolution)
        
        note = muspy.Note(
            time=current_time_ticks,
            pitch=int(pitch),
            duration=duration_ticks,
            velocity=100
        )
        track.notes.append(note)
        current_time_ticks += duration_ticks
        
    music.tracks.append(track)
    return music

def fitness_function_muspy(melody):
    # 1. 基础检查
    if not melody.notes or not MUSPY_AVAILABLE:
        return 0
        
    try:
        # 2. 转换格式
        m_obj = convert_to_muspy(melody)
        if not m_obj or not m_obj.tracks[0].notes:
            return 0
        
        # 3. 计算指标
        # scale_consistency: 0.0 ~ 1.0
        score_scale = muspy.scale_consistency(m_obj)
        
        # pitch_entropy: 音高熵
        entropy = muspy.pitch_entropy(m_obj)
        
        # 目标熵值 3.0，距离越远分越低
        target_entropy = 3.0
        score_entropy = 1.0 / (1.0 + abs(entropy - target_entropy))
        
        # 4. 最终加权 (放大100倍)
        total_score = (score_scale * 70) + (score_entropy * 30)
        
        if np.isnan(total_score):
            return 0
            
        return total_score
        
    except Exception as e:
        print(f"MusPy Error: {e}")
        return 0

# === 函数列表导出 ===
funcs = [
    fitness_function_random,
    fitness_function_c_major,
    fitness_function_end_c,
    fitness_function_diff,
    fitness_function_stepwise,
    fitness_function_anti_boredom,
    fitness_function_7,
    fitness_function_8,
    fitness_function_9,
    fitness_function_10,
    fitness_function_11,
    fitness_function_muspy
]