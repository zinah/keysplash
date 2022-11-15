import fluidsynth


WHITE_KEYS_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
BLACK_KEYS_NOTES = ["C#", "D#", "F#", "G#", "A#"]
# TODO better data structure to indicate "index" or placement on the keyboard
# for each note
NOTES = WHITE_KEYS_NOTES + BLACK_KEYS_NOTES
OCTAVES = list(range(3, 8))
NOTES_IN_OCTAVE = len(NOTES)

white_keys_notes = [(note, octave) for octave in OCTAVES for note in WHITE_KEYS_NOTES]


def note_to_midi_number(note: str, octave: int) -> int:
    """
    Translate note (e.g. C) and octave (e.g. 4) to MIDI note number.
    """
    midi_note_number = NOTES.index(note)
    midi_note_number += NOTES_IN_OCTAVE * octave
    return midi_note_number


def play_note(fs: fluidsynth.Synth, note: str, octave: int) -> None:
    """
    Play MIDI note via synthesiser.
    """
    note_midi_value = note_to_midi_number(note, octave)
    fs.noteon(0, note_midi_value, 60)
