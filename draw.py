from random import randint

import pygame

from colors import linear_gradient
from const import MAX_X, MAX_Y
from music import white_keys_notes

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

gradient = dict(
    zip(
        white_keys_notes,
        linear_gradient((255, 0, 0), (0, 0, 255), white_keys_no),
    )
)


def draw_keyboard(surface, bg_color, x, y, width, height):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 0)
    # borders on each side of the keyboard
    pygame.draw.rect(surface, bg_color, (x, y, offset, height), 0)
    pygame.draw.rect(surface, bg_color, (width - offset, y, offset, height), 0)

    for x in white_keys_x_coords:
        pygame.draw.rect(surface, black, (x, MAX_Y, key_width, 200), 2)
    for x in black_keys_x_coords:
        pygame.draw.rect(surface, black, (x, MAX_Y, key_width // 2, 100), 0)


def draw_explosion(surface, explosion):
    for particle_coords, color, _ in explosion:
        pygame.draw.circle(surface, color, particle_coords, randint(1, 3), 1)


def draw_highlight(surface, color, highlight):
    surface.fill(color, highlight)