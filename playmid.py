import pygame
import os
import glob

def play_all_midis(directory="results"):
    """
    Scans the directory for all .mid files and plays them sequentially.
    Default directory is 'results' where generated MIDI files are stored.
    """
    # Initialize pygame mixer
    pygame.init()
    pygame.mixer.init()
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return
    
    # Use glob to find all .mid files in the current folder and subfolders
    # recursive=True allows searching through subdirectories
    midi_files = glob.glob(os.path.join(directory, "**/*.mid"), recursive=True)
    
    if not midi_files:
        print(f"在 {os.path.abspath(directory)} 中没有找到MIDI文件")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return

    print(f"在 {directory}/ 文件夹中找到 {len(midi_files)} 个MIDI文件")
    print("按 Ctrl+C 跳过当前曲目\n")

    for i, file_path in enumerate(midi_files):
        print(f"[{i+1}/{len(midi_files)}] 播放: {os.path.basename(file_path)}")
        
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Keep the script alive while the music plays
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except KeyboardInterrupt:
            # Catching Ctrl+C to skip the song
            print("  >> 已跳过\n")
            pygame.mixer.music.stop()
            continue 
        except Exception as e:
            print(f"  错误: {e}\n")

    print(f"\n✓ 所有MIDI文件播放完毕")
    pygame.quit()

if __name__ == "__main__":
    # You can change "results" to a specific folder path if your files are elsewhere
    play_all_midis("results")