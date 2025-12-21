#!/usr/bin/env python3
"""
快速测试脚本 - 验证系统是否正常工作
Quick Test Script

运行此脚本以验证：
1. 所有模块可以正确导入
2. 双基因编码系统工作正常
3. 适应度函数可以正确计算
4. MIDI文件可以正确生成
"""

def test_system():
    print("="*60)
    print("  音乐遗传算法系统 - 快速测试")
    print("="*60)
    
    # 测试1: 导入模块
    print("\n[1/5] 测试模块导入...")
    try:
        from main import Individual, SCALES, MelodyAdapter, save_to_midi
        from fitness_function_rhythm import rhythm_fitness_funcs
        from fitness_function_pitch import pitch_fitness_funcs
        print(f"  ✓ 成功导入所有模块")
        print(f"  ✓ 节奏函数: {len(rhythm_fitness_funcs)} 个")
        print(f"  ✓ 音高函数: {len(pitch_fitness_funcs)} 个")
        print(f"  ✓ 可生成组合: {len(rhythm_fitness_funcs) * len(pitch_fitness_funcs)} 种")
    except Exception as e:
        print(f"  ✗ 导入失败: {e}")
        return False
    
    # 测试2: 创建个体
    print("\n[2/5] 测试个体创建...")
    try:
        scale = SCALES['C_major']
        ind = Individual(scale_notes=scale)
        print(f"  ✓ 成功创建个体")
        print(f"  - 节奏基因长度: {len(ind.rhythm_genes)}")
        print(f"  - 音高基因长度: {len(ind.pitch_genes)}")
        print(f"  - 节奏基因示例: {ind.rhythm_genes[:8]}")
        print(f"  - 音高基因示例: {ind.pitch_genes[:8]}")
    except Exception as e:
        print(f"  ✗ 创建失败: {e}")
        return False
    
    # 测试3: 解码为音符
    print("\n[3/5] 测试基因解码...")
    try:
        notes = ind.to_notes()
        print(f"  ✓ 成功解码为 {len(notes)} 个音符")
        if notes:
            print(f"  - 第一个音符: 音高={notes[0][0]}, 开始时间={notes[0][1]}, 时值={notes[0][2]}")
    except Exception as e:
        print(f"  ✗ 解码失败: {e}")
        return False
    
    # 测试4: 计算适应度
    print("\n[4/5] 测试适应度计算...")
    try:
        adapter = MelodyAdapter(notes, ind.rhythm_genes, ind.pitch_genes)
        
        # 测试节奏适应度
        r_func = rhythm_fitness_funcs[0]
        r_score = r_func(adapter)
        print(f"  ✓ 节奏适应度 ({r_func.__name__}): {r_score:.2f}")
        
        # 测试音高适应度
        p_func = pitch_fitness_funcs[0]
        p_score = p_func(adapter)
        print(f"  ✓ 音高适应度 ({p_func.__name__}): {p_score:.2f}")
        
        print(f"  ✓ 总适应度: {r_score + p_score:.2f}")
    except Exception as e:
        print(f"  ✗ 计算失败: {e}")
        return False
    
    # 测试5: 生成MIDI文件
    print("\n[5/5] 测试MIDI文件生成...")
    try:
        test_filename = "test_output.mid"
        save_to_midi(ind, test_filename)
        
        import os
        if os.path.exists(test_filename):
            file_size = os.path.getsize(test_filename)
            print(f"  ✓ MIDI文件已生成")
            print(f"  - 文件名: {test_filename}")
            print(f"  - 文件大小: {file_size} 字节")
            
            # 清理测试文件
            os.remove(test_filename)
            print(f"  ✓ 测试文件已清理")
        else:
            print(f"  ✗ 文件未生成")
            return False
    except Exception as e:
        print(f"  ✗ 生成失败: {e}")
        return False
    
    # 全部通过
    print("\n" + "="*60)
    print("  🎉 所有测试通过！系统工作正常！")
    print("="*60)
    print("\n可以运行以下命令开始生成音乐：")
    print("  python main.py")
    print("\n查看README.md了解更多使用方法。")
    return True

if __name__ == "__main__":
    import sys
    success = test_system()
    sys.exit(0 if success else 1)

