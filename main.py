import random
import copy
import time
import os
from midiutil import MIDIFile

# 创建results文件夹
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)
    print(f"✓ 已创建 {RESULTS_DIR}/ 文件夹")

# === 1. 导入适应度函数库 ===
try:
    from fitness_function_rhythm import rhythm_fitness_overall
    from fitness_function_pitch import pitch_fitness_overall
    print("✓ 已导入综合适应度函数")
except ImportError as e:
    print(f"错误: 未找到适应度函数文件 - {e}")
    exit(1)

# === 2. 调式定义 ===
# 音域范围：F3(53) ~ G5(79)
PITCH_MIN = 53
PITCH_MAX = 79

def generate_scale_in_range(root_midi, intervals, min_pitch=53, max_pitch=79):
    """
    在指定音域范围内生成调式音阶
    
    Args:
        root_midi: 根音的MIDI音高（例如C4=60）
        intervals: 半音间隔模式（例如大调：[2,2,1,2,2,2,1]）
        min_pitch: 最低音高
        max_pitch: 最高音高
    
    Returns:
        list: 该范围内所有调内音的MIDI音高列表
    """
    scale = []
    
    # 先找到range内最低的根音位置
    current = root_midi
    while current - 12 >= min_pitch:
        current -= 12
    
    # 从这个位置开始，向上生成音阶
    while current <= max_pitch:
        # 生成一个八度内的所有音
        pitch = current
        for interval in intervals:
            if min_pitch <= pitch <= max_pitch:
                scale.append(pitch)
            pitch += interval
        current += 12  # 移到下一个八度
    
    return sorted(list(set(scale)))  # 去重并排序

# 大调音阶的半音间隔：全全半全全全半
MAJOR_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
# 自然小调的半音间隔：全半全全半全全
MINOR_INTERVALS = [2, 1, 2, 2, 1, 2, 2]

SCALES = {
    # 大调
    'C_major': generate_scale_in_range(60, MAJOR_INTERVALS),  # C D E F G A B
    'G_major': generate_scale_in_range(67, MAJOR_INTERVALS),  # G A B C D E F#
    'D_major': generate_scale_in_range(62, MAJOR_INTERVALS),  # D E F# G A B C#
    'A_major': generate_scale_in_range(69, MAJOR_INTERVALS),  # A B C# D E F# G#
    'E_major': generate_scale_in_range(64, MAJOR_INTERVALS),  # E F# G# A B C# D#
    'F_major': generate_scale_in_range(65, MAJOR_INTERVALS),  # F G A Bb C D E
    
    # 小调
    'A_minor': generate_scale_in_range(69, MINOR_INTERVALS),  # A B C D E F G
    'E_minor': generate_scale_in_range(64, MINOR_INTERVALS),  # E F# G A B C D
    'D_minor': generate_scale_in_range(62, MINOR_INTERVALS),  # D E F G A Bb C
}

print(SCALES)
# === 3. 编码配置 ===
RHYTHM_LENGTH = 16  # 16个八分音符 = 4小节
PITCH_LENGTH = 16   # 对应的16个音高位置

# 节奏编码
RHYTHM_NOTE = 1      # 发声（起拍）
RHYTHM_HOLD = 2      # 延长
RHYTHM_REST = 0      # 休止符

# === 4. Individual类（双基因编码）===
class Individual:
    def __init__(self, rhythm_genes=None, pitch_genes=None, scale_notes=None):
        """
        rhythm_genes: 长度16的节奏基因 [0=休止, 1=发声, 2=延长]
        pitch_genes: 长度16的音高基因 [0到len(scale_notes)-1，索引调式内的音]
        scale_notes: 调式音阶列表（MIDI音高）
        """
        self.scale_notes = scale_notes if scale_notes else SCALES['C_major']
        self.num_scale_notes = len(self.scale_notes)
        
        if rhythm_genes:
            self.rhythm_genes = rhythm_genes
        else:
            # 加权生成节奏：40%发声，30%延长，30%休止
            self.rhythm_genes = [self._generate_rhythm() for _ in range(RHYTHM_LENGTH)]
            # 确保第一个是发声
            if self.rhythm_genes[0] != RHYTHM_NOTE:
                self.rhythm_genes[0] = RHYTHM_NOTE
                
        if pitch_genes:
            self.pitch_genes = pitch_genes
        else:
            # 随机生成音高索引（索引范围：0 到 调式音数量-1）
            self.pitch_genes = [random.randint(0, self.num_scale_notes - 1) 
                               for _ in range(PITCH_LENGTH)]
            
        self.rhythm_fitness = 0.0
        self.pitch_fitness = 0.0
        self.total_fitness = 0.0
    
    def _generate_rhythm(self):
        """加权生成节奏基因"""
        rand = random.random()
        if rand < 0.40:
            return RHYTHM_NOTE  # 40% 发声
        elif rand < 0.70:
            return RHYTHM_HOLD  # 30% 延长
        else:
            return RHYTHM_REST  # 30% 休止
    
    def to_notes(self):
        """
        将双基因解码为音符列表
        返回: [(pitch, start_time, duration), ...]
        """
        notes = []
        current_pitch = None
        current_start = 0.0
        current_dur = 0
        
        for i in range(RHYTHM_LENGTH):
            time_step = i * 0.5  # 每个八分音符0.5拍
            rhythm = self.rhythm_genes[i]
            
            if rhythm == RHYTHM_NOTE:
                # 如果有音符在播放，先结束它
                if current_pitch is not None:
                    notes.append((current_pitch, current_start, current_dur * 0.5))
                
                # 开始新音符
                pitch_idx = self.pitch_genes[i]
                current_pitch = self.scale_notes[pitch_idx]
                current_start = time_step
                current_dur = 1
                
            elif rhythm == RHYTHM_HOLD:
                if current_pitch is not None:
                    current_dur += 1  # 延长当前音符
                # 如果前面是休止，则继续休止
                
            elif rhythm == RHYTHM_REST:
                # 结束当前音符（如果有）
                if current_pitch is not None:
                    notes.append((current_pitch, current_start, current_dur * 0.5))
                current_pitch = None
                current_dur = 0
        
        # 结束最后的音符
        if current_pitch is not None:
            notes.append((current_pitch, current_start, current_dur * 0.5))
            
        return notes

def debug_genome(individual):
    """调试输出"""
    rhythm = individual.rhythm_genes
    pitch = individual.pitch_genes
    
    note_count = rhythm.count(RHYTHM_NOTE)
    hold_count = rhythm.count(RHYTHM_HOLD)
    rest_count = rhythm.count(RHYTHM_REST)
    
    print(f"\n--- 基因调试工具 ---")
    print(f"节奏基因: {rhythm}")
    print(f"音高基因: {pitch}")
    print(f"统计: 发声:{note_count} | 延长:{hold_count} | 休止:{rest_count}")
    print(f"节奏适应度: {individual.rhythm_fitness:.2f}")
    print(f"音高适应度: {individual.pitch_fitness:.2f}")
    print(f"总适应度: {individual.total_fitness:.2f}")

class MelodyAdapter:
    """适配器：将Individual伪装成旧版Melody对象"""
    def __init__(self, note_list, rhythm_genes, pitch_genes):
        self.notes = note_list
        self.rhythm_genes = rhythm_genes
        self.pitch_genes = pitch_genes

# === 5. 遗传操作算子 ===

def selection_roulette(population):
    """轮盘赌选择"""
    min_fit = min(ind.total_fitness for ind in population)
    offset = abs(min_fit) + 1 if min_fit < 0 else 0
    
    total_fitness = sum(ind.total_fitness + offset for ind in population)
    if total_fitness == 0:
        return random.choice(population)
        
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind in population:
        current += (ind.total_fitness + offset)
        if current > pick:
            return ind
    return population[-1]

def crossover_genes(genes1, genes2):
    """单点交叉"""
    point = random.randint(1, len(genes1) - 1)
    c1 = genes1[:point] + genes2[point:]
    c2 = genes2[:point] + genes1[point:]
    return c1, c2

def mutate_rhythm(genes, rate=0.05):
    """节奏变异"""
    new_genes = genes[:]
    for i in range(len(new_genes)):
        if random.random() < rate:
            new_genes[i] = random.choice([RHYTHM_NOTE, RHYTHM_HOLD, RHYTHM_REST])
    # 确保第一个是发声
    if new_genes[0] != RHYTHM_NOTE:
        new_genes[0] = RHYTHM_NOTE
    return new_genes

def mutate_pitch(genes, num_scale_notes, rate=0.05):
    """音高变异"""
    new_genes = genes[:]
    for i in range(len(new_genes)):
        if random.random() < rate:
            new_genes[i] = random.randint(0, num_scale_notes - 1)
    return new_genes

def musical_transform_pitch(genes, num_scale_notes):
    """音高特殊变换：移调、倒影、逆行"""
    new_genes = genes[:]
    op = random.choice(['transposition', 'inversion', 'retrograde'])
    
    if op == 'retrograde':
        new_genes.reverse()
    elif op == 'transposition':
        shift = random.choice([-2, -1, 1, 2])
        new_genes = [(g + shift) % num_scale_notes for g in new_genes]
    elif op == 'inversion':
        pivot = num_scale_notes // 2  # 中心音
        new_genes = [(2 * pivot - g) % num_scale_notes for g in new_genes]
    
    return new_genes

def musical_transform_rhythm(genes):
    """节奏特殊变换：逆行、增值、减值"""
    new_genes = genes[:]
    op = random.choice(['retrograde', 'augmentation', 'diminution'])
    
    if op == 'retrograde':
        new_genes.reverse()
    elif op == 'augmentation':
        # 增值：将一些NOTE改为HOLD（让音符更长）
        for i in range(len(new_genes)):
            if new_genes[i] == RHYTHM_NOTE and random.random() < 0.3:
                if i + 1 < len(new_genes):
                    new_genes[i + 1] = RHYTHM_HOLD
    elif op == 'diminution':
        # 减值：将一些HOLD改为NOTE（让音符更短）
        for i in range(len(new_genes)):
            if new_genes[i] == RHYTHM_HOLD and random.random() < 0.3:
                new_genes[i] = RHYTHM_NOTE
    
    # 确保第一个是发声
    if new_genes[0] != RHYTHM_NOTE:
        new_genes[0] = RHYTHM_NOTE
    return new_genes

# === 6. 主遗传算法 ===

def run_genetic_algorithm(rhythm_fitness_func, pitch_fitness_func, 
                         scale_notes, func_name="Unknown"):
    """
    双基因独立进化的遗传算法
    """
    POP_SIZE = 200
    MAX_GEN = 1024
    ELITISM_COUNT = 2
    
    # 初始化种群
    population = [Individual(scale_notes=scale_notes) for _ in range(POP_SIZE)]
    
    print(f"\n{'='*60}")
    print(f"开始运行: {func_name}")
    print(f"调式: {scale_notes}")
    print(f"{'='*60}")
    
    for gen in range(MAX_GEN):
        # 1. 计算适应度
        for ind in population:
            note_list = ind.to_notes()
            adapter = MelodyAdapter(note_list, ind.rhythm_genes, ind.pitch_genes)
            
            try:
                ind.rhythm_fitness = rhythm_fitness_func(adapter)
                ind.pitch_fitness = pitch_fitness_func(adapter)
                # 总适应度是两者的加权和
                ind.total_fitness = ind.rhythm_fitness + ind.pitch_fitness
            except Exception as e:
                print(f"适应度计算错误: {e}")
                ind.rhythm_fitness = 0
                ind.pitch_fitness = 0
                ind.total_fitness = 0
        
        # 排序
        population.sort(key=lambda x: x.total_fitness, reverse=True)
        best = population[0]
        
        # 2. 生成下一代
        next_gen = []
        
        # 精英保留
        next_gen.extend([
            Individual(
                rhythm_genes=ind.rhythm_genes[:],
                pitch_genes=ind.pitch_genes[:],
                scale_notes=scale_notes
            ) for ind in population[:ELITISM_COUNT]
        ])
        
        while len(next_gen) < POP_SIZE:
            # 选择
            p1 = selection_roulette(population)
            p2 = selection_roulette(population)
            
            # 复制父代
            c1_rhythm = p1.rhythm_genes[:]
            c1_pitch = p1.pitch_genes[:]
            c2_rhythm = p2.rhythm_genes[:]
            c2_pitch = p2.pitch_genes[:]
            
            # 交叉（节奏和音高独立交叉）
            if random.random() < 0.7:
                c1_rhythm, c2_rhythm = crossover_genes(c1_rhythm, c2_rhythm)
            if random.random() < 0.7:
                c1_pitch, c2_pitch = crossover_genes(c1_pitch, c2_pitch)
            
            # 获取音阶大小
            num_scale_notes = len(scale_notes)
            
            # 变异
            c1_rhythm = mutate_rhythm(c1_rhythm)
            c1_pitch = mutate_pitch(c1_pitch, num_scale_notes)
            c2_rhythm = mutate_rhythm(c2_rhythm)
            c2_pitch = mutate_pitch(c2_pitch, num_scale_notes)
            
            # 特殊变换
            if random.random() < 0.03:
                c1_pitch = musical_transform_pitch(c1_pitch, num_scale_notes)
            if random.random() < 0.03:
                c2_pitch = musical_transform_pitch(c2_pitch, num_scale_notes)
            if random.random() < 0.03:
                c1_rhythm = musical_transform_rhythm(c1_rhythm)
            if random.random() < 0.03:
                c2_rhythm = musical_transform_rhythm(c2_rhythm)
            
            # 创建新个体
            next_gen.append(Individual(c1_rhythm, c1_pitch, scale_notes))
            if len(next_gen) < POP_SIZE:
                next_gen.append(Individual(c2_rhythm, c2_pitch, scale_notes))
        
        population = next_gen
        
        # 输出进度
        if gen % 200 == 0:
            print(f"  第{gen:4d}代: 总分={best.total_fitness:7.2f} "
                  f"(节奏={best.rhythm_fitness:6.2f}, 音高={best.pitch_fitness:6.2f})")
    
    # 最终输出
    best = population[0]
    print(f"\n最终结果: 总分={best.total_fitness:.2f} "
          f"(节奏={best.rhythm_fitness:.2f}, 音高={best.pitch_fitness:.2f})")
    
    return best

def save_to_midi(individual, filename):
    """保存为MIDI文件到results文件夹"""
    # 确保文件名保存到results文件夹
    filepath = os.path.join(RESULTS_DIR, filename)
    
    mf = MIDIFile(1)
    track = 0
    mf.addTrackName(track, 0, "GA Melody")
    mf.addTempo(track, 0, 120)
    
    decoded_notes = individual.to_notes()
    
    for pitch, start, duration in decoded_notes:
        mf.addNote(track, 0, pitch, start, duration, 100)
    
    with open(filepath, 'wb') as out_f:
        mf.writeFile(out_f)
    print(f"✓ 已保存: {filepath}")

# === 7. 主程序 ===
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  音乐遗传算法 - 节奏与音高独立进化")
    print("="*60)
    
    # 用户输入调式
    print("\n可用调式:")
    for i, scale_name in enumerate(SCALES.keys(), 1):
        print(f"  {i}. {scale_name}")
    
    while True:
        try:
            choice = input("\n请选择调式编号 (1-9，直接回车默认C大调): ").strip()
            if not choice:
                chosen_scale = 'C_major'
                break
            choice_num = int(choice)
            if 1 <= choice_num <= len(SCALES):
                chosen_scale = list(SCALES.keys())[choice_num - 1]
                break
            else:
                print("无效选择，请重新输入")
        except ValueError:
            print("请输入数字")
    
    scale_notes = SCALES[chosen_scale]
    print(f"\n已选择: {chosen_scale}")
    print(f"音阶: {scale_notes}\n")
    
    # 检查适应度函数
    if not pitch_fitness_funcs or not rhythm_fitness_funcs:
        print("警告: 适应度函数列表为空，请检查 fitness_function.py")
        exit(1)
    
    # 运行所有组合
    total_combinations = len(pitch_fitness_funcs) * len(rhythm_fitness_funcs)
    current = 0
    
    for pitch_func in pitch_fitness_funcs:
        for rhythm_func in rhythm_fitness_funcs:
            current += 1
            
            # 生成函数名
            func_name = f"{rhythm_func.__name__}_{pitch_func.__name__}"
            
            print(f"\n[{current}/{total_combinations}] 组合: {func_name}")
            
            # 运行算法
            best_ind = run_genetic_algorithm(
                rhythm_func, 
                pitch_func, 
                scale_notes,
                func_name=func_name
            )
            
            # 调试输出
            debug_genome(best_ind)
            
            # 保存结果
            output_filename = f"output_{chosen_scale}_{func_name}.mid"
            save_to_midi(best_ind, output_filename)
    
    print("\n" + "="*60)
    print("  所有组合运行完毕！")
    print("="*60)
