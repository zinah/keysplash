WHITE_KEYS_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
BLACK_KEYS_NOTES = ["C#", "D#", "F#", "G#", "A#"]
# TODO better data structure to indicate "index" or placement on the keyboard
# for each note
NOTES = WHITE_KEYS_NOTES + BLACK_KEYS_NOTES
OCTAVES = list(range(3, 8))
NOTES_IN_OCTAVE = len(NOTES)

white_keys_notes = [(note, octave) for octave in OCTAVES for note in WHITE_KEYS_NOTES]


def note_to_number(note, octave):
    note = NOTES.index(note)
    note += NOTES_IN_OCTAVE * octave
    return note


def play_note(fs, note_name):
    note_midi_value = note_to_number(*note_name)
    fs.noteon(0, note_midi_value, 60)
