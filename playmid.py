import pygame
import os
import glob

def play_all_midis(directory="."):
    """
    Scans the directory for all .mid files and plays them sequentially.
    """
    # Initialize pygame mixer
    pygame.init()
    pygame.mixer.init()
    
    # Use glob to find all .mid files in the current folder and subfolders
    # recursive=True allows searching through subdirectories
    midi_files = glob.glob(os.path.join(directory, "**/*.mid"), recursive=True)
    
    if not midi_files:
        print(f"No MIDI files found in: {os.path.abspath(directory)}")
        return

    print(f"Found {len(midi_files)} MIDI files. Starting playback...")
    print("Press Ctrl+C to skip the current song and move to the next.")

    for i, file_path in enumerate(midi_files):
        print(f"\n[{i+1}/{len(midi_files)}] Playing: {os.path.basename(file_path)}")
        
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Keep the script alive while the music plays
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except KeyboardInterrupt:
            # Catching Ctrl+C to skip the song
            print("\n  >> Skipped by user.")
            pygame.mixer.music.stop()
            continue 
        except Exception as e:
            print(f"  Error playing {file_path}: {e}")

    print("\nAll MIDI files have been played.")
    pygame.quit()

if __name__ == "__main__":
    # You can change "." to a specific folder path if your files are elsewhere
    play_all_midis(".")