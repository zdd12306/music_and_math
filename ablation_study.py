#!/usr/bin/env python3
"""
消融实验脚本 (Ablation Study)
Ablation Study Script

用于系统性地测试每个适应度函数的独立贡献
"""

import os
import sys

# 导入配置和主程序
from config import (
    RHYTHM_WEIGHTS, PITCH_WEIGHTS, SCALES, DEFAULT_SCALE,
    enable_single_rhythm_function, enable_single_pitch_function,
    reset_to_default_weights
)
from main import (
    Individual, run_genetic_algorithm, save_to_midi, debug_genome
)
from fitness_function_rhythm import rhythm_fitness_overall
from fitness_function_pitch import pitch_fitness_overall

def run_ablation_study(scale_name=None):
    """
    运行完整的消融实验
    
    实验设计：
    1. 测试每个节奏函数的单独效果
    2. 测试每个音高函数的单独效果
    3. 测试所有函数组合的效果
    """
    
    if scale_name is None:
        scale_name = DEFAULT_SCALE
    
    scale_notes = SCALES[scale_name]
    results_dir = "results/ablation"
    
    # 创建ablation子文件夹
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"✓ 已创建 {results_dir}/ 文件夹")
    
    print("\n" + "="*70)
    print("  消融实验 (Ablation Study)")
    print("="*70)
    print(f"\n调式: {scale_name}")
    print(f"音阶大小: {len(scale_notes)} 个音")
    print(f"\n实验设计:")
    print("  1. 基线测试 (所有权重=0)")
    print("  2. 单节奏函数测试 (3个)")
    print("  3. 单音高函数测试 (3个)")
    print("  4. 完整组合测试 (恢复默认权重)")
    print("="*70)
    
    # ========================================
    # 实验1: 基线 - 所有权重为0
    # ========================================
    print("\n[实验1/8] 基线测试 - 所有权重=0")
    print("-"*70)
    
    # 确保所有权重为0
    for key in RHYTHM_WEIGHTS:
        RHYTHM_WEIGHTS[key] = 0.0
    for key in PITCH_WEIGHTS:
        PITCH_WEIGHTS[key] = 0.0
    
    best_ind = run_genetic_algorithm(
        rhythm_fitness_overall,
        pitch_fitness_overall,
        scale_notes,
        func_name="baseline_all_zero"
    )
    
    debug_genome(best_ind)
    filename = f"ablation_01_baseline_all_zero.mid"
    save_to_midi(best_ind, filename)
    
    # ========================================
    # 实验2-4: 单节奏函数测试
    # ========================================
    rhythm_funcs = ['basic', 'legato', 'balanced']
    
    for idx, func_name in enumerate(rhythm_funcs, start=2):
        print(f"\n[实验{idx}/8] 单节奏函数测试 - {func_name}")
        print("-"*70)
        
        # 重置所有权重
        for key in RHYTHM_WEIGHTS:
            RHYTHM_WEIGHTS[key] = 0.0
        for key in PITCH_WEIGHTS:
            PITCH_WEIGHTS[key] = 0.0
        
        # 只启用当前节奏函数
        RHYTHM_WEIGHTS[func_name] = 1.0
        
        best_ind = run_genetic_algorithm(
            rhythm_fitness_overall,
            pitch_fitness_overall,
            scale_notes,
            func_name=f"rhythm_only_{func_name}"
        )
        
        debug_genome(best_ind)
        filename = f"ablation_0{idx}_rhythm_only_{func_name}.mid"
        save_to_midi(best_ind, filename)
    
    # ========================================
    # 实验5-7: 单音高函数测试
    # ========================================
    pitch_funcs = ['stepwise', 'arch', 'end_tonic']
    
    for idx, func_name in enumerate(pitch_funcs, start=5):
        print(f"\n[实验{idx}/8] 单音高函数测试 - {func_name}")
        print("-"*70)
        
        # 重置所有权重
        for key in RHYTHM_WEIGHTS:
            RHYTHM_WEIGHTS[key] = 0.0
        for key in PITCH_WEIGHTS:
            PITCH_WEIGHTS[key] = 0.0
        
        # 只启用当前音高函数
        PITCH_WEIGHTS[func_name] = 1.0
        
        best_ind = run_genetic_algorithm(
            rhythm_fitness_overall,
            pitch_fitness_overall,
            scale_notes,
            func_name=f"pitch_only_{func_name}"
        )
        
        debug_genome(best_ind)
        filename = f"ablation_0{idx}_pitch_only_{func_name}.mid"
        save_to_midi(best_ind, filename)
    
    # ========================================
    # 实验8: 完整组合 (默认权重)
    # ========================================
    print(f"\n[实验8/8] 完整组合测试 - 默认权重")
    print("-"*70)
    
    reset_to_default_weights()
    
    best_ind = run_genetic_algorithm(
        rhythm_fitness_overall,
        pitch_fitness_overall,
        scale_notes,
        func_name="full_combination"
    )
    
    debug_genome(best_ind)
    filename = f"ablation_08_full_combination.mid"
    save_to_midi(best_ind, filename)
    
    # ========================================
    # 实验完成
    # ========================================
    print("\n" + "="*70)
    print("  ✓ 消融实验完成！")
    print("="*70)
    print(f"\n生成了 8 个MIDI文件:")
    print(f"  results/ablation_01_baseline_all_zero.mid")
    print(f"  results/ablation_02_rhythm_only_basic.mid")
    print(f"  results/ablation_03_rhythm_only_legato.mid")
    print(f"  results/ablation_04_rhythm_only_balanced.mid")
    print(f"  results/ablation_05_pitch_only_stepwise.mid")
    print(f"  results/ablation_06_pitch_only_arch.mid")
    print(f"  results/ablation_07_pitch_only_end_tonic.mid")
    print(f"  results/ablation_08_full_combination.mid")
    print(f"\n运行 'python playmid.py' 播放所有结果")
    print(f"对比不同实验的音乐效果，分析每个函数的贡献")

if __name__ == "__main__":
    print("\n消融实验将测试每个适应度函数的独立贡献")
    print("这将需要较长时间（约30-60分钟）")
    
    # 用户选择调式
    print("\n可用调式:")
    for i, scale_name in enumerate(SCALES.keys(), 1):
        print(f"  {i}. {scale_name}")
    
    choice = input(f"\n请选择调式编号 (直接回车使用{DEFAULT_SCALE}): ").strip()
    
    if choice:
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(SCALES):
                chosen_scale = list(SCALES.keys())[choice_num - 1]
            else:
                print("无效选择，使用默认调式")
                chosen_scale = DEFAULT_SCALE
        except ValueError:
            print("无效输入，使用默认调式")
            chosen_scale = DEFAULT_SCALE
    else:
        chosen_scale = DEFAULT_SCALE
    
    confirm = input(f"\n确认开始消融实验? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        run_ablation_study(chosen_scale)
    else:
        print("已取消")

