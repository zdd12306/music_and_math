import pretty_midi
import os
import glob

def evaluate_midi(midi_path):
    """分析单个MIDI文件"""
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        
        # 1. Check Pitch Range
        pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
        if pitches:
            print(f"  音高范围: {min(pitches)} ~ {max(pitches)} (跨度 {max(pitches)-min(pitches)} 半音)")
        
        # 2. Check Total Duration
        print(f"  总时长: {midi_data.get_end_time():.2f} 秒")
        
        # 3. Check number of notes
        note_count = len(pitches)
        print(f"  音符数量: {note_count}")
        
    except Exception as e:
        print(f"  错误: {e}")

def evaluate_all_midis(directory="results"):
    """批量分析MIDI文件"""
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return
    
    midi_files = glob.glob(os.path.join(directory, "*.mid"))
    
    if not midi_files:
        print(f"在 {directory}/ 中没有找到MIDI文件")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return
    
    print(f"在 {directory}/ 中找到 {len(midi_files)} 个MIDI文件\n")
    print("="*70)
    
    for midi_file in midi_files:
        print(f"\n{os.path.basename(midi_file)}:")
        evaluate_midi(midi_file)
    
    print("\n" + "="*70)
    print("✓ 分析完成")

if __name__ == "__main__":
    # 如果只想分析特定文件，取消下面的注释并修改文件名
    # evaluate_midi("results/output_C_major_rhythm_fitness_basic_pitch_fitness_stepwise.mid")
    
    # 分析results文件夹中的所有MIDI文件
    evaluate_all_midis("results")