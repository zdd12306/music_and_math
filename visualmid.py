import pypianoroll
import matplotlib.pyplot as plt
import os
import glob
from music21 import converter

def visualize_all_midis(input_dir=".", output_dir="plots"):
    """
    Scans directory for MIDIs and saves both Piano Roll and Staff images.
    """
    # 1. Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 2. Find all MIDI files
    midi_files = glob.glob(os.path.join(input_dir, "**/*.mid"), recursive=True)
    
    if not midi_files:
        print("No MIDI files found to visualize.")
        return

    print(f"Found {len(midi_files)} files. Generating visualizations...")

    for file_path in midi_files:
        # Get base name without extension for naming images
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"  Processing: {base_name}")

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
                print(f"    Staff export failed for {base_name} (Check MuseScore installation).")

        except Exception as e:
            print(f"    Error processing {base_name}: {e}")

    print(f"\nAll visualizations saved in the '{output_dir}' folder.")

if __name__ == "__main__":
    visualize_all_midis()