from math import cos, pi, sin
from random import choice, gauss, randint, uniform
import sys

import pygame

from colors import linear_gradient

pygame.init()

game_running = True
max_x = 1024
max_y = 568
background_color = (30, 30, 30)

pygame.display.set_caption("KeySplash!")
window = pygame.display.set_mode((max_x, max_y + 200))
window.fill(background_color)

pygame.display.update()

clock = pygame.time.Clock()
fps = 60

step = 5
beams = []
explosions = []
note_highlights = []
explosion_max_ticks = 100

octaves = 4
white_keys_in_octave = 7
black_keys_in_octave = 5
white_keys_no = octaves * white_keys_in_octave + 1
key_width = max_x // white_keys_no
offset = (max_x - white_keys_no * key_width) // 2
white_keys_x_coords = [offset + i * key_width for i in range(0, white_keys_no)]
black_keys_x_coords = [
    offset + 0.75 * key_width + i * key_width
    for i in range(0, 28)
    if (i - 2) % 7 != 0 and (i - 6) % 7 != 0 or i == 0
]

white_keys_notes = [
    "C2",
    "D2",
    "E2",
    "F2",
    "G2",
    "A2",
    "B2",
    "C3",
    "D3",
    "E3",
    "F3",
    "G3",
    "A3",
    "B3",
    "C4",
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
    "B4",
    "C5",
    "D5",
    "E5",
    "F5",
    "G5",
    "A5",
    "B5",
    "C6",
]

white_keys = dict(zip(white_keys_notes, white_keys_x_coords))
white_keys_keybinds = {
    pygame.K_1: "C2",
    pygame.K_2: "D2",
    pygame.K_3: "E2",
    pygame.K_4: "F2",
    pygame.K_5: "G2",
    pygame.K_6: "A2",
    pygame.K_7: "B2",
    pygame.K_q: "C3",
    pygame.K_w: "D3",
    pygame.K_e: "E3",
    pygame.K_r: "F3",
    pygame.K_t: "G3",
    pygame.K_y: "A3",
    pygame.K_u: "B3",
    pygame.K_a: "C4",
    pygame.K_s: "D4",
    pygame.K_d: "E4",
    pygame.K_f: "F4",
    pygame.K_g: "G4",
    pygame.K_h: "A4",
    pygame.K_j: "B4",
    pygame.K_z: "C5",
    pygame.K_x: "D5",
    pygame.K_c: "E5",
    pygame.K_v: "F5",
    pygame.K_b: "G5",
    pygame.K_n: "A5",
    pygame.K_m: "B5",
    pygame.K_SPACE: "C6",
}

gradient = dict(
    zip(
        white_keys_notes,
        linear_gradient((255, 0, 0), (0, 0, 255), len(white_keys_notes)),
    )
)


def draw_keyboard():
    pygame.draw.rect(window, (255, 255, 255), (0, max_y, max_x, 200), 0)
    # borders on each side of the keyboard
    pygame.draw.rect(window, background_color, (0, max_y, offset, 200), 0)
    pygame.draw.rect(window, background_color, (max_x - offset, max_y, offset, 200), 0)

    for x in white_keys_x_coords:
        pygame.draw.rect(window, background_color, (x, max_y, key_width, 200), 2)
    for x in black_keys_x_coords:
        pygame.draw.rect(window, (0, 0, 0), (x, max_y, key_width // 2, 100), 0)


def move_beam(x, y):
    return x, y + step


def get_key_color(key):
    return gradient[key]


def draw_and_move_explosion(explosion):
    next_explosion_placement = []
    for particle in explosion:
        particle_coords, color, ticks_left = particle
        x, y = particle_coords
        pygame.draw.circle(window, color, particle_coords, randint(1, 3), 1)
        if ticks_left - 1 > 0:
            next_explosion_placement.append([[x, y + 1], color, ticks_left - 1])
    return next_explosion_placement


# TODO more realistic explosions
def explode(origin_x, origin_y, color):
    number_of_points = 100
    boom_particles = []
    mean_radius = 20
    sigma_radius = 50

    for i in range(number_of_points):
        theta = uniform(0, 2 * pi)
        radius = gauss(mean_radius, sigma_radius)
        x = origin_x + radius * cos(theta)
        y = origin_y + radius * sin(theta)
        boom_particles.append([[x, y], color, explosion_max_ticks])
    return boom_particles


# creating a running loop
while game_running:
    # Setup background and keyboard
    window.fill(background_color)
    draw_keyboard()

    # creating a loop to check events that are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # checking if keydown event happened
        # TODO Choose color and postion based on which key was pressed
        if event.type == pygame.KEYDOWN:
            note_pressed = white_keys_keybinds.get(event.key, None)
            if note_pressed:
                key_color = get_key_color(note_pressed)
                new_highlight = pygame.Rect(
                    *[white_keys.get(note_pressed), max_y], key_width, 200
                )
                note_highlights.append([new_highlight, key_color, 15])

                new_beam = pygame.Rect(
                    *[white_keys.get(note_pressed), 0], key_width, key_width
                )
                # TODO choose color that is not too close to the background color
                beams.append([new_beam, key_color])

    ticks = pygame.time.get_ticks()
    new_beams = []
    new_explosions = []
    new_highlights = []

    for beam, color in beams:
        new_x, new_y = move_beam(*beam.topleft)
        if new_y + key_width < max_y:
            beam.topleft = (new_x, new_y)
            new_beams.append([beam, color])
        else:
            # the origin of the explosion should be in the middle of the top of the beam
            explosions.append(explode(new_x + key_width // 2, new_y, color))
        window.fill(color, beam)
    beams = new_beams

    for explosion in explosions:
        next_explosion_placement = draw_and_move_explosion(explosion)
        if next_explosion_placement:
            new_explosions.append(next_explosion_placement)
    explosions = new_explosions

    for highlight, color, ticks_left in note_highlights:
        window.fill(color, highlight)
        if ticks_left - 1 > 0:
            new_highlights.append([highlight, color, ticks_left - 1])
    note_highlights = new_highlights

    clock.tick(fps)
    pygame.display.flip()
