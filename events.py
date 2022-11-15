import sys

import pygame

from const import NOTES_KEYBINDS


def check_quit_game(event, fs):
    if event.type == pygame.QUIT:
        pygame.quit()
        fs.delete()
        sys.exit()


def check_note_pressed(event):
    """
    Returns note name (e.g. C#) and octave if note detected
    """
    if event.type == pygame.KEYDOWN and event.key in NOTES_KEYBINDS:
        return NOTES_KEYBINDS[event.key]
    return (None, None)
