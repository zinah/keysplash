from math import cos, pi, sin
from random import gauss, randint, uniform
import sys

import fluidsynth
import pygame

from const import (
    BACKGROUND_COLOR,
    MAX_X,
    MAX_Y,
    NOTES_KEYBINDS,
    SF_PATH,
    WINDOW_TITLE,
)
from draw import draw_keyboard, key_width, gradient, white_keys
from music import play_note


pygame.init()
game_running = True

pygame.display.set_caption(WINDOW_TITLE)
window = pygame.display.set_mode((MAX_X, MAX_Y + 200))
window.fill(BACKGROUND_COLOR)
pygame.display.update()

clock = pygame.time.Clock()
fps = 60

step = 5
beams = []
explosions = []
note_highlights = []
explosion_max_ticks = 100



def check_note_pressed(event):
    """
    Returns note name (e.g. C#) and octave if note detected
    """
    if event and event.type == pygame.KEYDOWN and event.key in NOTES_KEYBINDS:
        return NOTES_KEYBINDS[event.key]
    return (None, None)


def move_beam(x, y):
    return x, y + step


def get_key_color(key):
    return gradient[key]


def make_highlight(note, octave):
    return pygame.Rect(
        *[white_keys.get((note, octave)), MAX_Y], key_width, 200
    )


def make_beam(note, octave):
    return pygame.Rect(
        *[white_keys.get((note, octave)), 0], key_width, key_width
    )


def draw_and_move_explosion(explosion):
    next_explosion_placement = []
    for particle in explosion:
        particle_coords, color, ticks_left = particle
        x, y = particle_coords
        pygame.draw.circle(window, color, particle_coords, randint(1, 3), 1)
        if ticks_left - 1 > 0:
            next_explosion_placement.append([[x, y + 1], color, ticks_left - 1])
    return next_explosion_placement


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


fs = fluidsynth.Synth()
fs.start(driver="alsa")
sfid = fs.sfload(SF_PATH)
fs.program_select(0, sfid, 0, 0)

# creating a running loop
while game_running:
    # Setup background and keyboard
    window.fill(BACKGROUND_COLOR)
    draw_keyboard(window, BACKGROUND_COLOR, 0, MAX_Y, MAX_X, 200)

    # creating a loop to check events that are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            fs.delete()
            sys.exit()

        note, octave = check_note_pressed(event)
        if note and octave:
            play_note(fs, note, octave)
            key_color = get_key_color((note, octave))
            note_highlights.append([make_highlight(note, octave), key_color, 15])
            beams.append([make_beam(note, octave), key_color])

    ticks = pygame.time.get_ticks()
    new_beams = []
    new_explosions = []
    new_highlights = []

    for beam, color in beams:
        new_x, new_y = move_beam(*beam.topleft)
        if new_y + key_width < MAX_Y:
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
