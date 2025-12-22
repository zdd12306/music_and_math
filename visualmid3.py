from music21 import converter, note, chord

def get_lily_name(p):
    """
    Manually converts a music21 pitch to LilyPond format.
    C4 -> c', C5 -> c'', C3 -> c, C2 -> c,
    """
    # 1. Step (lowercase)
    step = p.step.lower()
    
    # 2. Accidental
    acc = ""
    if p.accidental:
        if p.accidental.name == 'sharp':
            acc = "is"
        elif p.accidental.name == 'flat':
            acc = "es"
            
    # 3. Octave markers
    # Middle C (C4) in LilyPond is c'
    octave_val = p.octave
    if octave_val >= 4:
        marks = "'" * (octave_val - 3)
    else:
        marks = "," * (3 - octave_val)
        
    return f"{step}{acc}{marks}"

def music21_to_lilypond(midi_path):
    score = converter.parse(midi_path)
    
    ly_code = [
        '\\header {',
        '  title = "GA Generated Melody"',
        '  composer = "PITCH_MAP: Manual Conversion"',
        '}',
        '\\score {',
        '  {',
        '    \\clef treble',
        '    \\key e \\major',
        '    \\time 4/4'
    ]
    
    # Mapping duration
    duration_map = {4.0: '1', 2.0: '2', 1.0: '4', 0.5: '8', 0.25: '16'}

    for n in score.flat.notesAndRests:
        dur = duration_map.get(n.quarterLength, '4')
        
        if n.isRest:
            ly_code.append(f"    r{dur}")
        elif n.isChord:
            # Handle chords
            pitches = [get_lily_name(p) for p in n.pitches]
            ly_code.append(f"    <{' '.join(pitches)}>{dur}")
        else:
            # Use our manual function
            pitch_name = get_lily_name(n.pitch)
            ly_code.append(f"    {pitch_name}{dur}")
            
    ly_code.extend(['  }', '  \\layout {}', '}'])
    return "\n".join(ly_code)

# Example usage:
print(music21_to_lilypond("/home/benyan2023/workspace/Homework/music_and_math/results/output_fit_w_3.7_0.7_0.7.mid"))