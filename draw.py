from random import randint

import pygame

from const import MAX_X, MAX_Y
from music import white_keys_notes


NoteName = str
Octave = int
Coordinates = tuple[int, int]
RGBColor = tuple[int, int, int]
TickCounter = int
Explosion = list[Coordinates, RGBColor, TickCounter]

black = (0, 0, 0)

octaves = 4
white_keys_in_octave = 7
black_keys_in_octave = 5
white_keys_no = octaves * white_keys_in_octave + 1
key_width = MAX_X // white_keys_no
offset = (MAX_X - white_keys_no * key_width) // 2
white_keys_x_coords = [offset + i * key_width for i in range(0, white_keys_no)]
black_keys_x_coords = [
    offset + 0.75 * key_width + i * key_width
    for i in range(0, 28)
    if (i - 2) % 7 != 0 and (i - 6) % 7 != 0 or i == 0
]


white_keys = dict(zip(white_keys_notes, white_keys_x_coords))


def make_highlight(note: NoteName, octave: Octave) -> pygame.Rect:
    """
    Create the highlight object to cover the pressed key to indicate that it was
    pressed.
    """
    return pygame.Rect(*[white_keys.get((note, octave)), MAX_Y], key_width, 200)


def make_droplet(note: NoteName, octave: Octave) -> pygame.Rect:
    """
    Create the droplet object that will move down from the top of the screen
    and fall on the specific key that was pressed.
    """
    return pygame.Rect(*[white_keys.get((note, octave)), 0], key_width, key_width)


# TODO Pass in the keys coords, don't use globals
def draw_keyboard(
    surface: pygame.Surface, bg_color: RGBColor, x: int, y: int, width: int, height: int
) -> None:
    """
    Draw the musical keyboard.
    """
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 0)
    # borders on each side of the keyboard
    pygame.draw.rect(surface, bg_color, (x, y, offset, height), 0)
    pygame.draw.rect(surface, bg_color, (width - offset, y, offset, height), 0)

    for x in white_keys_x_coords:
        pygame.draw.rect(surface, black, (x, MAX_Y, key_width, 200), 2)
    for x in black_keys_x_coords:
        pygame.draw.rect(surface, black, (x, MAX_Y, key_width // 2, 100), 0)


def draw_droplet(
    surface: pygame.Surface, color: RGBColor, droplet: pygame.Rect
) -> None:
    """
    Draw a droplet.
    """
    surface.fill(color, droplet)


def draw_explosion(surface: pygame.Surface, explosion: Explosion) -> None:
    """
    Draw the particles in an explosion.
    """
    for particle_coords, color, _ in explosion:
        pygame.draw.circle(surface, color, particle_coords, randint(1, 3), 1)


def draw_highlight(
    surface: pygame.Surface, color: RGBColor, highlight: pygame.Rect
) -> None:
    """
    Draw the highlight on a key.
    """
    surface.fill(color, highlight)
