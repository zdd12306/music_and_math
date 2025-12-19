import pretty_midi

midi_data = pretty_midi.PrettyMIDI("output_fitness_function_7.mid")

# 1. Check Pitch Range
pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
if pitches:
    print(f"Pitch Range: {min(pitches)} to {max(pitches)}")

# 2. Check Total Duration
print(f"Total Duration: {midi_data.get_end_time()} seconds")

# 3. Check for Scale Consistency
# (You can count how many notes fall outside your target scale)