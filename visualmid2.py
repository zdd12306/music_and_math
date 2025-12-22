from music21 import converter, environment
import os
import glob

# 1. Setup (Run this once to tell music21 where MuseScore is)
# On Windows, it usually looks like this:
# us = environment.UserSettings()
# us['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'

def view_midi_score(midi_file_path):
    """在MuseScore中打开MIDI文件查看五线谱"""
    if not os.path.exists(midi_file_path):
        print(f"错误: 文件 '{midi_file_path}' 不存在")
        return
    
    print(f"正在打开: {midi_file_path}")
    
    # 2. Load your MIDI file
    score = converter.parse(midi_file_path)
    
    # 3. Generate the staff notation
    # This will open the notation in MuseScore or your default MusicXML viewer
    try:
        score.show()
    except:
        # 如果图形界面失败，显示文本版本
        print("\n五线谱文本表示:")
        score.show('text')

def list_midi_files(directory="results"):
    """列出results文件夹中的所有MIDI文件"""
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return []
    
    midi_files = glob.glob(os.path.join(directory, "*.mid"))
    return midi_files

if __name__ == "__main__":
    midi_files = list_midi_files("results")
    
    if not midi_files:
        print("在 results/ 中没有找到MIDI文件")
        print("请先运行 'python main.py' 生成音乐文件")
    else:
        print(f"在 results/ 中找到 {len(midi_files)} 个MIDI文件:\n")
        for i, f in enumerate(midi_files, 1):
            print(f"  {i}. {os.path.basename(f)}")
        
        # 打开第一个文件作为示例
        print(f"\n正在打开第一个文件...")
        view_midi_score(midi_files[0])
        
        # 如果想打开特定文件，取消下面的注释
        view_midi_score("/home/benyan2023/workspace/Homework/music_and_math/1766198607/output_fit_w_3.7_0.7_0.7.mid")