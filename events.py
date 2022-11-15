from __future__ import annotations
import sys

import fluidsynth
import pygame

from const import NOTES_KEYBINDS


NoteName = str
Octave = int
Note = tuple[NoteName, Octave]


def check_quit_game(event: pygame.event.Event, fs: fluidsynth.Synth) -> None:
    """
    Check if the game has ended, if so, clean up.
    """
    if event.type == pygame.QUIT:
        pygame.quit()
        fs.delete()
        sys.exit()


def check_note_pressed(event: pygame.event.Event) -> Note | tuple[None, None]:
    """
    Returns note name (e.g. C#) and octave if note detected.
    """
    if event.type == pygame.KEYDOWN and event.key in NOTES_KEYBINDS:
        return NOTES_KEYBINDS[event.key]
    return (None, None)
