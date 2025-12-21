import random
import copy
import time
from midiutil import MIDIFile

# === 1. 导入你的适应度函数库 ===
# 假设你的 fitness_function.py 中有一个列表叫 funcs
# 格式: funcs = [fitness_function_1, fitness_function_2, ...]
try:
    from fitness_function import funcs
except ImportError:
    print("错误: 未找到 fitness_function.py 或 funcs 列表。请确保文件存在。")
    funcs = []      

# === 2. 基础配置 (严格对应课件编码) ===
# 课件 P.43-44: 乐音体系编码
# F3(53) ~ G5(79)
PITCH_MAP = list(range(53, 80)) 
NUM_PITCHES = len(PITCH_MAP)
CODE_REST = 0                  # 0 代表休止符
CODE_HOLD = NUM_PITCHES + 1    # 14/29 代表延长记号 (Sustain) [cite: 438, 446]

# 基因长度: 4小节 x 4拍 x 2(八分音符) = 32 [cite: 444]
GENOME_LENGTH = 64 

# === 3. 数据结构定义 ===
def generate_weighted_gene():
    """
    加权生成基因：
    - 延长记号 (HOLD): 50% 概率 (让音符平均长度为 2 个单位，即四分音符)
    - 休止符 (REST): 10% 概率
    - 新音符 (NOTE): 40% 概率
    """
    rand = random.random()
    if rand < 0.5:
        return CODE_HOLD  # 50% 概率产生延长
    elif rand < 0.6:
        return CODE_REST  # 10% 概率产生休止
    else:
        return random.randint(1, NUM_PITCHES) # 剩余 40% 随机产生一个音高
    
class Individual:
    def __init__(self, genes=None):
        if genes:
            self.genes = genes
        else:
            # 使用加权生成替代原来的 random.randint
            self.genes = [generate_weighted_gene() for _ in range(GENOME_LENGTH)]
            
            # 修正：第一个基因不能是延长记号 (因为前面没有音)，强制设为休止或随机音
            if self.genes[0] == CODE_HOLD:
                self.genes[0] = random.randint(0, NUM_PITCHES)
                
        self.fitness = 0.0
    # In your Individual class:            
    def to_notes(self):
            """
            Decodes genes into a list of (pitch, start_time, duration).
            This ensures rests actually take up space.
            """
            notes = []
            current_pitch = None
            current_start_time = 0.0
            current_dur = 0
            
            for i, gene in enumerate(self.genes):
                time_step = i * 0.5  # Each gene is an 8th note (0.5 beats)
                
                if 1 <= gene <= NUM_PITCHES:
                    # 1. If a note was already playing, close it
                    if current_pitch is not None:
                        notes.append((PITCH_MAP[current_pitch-1], current_start_time, current_dur * 0.5))
                    
                    # 2. Start a new note
                    current_pitch = gene
                    current_start_time = time_step
                    current_dur = 1
                    
                elif gene == CODE_HOLD:
                    if current_pitch is not None:
                        current_dur += 1 # Extend the current note
                    # If HOLD follows a REST, we do nothing (it stays silent)
                    
                elif gene == CODE_REST:
                    # If a note was playing, close it and reset
                    if current_pitch is not None:
                        notes.append((PITCH_MAP[current_pitch-1], current_start_time, current_dur * 0.5))
                    current_pitch = None
                    current_dur = 0

            # Close the final note if it exists
            if current_pitch is not None:
                notes.append((PITCH_MAP[current_pitch-1], current_start_time, current_dur * 0.5))
                
            return notes
    
def debug_genome(individual):
        genes = individual.genes
        note_count = sum(1 for g in genes if 1 <= g <= NUM_PITCHES)
        hold_count = sum(1 for g in genes if g == CODE_HOLD)
        rest_count = sum(1 for g in genes if g == CODE_REST)
        
        print(f"\n--- Genome Debug Tool ---")
        print(f"DNA Sequence: {genes}")
        print(f"Stats: Notes: {note_count} | Holds: {hold_count} | Rests: {rest_count}")
        
        # Check for "Illegal" Holds (Holds that appear after a Rest)
        illegal_holds = 0
        for i in range(1, len(genes)):
            if genes[i] == CODE_HOLD and genes[i-1] == CODE_REST:
                illegal_holds += 1
        if illegal_holds > 0:
            print(f"Warning: Found {illegal_holds} holds following a rest (these sound like silence).")

class MelodyAdapter:
    """
    适配器类：
    你的 fitness_function 通常期望读取 melody.notes
    这个类将 Individual 伪装成旧版的 Melody 对象
    """
    def __init__(self, note_list):
        # 统一格式: [(pitch, duration), ...]
        self.notes = note_list

# === 4. 遗传操作算子 (对应课件 P.45-52) ===

def selection_roulette(population):
    """
    轮盘赌选择 [cite: 530, 538]
    """
    # 处理可能的负分，将适应度平移到正数区间
    min_fit = min(ind.fitness for ind in population)
    offset = abs(min_fit) if min_fit < 0 else 0
    
    total_fitness = sum(ind.fitness + offset for ind in population)
    if total_fitness == 0:
        return random.choice(population)
        
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind in population:
        current += (ind.fitness + offset)
        if current > pick:
            return ind
    return population[-1]

def crossover(p1, p2):
    """
    单点交叉 [cite: 460, 467]
    """
    point = random.randint(1, GENOME_LENGTH - 1)
    c1_genes = p1.genes[:point] + p2.genes[point:]
    c2_genes = p2.genes[:point] + p1.genes[point:]
    return Individual(c1_genes), Individual(c2_genes)

def mutate(ind, rate=0.05):
    """
    单点变异 (使用加权逻辑)
    """
    new_genes = ind.genes[:]
    for i in range(len(new_genes)):
        if random.random() < rate:
            # 变异时也倾向于生成延长记号，保持节奏的长线条
            new_genes[i] = generate_weighted_gene()
            
    # # 再次修正首位基因
    # if new_genes[0] == CODE_HOLD:
    #     new_genes[0] = random.randint(0, NUM_PITCHES)
    return Individual(new_genes)

def musical_transform(ind):
    """
    特殊变异：移调、倒影、逆行 
    """
    genes = ind.genes[:]
    op = random.choice(['transposition', 'inversion', 'retrograde'])
    
    if op == 'retrograde':
        genes.reverse()
    elif op == 'transposition':
        shift = random.choice([-2, -1, 1, 2])
        for i in range(len(genes)):
            if 1 <= genes[i] <= NUM_PITCHES:
                val = genes[i] + shift
                if 1 <= val <= NUM_PITCHES: genes[i] = val
    elif op == 'inversion':
        pivot = next((g for g in genes if 1 <= g <= NUM_PITCHES), 10) # 寻找中心轴
        for i in range(len(genes)):
            if 1 <= genes[i] <= NUM_PITCHES:
                dist = genes[i] - pivot
                val = pivot - dist
                if 1 <= val <= NUM_PITCHES: genes[i] = val
                
    return Individual(genes)

# === 5. 遗传算法主程序 ===

def run_genetic_algorithm(target_fitness_func, func_name="Unknown"):
    # 参数设置 [cite: 540]
    POP_SIZE = 200
    MAX_GEN = 2000
    ELITISM_COUNT = 5 # 精英保留数量
    
    # 初始化种群
    population = [Individual() for _ in range(POP_SIZE)]
    
    print(f"--- 开始运行: {func_name} ---")
    
    for gen in range(MAX_GEN):
        # 1. 计算适应度 [cite: 548]
        for ind in population:
            # === 关键步骤：适配器转换 ===
            # 将整数基因解码为音符列表，传给你的 fitness_function
            note_list = ind.to_notes()
            adapter = MelodyAdapter(note_list)
            # if ind == population[-1]:
            #     breakpoint()
            # 调用外部传入的函数
            try:
                
                ind.fitness = target_fitness_func(adapter)
            except Exception as e:
                ind.fitness = 0 # 防止报错中断
        
        # 排序
        population.sort(key=lambda x: x.fitness, reverse=True)
        best_score = population[0].fitness
        # 2. 生成下一代 [cite: 554]
        next_gen = []
        
        # 精英策略 (直接复制) [cite: 502, 508]
        next_gen.extend([Individual(ind.genes[:]) for ind in population[:ELITISM_COUNT]])
        
        while len(next_gen) < POP_SIZE:
            # 轮盘赌选择
            p1 = selection_roulette(population)
            p2 = selection_roulette(population)
            
            c1, c2 = Individual(p1.genes[:]), Individual(p2.genes[:])
            
            # 交叉 [cite: 556]
            if random.random() < 0.7:
                c1, c2 = crossover(p1, p2)
            
            # 变异
            c1 = mutate(c1)
            c2 = mutate(c2)
            
            # 特殊变换
            if random.random() < 0.1: c1 = musical_transform(c1)
            if random.random() < 0.1: c2 = musical_transform(c2)
                
            next_gen.append(c1)
            if len(next_gen) < POP_SIZE: next_gen.append(c2)
            
        population = next_gen
        
        if gen % 200 == 0:
            print(f"  Gen {gen}: Best Score = {best_score:.2f}")
    return population[0]

def save_to_midi(individual, filename):
    mf = MIDIFile(1)
    track = 0
    start_time_offset = 0 
    mf.addTrackName(track, start_time_offset, "GA Melody")
    mf.addTempo(track, start_time_offset, 120)
    
    # Get the decoded notes: (pitch, start_time, duration)
    decoded_notes = individual.to_notes()
    
    for pitch, start, duration in decoded_notes:
        # mf.addNote(track, channel, pitch, time, duration, volume)
        mf.addNote(track, 0, pitch, start, duration, 100)
        
    with open(filename, 'wb') as out_f:
        mf.writeFile(out_f)
    print(f"  已保存: {filename}")

# === 7. 主执行循环：枚举 funcs ===
if __name__ == "__main__":
    if not funcs:
        print("警告: funcs 列表为空，请检查 fitness_function.py")
    import time, os
    ts = (int)(time.time())
    os.mkdir(f'{ts}')
    for i, fitness_func in enumerate(funcs):
        # 获取函数名用于生成文件名
        fname = fitness_func.__name__
        
        # 运行算法
        best_ind = run_genetic_algorithm(fitness_func, func_name=fname)
        debug_genome(best_ind)
        # 保存结果
        output_filename = f"{ts}/output_{fname}.mid"
        save_to_midi(best_ind, output_filename)
        
    print("\n所有函数运行完毕！")