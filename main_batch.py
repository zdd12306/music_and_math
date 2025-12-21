#!/usr/bin/env python3
"""
批量生成脚本 - 生成所有适应度函数组合
Batch Generation Script

如果你想要测试所有适应度函数的组合，运行这个脚本
它会生成所有可能的 rhythm × pitch 组合（最多上百个文件）

警告：这会需要很长时间！
"""

import random
import copy
import time
import os
from midiutil import MIDIFile

# 导入所有适应度函数
try:
    from fitness_function_rhythm import rhythm_fitness_funcs
    from fitness_function_pitch import pitch_fitness_funcs
    print(f"✓ 已导入 {len(rhythm_fitness_funcs)} 个节奏函数")
    print(f"✓ 已导入 {len(pitch_fitness_funcs)} 个音高函数")
except ImportError as e:
    print(f"错误: {e}")
    exit(1)

# 导入主程序的核心功能
from main import (
    SCALES, Individual, run_genetic_algorithm, 
    save_to_midi, debug_genome, RESULTS_DIR
)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  批量音乐生成 - 所有适应度函数组合")
    print("="*70)
    
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
    print(f"音阶: {len(scale_notes)} 个音\n")
    
    # 计算总组合数
    total_combinations = len(pitch_fitness_funcs) * len(rhythm_fitness_funcs)
    
    print(f"⚠️  将生成 {total_combinations} 个不同的音乐文件")
    print(f"    预计耗时: 约 {total_combinations * 2} 分钟")
    
    confirm = input("\n确认继续？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("已取消")
        exit(0)
    
    print("\n开始批量生成...\n")
    
    # 运行所有组合
    current = 0
    start_time = time.time()
    
    for rhythm_func in rhythm_fitness_funcs:
        for pitch_func in pitch_fitness_funcs:
            current += 1
            
            # 生成函数名
            func_name = f"{rhythm_func.__name__}_{pitch_func.__name__}"
            
            print(f"\n{'='*70}")
            print(f"[{current}/{total_combinations}] 组合: {func_name}")
            print(f"{'='*70}")
            
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
            
            # 显示进度
            elapsed = time.time() - start_time
            avg_time = elapsed / current
            remaining = (total_combinations - current) * avg_time
            print(f"\n进度: {current}/{total_combinations} ({current/total_combinations*100:.1f}%)")
            print(f"已用时间: {elapsed/60:.1f} 分钟")
            print(f"预计剩余: {remaining/60:.1f} 分钟")
    
    total_time = time.time() - start_time
    
    print("\n" + "="*70)
    print("  ✓ 所有组合生成完毕！")
    print("="*70)
    print(f"\n总共生成: {total_combinations} 个文件")
    print(f"总耗时: {total_time/60:.1f} 分钟")
    print(f"文件位置: {RESULTS_DIR}/")
    print(f"\n运行 'python playmid.py' 播放所有音乐")

