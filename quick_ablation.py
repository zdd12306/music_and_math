#!/usr/bin/env python3
"""
快速消融测试 (Quick Ablation Test)

快速测试单个函数的效果，不需要运行完整的消融实验
"""

import sys

# 导入配置
from config import (
    enable_single_rhythm_function,
    enable_single_pitch_function,
    reset_to_default_weights,
    RHYTHM_WEIGHTS,
    PITCH_WEIGHTS
)

def show_current_weights():
    """显示当前权重配置"""
    print("\n当前权重配置:")
    print("\n节奏权重:")
    for key, value in RHYTHM_WEIGHTS.items():
        status = "✓" if value > 0 else "✗"
        print(f"  {status} {key:12} = {value}")
    
    print("\n音高权重:")
    for key, value in PITCH_WEIGHTS.items():
        status = "✓" if value > 0 else "✗"
        print(f"  {status} {key:12} = {value}")

def main():
    print("="*60)
    print("  快速消融测试工具")
    print("="*60)
    
    show_current_weights()
    
    print("\n可用操作:")
    print("  1. 测试单个节奏函数")
    print("  2. 测试单个音高函数")
    print("  3. 测试节奏+音高组合")
    print("  4. 恢复默认权重")
    print("  5. 查看当前权重")
    print("  6. 运行主程序")
    print("  0. 退出")
    
    while True:
        choice = input("\n请选择操作 (0-6): ").strip()
        
        if choice == '1':
            print("\n可用的节奏函数:")
            for i, key in enumerate(RHYTHM_WEIGHTS.keys(), 1):
                print(f"  {i}. {key}")
            func_choice = input("选择函数编号: ").strip()
            try:
                func_idx = int(func_choice) - 1
                func_name = list(RHYTHM_WEIGHTS.keys())[func_idx]
                weight = input(f"设置权重 (默认1.0): ").strip()
                weight = float(weight) if weight else 1.0
                enable_single_rhythm_function(func_name, weight)
                show_current_weights()
            except (ValueError, IndexError):
                print("无效选择")
        
        elif choice == '2':
            print("\n可用的音高函数:")
            for i, key in enumerate(PITCH_WEIGHTS.keys(), 1):
                print(f"  {i}. {key}")
            func_choice = input("选择函数编号: ").strip()
            try:
                func_idx = int(func_choice) - 1
                func_name = list(PITCH_WEIGHTS.keys())[func_idx]
                weight = input(f"设置权重 (默认1.0): ").strip()
                weight = float(weight) if weight else 1.0
                enable_single_pitch_function(func_name, weight)
                show_current_weights()
            except (ValueError, IndexError):
                print("无效选择")
        
        elif choice == '3':
            print("\n设置节奏函数:")
            for i, key in enumerate(RHYTHM_WEIGHTS.keys(), 1):
                print(f"  {i}. {key}")
            r_choice = input("选择节奏函数: ").strip()
            
            print("\n设置音高函数:")
            for i, key in enumerate(PITCH_WEIGHTS.keys(), 1):
                print(f"  {i}. {key}")
            p_choice = input("选择音高函数: ").strip()
            
            try:
                r_idx = int(r_choice) - 1
                p_idx = int(p_choice) - 1
                r_name = list(RHYTHM_WEIGHTS.keys())[r_idx]
                p_name = list(PITCH_WEIGHTS.keys())[p_idx]
                
                # 先全部清零
                for key in RHYTHM_WEIGHTS:
                    RHYTHM_WEIGHTS[key] = 0.0
                for key in PITCH_WEIGHTS:
                    PITCH_WEIGHTS[key] = 0.0
                
                # 启用选定的函数
                RHYTHM_WEIGHTS[r_name] = 1.0
                PITCH_WEIGHTS[p_name] = 1.0
                
                print(f"\n✓ 已启用组合: rhythm_{r_name} + pitch_{p_name}")
                show_current_weights()
            except (ValueError, IndexError):
                print("无效选择")
        
        elif choice == '4':
            reset_to_default_weights()
            show_current_weights()
        
        elif choice == '5':
            show_current_weights()
        
        elif choice == '6':
            print("\n正在运行主程序...")
            import main
            break
        
        elif choice == '0':
            print("退出")
            break
        
        else:
            print("无效选择，请输入0-6")

if __name__ == "__main__":
    main()

