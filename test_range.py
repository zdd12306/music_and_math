#!/usr/bin/env python3
"""
测试音域扩展 - 验证 F3(53) 到 G5(79) 的音域范围
"""

from main import SCALES, Individual, generate_scale_in_range

print("="*70)
print("  音域扩展测试：F3(53) ~ G5(79)")
print("="*70)

# 测试每个调式的音阶生成
print("\n【调式音阶测试】\n")
for scale_name, scale_notes in SCALES.items():
    print(f"{scale_name:12} : {len(scale_notes):2}个音")
    print(f"  音域: {scale_notes[0]} ({scale_notes[0]}) ~ {scale_notes[-1]} ({scale_notes[-1]})")
    print(f"  跨度: {scale_notes[-1] - scale_notes[0]} 个半音")
    print(f"  音符: {scale_notes[:5]}...{scale_notes[-3:]}")
    print()

# 验证音域范围
print("\n【音域验证】\n")
all_in_range = True
for scale_name, scale_notes in SCALES.items():
    min_pitch = min(scale_notes)
    max_pitch = max(scale_notes)
    
    if min_pitch < 53 or max_pitch > 79:
        print(f"❌ {scale_name}: 超出范围！ ({min_pitch} ~ {max_pitch})")
        all_in_range = False
    else:
        print(f"✓ {scale_name}: 在范围内 ({min_pitch} ~ {max_pitch})")

if all_in_range:
    print("\n🎉 所有调式都在 F3(53) ~ G5(79) 范围内！")
else:
    print("\n⚠️  部分调式超出指定范围")

# 测试个体生成
print("\n" + "="*70)
print("【个体生成测试】")
print("="*70)

scale = SCALES['C_major']
ind = Individual(scale_notes=scale)

print(f"\n调式: C_major")
print(f"音阶大小: {len(scale)} 个音")
print(f"音高基因长度: {len(ind.pitch_genes)}")
print(f"音高基因范围: {min(ind.pitch_genes)} ~ {max(ind.pitch_genes)}")
print(f"音高基因示例: {ind.pitch_genes}")

# 解码测试
notes = ind.to_notes()
if notes:
    pitches = [n[0] for n in notes]
    print(f"\n解码结果:")
    print(f"  生成了 {len(notes)} 个音符")
    print(f"  音高范围: {min(pitches)} ~ {max(pitches)}")
    print(f"  MIDI音符: {pitches}")
    
    # 验证所有音符都在调式内
    all_in_scale = all(p in scale for p in pitches)
    if all_in_scale:
        print(f"  ✓ 所有音符都在调式内")
    else:
        print(f"  ❌ 有音符超出调式")
        out_of_scale = [p for p in pitches if p not in scale]
        print(f"  超出的音符: {out_of_scale}")
else:
    print("  警告: 没有生成音符")

# 音域利用率测试
print("\n" + "="*70)
print("【音域利用率测试】")
print("="*70)

for scale_name in ['C_major', 'G_major', 'A_minor']:
    scale = SCALES[scale_name]
    
    # 生成多个个体，统计音域使用情况
    all_pitches = []
    for _ in range(20):
        ind = Individual(scale_notes=scale)
        notes = ind.to_notes()
        all_pitches.extend([n[0] for n in notes])
    
    if all_pitches:
        unique_pitches = sorted(set(all_pitches))
        coverage = len(unique_pitches) / len(scale) * 100
        
        print(f"\n{scale_name}:")
        print(f"  可用音: {len(scale)} 个")
        print(f"  实际使用: {len(unique_pitches)} 个 ({coverage:.1f}%)")
        print(f"  音域: {min(all_pitches)} ~ {max(all_pitches)} (跨度 {max(all_pitches)-min(all_pitches)} 半音)")

print("\n" + "="*70)
print("✅ 音域扩展测试完成！")
print("="*70)
print("\n现在可以生成 F3(53) 到 G5(79) 范围内的旋律了！")
print("运行 'python main.py' 开始生成音乐。")

