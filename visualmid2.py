from music21 import converter, environment

# 1. Setup (Run this once to tell music21 where MuseScore is)
# On Windows, it usually looks like this:
# us = environment.UserSettings()
# us['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'

# 2. Load your MIDI file
midi_file_path = 'output_fitness_function_7.mid'
score = converter.parse(midi_file_path)

# 3. Generate the staff notation
# This will open the notation in MuseScore or your default MusicXML viewer
score.show('text')

# Optional: If you want to see a text-based representation of the notes/staff
# score.show('text')