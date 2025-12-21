"""
配置文件 - 所有超参数设置
Configuration File - All Hyperparameters

修改这个文件来调整遗传算法和音乐生成的各种参数
"""

# ============================================================
# 音域设置 (Pitch Range)
# ============================================================

PITCH_MIN = 53  # F3 - 最低音
PITCH_MAX = 79  # G5 - 最高音

# ============================================================
# 编码设置 (Encoding)
# ============================================================

# 基因长度
RHYTHM_LENGTH = 32  # 32个八分音符 = 16拍 = 4小节（4/4拍）
PITCH_LENGTH = 32   # 对应的32个音高位置

# 节奏编码
RHYTHM_NOTE = 1      # 发声（起拍）
RHYTHM_HOLD = 2      # 延长
RHYTHM_REST = 0      # 休止符

# 初始化权重（生成个体时的概率分布）
INIT_RHYTHM_WEIGHTS = {
    'note': 0.50,   # 50% 发声
    'hold': 0.40,   # 40% 延长
    'rest': 0.10,   # 10% 休止
}

# ============================================================
# 遗传算法参数 (Genetic Algorithm)
# ============================================================

# 种群设置
POP_SIZE = 200           # 种群大小
MAX_GEN = 1024           # 最大代数
ELITISM_COUNT = 10        # 精英保留数量

# 遗传操作概率
CROSSOVER_RATE = 0.7     # 交叉概率 (70%)
MUTATION_RATE = 0.05     # 变异概率 (5%)
TRANSFORM_RATE = 0.05    # 特殊变换概率 (5%)

# 输出设置
PRINT_INTERVAL = 200     # 每N代输出一次进度

# ============================================================
# MIDI输出设置
# ============================================================

MIDI_TEMPO = 120         # BPM (每分钟节拍数)
MIDI_VELOCITY = 100      # 力度 (0-127)

# 输出目录
RESULTS_DIR = "results"

# ============================================================
# 调式定义 (Scales)
# ============================================================

# 大调音阶的半音间隔：全全半全全全半
MAJOR_INTERVALS = [2, 2, 1, 2, 2, 2, 1]

# 自然小调的半音间隔：全半全全半全全
MINOR_INTERVALS = [2, 1, 2, 2, 1, 2, 2]

# 可用的调式及其根音（MIDI音高）
AVAILABLE_SCALES = {
    # 大调
    'C_major': {'root': 60, 'intervals': MAJOR_INTERVALS},  # C D E F G A B
    'G_major': {'root': 67, 'intervals': MAJOR_INTERVALS},  # G A B C D E F#
    'D_major': {'root': 62, 'intervals': MAJOR_INTERVALS},  # D E F# G A B C#
    'A_major': {'root': 69, 'intervals': MAJOR_INTERVALS},  # A B C# D E F# G#
    'E_major': {'root': 64, 'intervals': MAJOR_INTERVALS},  # E F# G# A B C# D#
    'F_major': {'root': 65, 'intervals': MAJOR_INTERVALS},  # F G A Bb C D E
    
    # 小调
    'A_minor': {'root': 69, 'intervals': MINOR_INTERVALS},  # A B C D E F G
    'E_minor': {'root': 64, 'intervals': MINOR_INTERVALS},  # E F# G A B C D
    'D_minor': {'root': 62, 'intervals': MINOR_INTERVALS},  # D E F G A Bb C
}

# 默认调式
DEFAULT_SCALE = 'C_major'

# ============================================================
# 适应度函数权重 (Fitness Function Weights) - 最简版
# ============================================================

# 只保留两个最基本的适应度函数：
# 1. 音高：级进流畅 (stepwise) - 评估音高的平滑度
# 2. 节奏：节奏奇性 (parity) - 评估节奏的非对称性

# 节奏适应度函数权重 (用于 rhythm_fitness_overall)
RHYTHM_WEIGHTS = {
    'parity': 1.0,        # 节奏奇性（避免对称）
    'density': 1.0,       # 节奏密度（音符密度适中）
    'syncopation': 1.0,   # 切分音（节奏变化）
    'rest': 1.0,          # 休止符分布（适当的休止）
    'pattern': 1.0,       # 节奏模式（规律性）
}

# 音高适应度函数权重 (用于 pitch_fitness_overall)
PITCH_WEIGHTS = {
    'stepwise': 1.0,      # 级进流畅（鼓励小音程）
    'consonance': 1.0,    # 音程协和度（鼓励协和音程）
    'range': 1.0,         # 音域平衡（适中的音域范围）
    'direction': 1.0,     # 旋律方向变化（起伏丰富）
    'climax': 1.0,        # 旋律高潮（有明显高潮点）
}

# ============================================================
# 快速启用/禁用函数
# ============================================================

# 如果想测试效果，可以临时禁用某个函数：
# PITCH_WEIGHTS['stepwise'] = 0.0
# RHYTHM_WEIGHTS['parity'] = 0.0

# 或者使用这个辅助函数快速启用单个函数
def enable_single_rhythm_function(func_name, weight=1.0):
    """启用单个节奏函数（最简版）"""
    global RHYTHM_WEIGHTS
    # 先全部设为0
    for key in RHYTHM_WEIGHTS:
        RHYTHM_WEIGHTS[key] = 0.0
    # 启用指定函数
    if func_name in RHYTHM_WEIGHTS:
        RHYTHM_WEIGHTS[func_name] = weight
        print(f"✓ 已启用 rhythm_{func_name} (权重={weight})")
    else:
        print(f"✗ 错误: 未找到函数 {func_name}")

def enable_single_pitch_function(func_name, weight=1.0):
    """启用单个音高函数（最简版）"""
    global PITCH_WEIGHTS
    # 先全部设为0
    for key in PITCH_WEIGHTS:
        PITCH_WEIGHTS[key] = 0.0
    # 启用指定函数
    if func_name in PITCH_WEIGHTS:
        PITCH_WEIGHTS[func_name] = weight
        print(f"✓ 已启用 pitch_{func_name} (权重={weight})")
    else:
        print(f"✗ 错误: 未找到函数 {func_name}")

def reset_to_default_weights():
    """恢复默认权重（最简版）"""
    # 直接更新字典内容，而不是重新赋值
    # 这样可以保持对已导入引用的影响
    RHYTHM_WEIGHTS['parity'] = 1.0
    PITCH_WEIGHTS['stepwise'] = 1.0
    print("✓ 已恢复默认权重")

# ============================================================
# 显示设置
# ============================================================

DISPLAY_SETTINGS = {
    'show_debug': True,         # 是否显示调试信息
    'show_progress': True,      # 是否显示进度
    'show_scale_info': True,    # 是否显示音阶信息
}

# ============================================================
# 快捷配置预设
# ============================================================

# 如果想要更快的测试，使用这个预设
QUICK_TEST = {
    'POP_SIZE': 50,
    'MAX_GEN': 256,
    'PRINT_INTERVAL': 50,
}

# 如果想要更高质量的结果，使用这个预设
HIGH_QUALITY = {
    'POP_SIZE': 500,
    'MAX_GEN': 2048,
    'PRINT_INTERVAL': 200,
}

# 当前使用的配置模式 ('default', 'quick_test', 'high_quality')
CONFIG_MODE = 'default'

# ============================================================
# 配置应用函数
# ============================================================

def apply_config_mode(mode='default'):
    """应用配置模式"""
    global POP_SIZE, MAX_GEN, PRINT_INTERVAL
    
    if mode == 'quick_test':
        POP_SIZE = QUICK_TEST['POP_SIZE']
        MAX_GEN = QUICK_TEST['MAX_GEN']
        PRINT_INTERVAL = QUICK_TEST['PRINT_INTERVAL']
        print("⚡ 使用快速测试模式")
    elif mode == 'high_quality':
        POP_SIZE = HIGH_QUALITY['POP_SIZE']
        MAX_GEN = HIGH_QUALITY['MAX_GEN']
        PRINT_INTERVAL = HIGH_QUALITY['PRINT_INTERVAL']
        print("🎯 使用高质量模式")
    else:
        print("✓ 使用默认配置")

# 启动时应用配置
apply_config_mode(CONFIG_MODE)

# ============================================================
# 配置验证
# ============================================================

def validate_config(allow_zero_weights=False):
    """
    验证配置的合理性
    
    参数:
        allow_zero_weights: 是否允许权重全为0（用于消融实验）
    """
    errors = []
    warnings = []
    
    # 检查基本参数
    if RHYTHM_LENGTH != PITCH_LENGTH:
        errors.append("RHYTHM_LENGTH 必须等于 PITCH_LENGTH")
    
    if POP_SIZE < 10:
        warnings.append("POP_SIZE 太小可能导致多样性不足")
    
    if ELITISM_COUNT >= POP_SIZE:
        errors.append("ELITISM_COUNT 不能大于等于 POP_SIZE")
    
    if not (0 <= CROSSOVER_RATE <= 1):
        errors.append("CROSSOVER_RATE 必须在 0-1 之间")
    
    if not (0 <= MUTATION_RATE <= 1):
        errors.append("MUTATION_RATE 必须在 0-1 之间")
    
    # 检查权重和
    rhythm_weight_sum = sum(RHYTHM_WEIGHTS.values())
    pitch_weight_sum = sum(PITCH_WEIGHTS.values())
    
    if not allow_zero_weights:
        if abs(rhythm_weight_sum) < 0.1:
            errors.append("节奏权重和不能为0")
        if abs(pitch_weight_sum) < 0.1:
            errors.append("音高权重和不能为0")
    else:
        if abs(rhythm_weight_sum) < 0.1 and abs(pitch_weight_sum) < 0.1:
            warnings.append("⚠️  消融实验模式: 所有权重为0 (基线测试)")
        elif abs(rhythm_weight_sum) < 0.1:
            warnings.append("⚠️  消融实验模式: 节奏权重为0")
        elif abs(pitch_weight_sum) < 0.1:
            warnings.append("⚠️  消融实验模式: 音高权重为0")
    
    # 输出结果
    if errors:
        print("\n❌ 配置错误:")
        for e in errors:
            print(f"  - {e}")
        return False
    
    if warnings:
        print("\n⚠️  配置警告:")
        for w in warnings:
            print(f"  - {w}")
    
    if not errors and not warnings:
        print("\n✓ 配置有效")
    
    return True

# 自动验证
if __name__ == "__main__":
    print("="*60)
    print("  配置验证")
    print("="*60)
    
    # 检查是否为消融实验模式
    is_ablation = sum(RHYTHM_WEIGHTS.values()) == 0 or sum(PITCH_WEIGHTS.values()) == 0
    
    if validate_config(allow_zero_weights=is_ablation):
        print("\n✓ 配置验证通过")
        print(f"\n当前模式: {'🔬 消融实验' if is_ablation else '🎵 正常运行'}")
        print(f"配置预设: {CONFIG_MODE.upper()}")
        print(f"种群大小: {POP_SIZE}")
        print(f"最大代数: {MAX_GEN}")
        print(f"节奏权重和: {sum(RHYTHM_WEIGHTS.values()):.1f}")
        print(f"音高权重和: {sum(PITCH_WEIGHTS.values()):.1f}")
    else:
        print("\n✗ 配置验证失败，请修正错误")

