def str2midi(note):
    """
    Convert note name to MIDI number.
    
    Args:
    note (str): Note name in the format 'C4', 'D#5', etc.
    
    Returns:
    int: MIDI number corresponding to the input note.
    """
    notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
             'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
             'A#': 10, 'Bb': 10, 'B': 11}
    
    octave = int(note[-1])
    note_name = note[:-1]
    
    midi_number = (octave + 1) * 12 + notes[note_name]
    
    return midi_number

# # Example usage:
# print(str2midi('C4'))  # Output: 60
# print(str2midi('A#3')) # Output: 34


def midi2str(midi_number):
    """
    Convert MIDI number to note name.
    
    Args:
    midi_number (int): MIDI number.
    
    Returns:
    str: Note name corresponding to the input MIDI number.
    """
    notes = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#',
             7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
    
    note_name = notes[midi_number % 12]
    octave = (midi_number // 12) - 1
    
    return f"{note_name}{octave}"