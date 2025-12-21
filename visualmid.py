import pypianoroll
import matplotlib.pyplot as plt
import os
import glob
from music21 import converter

def visualize_all_midis(input_dir="results", output_dir="results/plots"):
    """
    Scans directory for MIDIs and saves both Piano Roll and Staff images.
    Default input is 'results' folder where generated MIDI files are stored.
    """
    # 1. Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 '{input_dir}' 不存在")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return
    
    # 2. Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ 已创建输出目录: {output_dir}/")
    
    # 3. Find all MIDI files
    midi_files = glob.glob(os.path.join(input_dir, "**/*.mid"), recursive=True)
    
    if not midi_files:
        print(f"在 {input_dir}/ 中没有找到MIDI文件")
        print(f"请先运行 'python main.py' 生成音乐文件")
        return

    print(f"在 {input_dir}/ 中找到 {len(midi_files)} 个文件，开始生成可视化...\n")

    for file_path in midi_files:
        # Get base name without extension for naming images
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"  处理: {base_name}")

        try:
            # --- A. Save Piano Roll Plot ---
            multitrack = pypianoroll.read(file_path)
            # Adjusting figure size for better readability
            multitrack.plot()
            plt.title(f"Piano Roll: {base_name}")
            plt.savefig(os.path.join(output_dir, f"{base_name}_pianoroll.png"), dpi=150)
            plt.close()

            # --- B. Save Musical Staff (MusicXML/PNG) ---
            # This requires MuseScore installed for background conversion
            score = converter.parse(file_path)
            # We save as PNG directly if your environment supports it
            # Otherwise, .show() opens it in MuseScore
            try:
                score.write('musicxml.png', fp=os.path.join(output_dir, f"{base_name}_staff.png"))
            except Exception as e:
                print(f"    五线谱导出失败 (需要安装MuseScore)")

        except Exception as e:
            print(f"    错误: {e}")

    print(f"\n✓ 所有可视化已保存到 '{output_dir}/' 文件夹")

if __name__ == "__main__":
    visualize_all_midis()