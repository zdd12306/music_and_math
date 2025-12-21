#!/usr/bin/env python3
"""
消融实验脚本 (Ablation Study)
Ablation Study Script

系统性地测试每个适应度函数的独立贡献
总共12个实验：1个基线 + 5个音高 + 5个节奏 + 1个完整组合
"""

import os
import sys

# 导入配置和主程序
from config import (
    RHYTHM_WEIGHTS, PITCH_WEIGHTS, DEFAULT_SCALE,
    reset_to_default_weights
)
from main import (
    Individual, run_genetic_algorithm, save_to_midi, debug_genome,
    SCALES
)
from fitness_function_rhythm import rhythm_fitness_overall
from fitness_function_pitch import pitch_fitness_overall


# 定义12个消融实验配置
ABLATION_EXPERIMENTS = [
    # ========== 实验1：基线 ==========
    {
        'id': 1,
        'name': 'baseline',
        'description': '基线（无约束）',
        'purpose': '了解无约束情况下的随机结果',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_01_baseline.mid'
    },
    
    # ========== 实验2-6：单独测试每个音高函数 ==========
    {
        'id': 2,
        'name': 'pitch_stepwise',
        'description': '音高-级进流畅',
        'purpose': '测试级进流畅的效果（小音程）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 1, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_02_pitch_stepwise.mid'
    },
    {
        'id': 3,
        'name': 'pitch_consonance',
        'description': '音高-音程协和',
        'purpose': '测试音程协和度的效果（协和音程）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 1, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_03_pitch_consonance.mid'
    },
    {
        'id': 4,
        'name': 'pitch_range',
        'description': '音高-音域平衡',
        'purpose': '测试音域控制的效果（适中音域）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 1, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_04_pitch_range.mid'
    },
    {
        'id': 5,
        'name': 'pitch_direction',
        'description': '音高-方向变化',
        'purpose': '测试旋律方向变化的效果（起伏丰富）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 1, 'climax': 0}
        },
        'filename': 'ablation_05_pitch_direction.mid'
    },
    {
        'id': 6,
        'name': 'pitch_climax',
        'description': '音高-旋律高潮',
        'purpose': '测试旋律高潮的效果（有明显高潮点）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 1}
        },
        'filename': 'ablation_06_pitch_climax.mid'
    },
    
    # ========== 实验7-11：单独测试每个节奏函数 ==========
    {
        'id': 7,
        'name': 'rhythm_parity',
        'description': '节奏-节奏奇性',
        'purpose': '测试节奏奇性的效果（避免对称）',
        'weights': {
            'rhythm': {'parity': 1, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_07_rhythm_parity.mid'
    },
    {
        'id': 8,
        'name': 'rhythm_density',
        'description': '节奏-节奏密度',
        'purpose': '测试节奏密度控制的效果（音符密度适中）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 1, 'syncopation': 0, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_08_rhythm_density.mid'
    },
    {
        'id': 9,
        'name': 'rhythm_syncopation',
        'description': '节奏-切分音',
        'purpose': '测试切分音的效果（节奏变化丰富）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 1, 'rest': 0, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_09_rhythm_syncopation.mid'
    },
    {
        'id': 10,
        'name': 'rhythm_rest',
        'description': '节奏-休止符分布',
        'purpose': '测试休止符分布的效果（适当的休止）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 1, 'pattern': 0},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_10_rhythm_rest.mid'
    },
    {
        'id': 11,
        'name': 'rhythm_pattern',
        'description': '节奏-节奏模式',
        'purpose': '测试节奏模式的效果（规律性）',
        'weights': {
            'rhythm': {'parity': 0, 'density': 0, 'syncopation': 0, 'rest': 0, 'pattern': 1},
            'pitch': {'stepwise': 0, 'consonance': 0, 'range': 0, 'direction': 0, 'climax': 0}
        },
        'filename': 'ablation_11_rhythm_pattern.mid'
    },
    
    # ========== 实验12：完整组合 ==========
    {
        'id': 12,
        'name': 'full_combination',
        'description': '完整组合（最优）',
        'purpose': '测试所有函数组合的效果',
        'weights': {
            'rhythm': {'parity': 1, 'density': 1, 'syncopation': 1, 'rest': 1, 'pattern': 1},
            'pitch': {'stepwise': 1, 'consonance': 1, 'range': 1, 'direction': 1, 'climax': 1}
        },
        'filename': 'ablation_12_full.mid'
    },
]


def set_weights(weight_config):
    """根据配置设置权重（直接赋值，不使用乘法）"""
    for key, value in weight_config['rhythm'].items():
        RHYTHM_WEIGHTS[key] = value
    for key, value in weight_config['pitch'].items():
        PITCH_WEIGHTS[key] = value


def run_ablation_study(scale_name=None):
    """
    运行完整的消融实验
    总共12个实验：1基线 + 5音高 + 5节奏 + 1完整
    """
    
    if scale_name is None:
        scale_name = DEFAULT_SCALE
    
    scale_notes = SCALES[scale_name]
    results_dir = "results"
    
    # 确保results文件夹存在
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"✓ 已创建 {results_dir}/ 文件夹")
    
    # 打印实验概览
    print("\n" + "="*70)
    print("  消融实验 (Ablation Study)")
    print("="*70)
    print(f"\n调式: {scale_name}")
    print(f"音阶大小: {len(scale_notes)} 个音")
    print(f"\n实验设计（共 {len(ABLATION_EXPERIMENTS)} 个实验）:")
    print(f"  实验1: 基线（无约束）")
    print(f"  实验2-6: 单独测试5个音高函数")
    print(f"  实验7-11: 单独测试5个节奏函数")
    print(f"  实验12: 完整组合（所有函数）")
    print("="*70)
    
    # 循环运行每个实验
    for i, experiment in enumerate(ABLATION_EXPERIMENTS, 1):
        total = len(ABLATION_EXPERIMENTS)
        
        print(f"\n[实验{i}/{total}] {experiment['description']}")
        print("-"*70)
        print(f"目的: {experiment['purpose']}")
        
        # 设置权重
        set_weights(experiment['weights'])
        
        # 运行遗传算法
        best_ind = run_genetic_algorithm(
            rhythm_fitness_overall,
            pitch_fitness_overall,
            scale_notes,
            func_name=experiment['name']
        )
        
        # 输出结果
        debug_genome(best_ind)
        save_to_midi(best_ind, experiment['filename'])
    
    # 实验完成总结
    print("\n" + "="*70)
    print("  ✓ 消融实验完成！")
    print("="*70)
    print(f"\n生成了 {len(ABLATION_EXPERIMENTS)} 个MIDI文件:")
    print(f"\n基线:")
    print(f"  results/{ABLATION_EXPERIMENTS[0]['filename']}")
    print(f"\n音高函数（实验2-6）:")
    for exp in ABLATION_EXPERIMENTS[1:6]:
        print(f"  results/{exp['filename']:35} - {exp['description']}")
    print(f"\n节奏函数（实验7-11）:")
    for exp in ABLATION_EXPERIMENTS[6:11]:
        print(f"  results/{exp['filename']:35} - {exp['description']}")
    print(f"\n完整组合:")
    print(f"  results/{ABLATION_EXPERIMENTS[11]['filename']}")
    
    print(f"\n运行 'python playmid.py' 播放所有结果")
    
    print(f"\n关键对比:")
    print(f"  • 基线 vs 单个函数 → 每个函数的独立作用")
    print(f"  • 音高函数之间 → 不同音高策略的效果")
    print(f"  • 节奏函数之间 → 不同节奏策略的效果")
    print(f"  • 单个函数 vs 完整组合 → 函数协同效果")


if __name__ == "__main__":
    print("\n消融实验")
    print("测试10个适应度函数：")
    print("  音高函数（5个）:")
    print("    1. stepwise - 级进流畅")
    print("    2. consonance - 音程协和")
    print("    3. range - 音域平衡")
    print("    4. direction - 方向变化")
    print("    5. climax - 旋律高潮")
    print("  节奏函数（5个）:")
    print("    6. parity - 节奏奇性")
    print("    7. density - 节奏密度")
    print("    8. syncopation - 切分音")
    print("    9. rest - 休止符分布")
    print("    10. pattern - 节奏模式")
    print(f"\n总实验数: {len(ABLATION_EXPERIMENTS)} 个")
    print(f"预计耗时: 约 {len(ABLATION_EXPERIMENTS) * 2}-{len(ABLATION_EXPERIMENTS) * 4} 分钟")
    
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
