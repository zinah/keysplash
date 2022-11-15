import fluidsynth
import pygame

from calculate import explode
from const import (
    BACKGROUND_COLOR,
    MAX_X,
    MAX_Y,
    NOTES_KEYBINDS,
    SF_PATH,
    WINDOW_TITLE,
)
from draw import (
    draw_explosion,
    draw_highlight,
    draw_keyboard,
    key_width,
    gradient,
    white_keys,
)
from events import check_note_pressed, check_quit_game
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


def move_beam(x, y):
    return x, y + step


def get_key_color(key):
    return gradient[key]


def make_highlight(note, octave):
    return pygame.Rect(*[white_keys.get((note, octave)), MAX_Y], key_width, 200)


def make_beam(note, octave):
    return pygame.Rect(*[white_keys.get((note, octave)), 0], key_width, key_width)


def move_explosion(explosion):
    next_explosion_placement = []
    for particle in explosion:
        particle_coords, color, ticks_left = particle
        x, y = particle_coords
        if ticks_left - 1 > 0:
            next_explosion_placement.append([[x, y + 1], color, ticks_left - 1])
    return next_explosion_placement


fs = fluidsynth.Synth()
fs.start(driver="alsa")
sfid = fs.sfload(SF_PATH)
fs.program_select(0, sfid, 0, 0)


while game_running:
    # Check for events
    for event in pygame.event.get():
        # Clean up if the game has ended
        check_quit_game(event, fs)

        note, octave = check_note_pressed(event)
        if note and octave:
            play_note(fs, note, octave)
            key_color = get_key_color((note, octave))
            note_highlights.append([make_highlight(note, octave), key_color, 15])
            beams.append([make_beam(note, octave), key_color])

    # Reset display
    window.fill(BACKGROUND_COLOR)
    draw_keyboard(window, BACKGROUND_COLOR, 0, MAX_Y, MAX_X, 200)

    new_beams = []
    new_explosions = []
    new_highlights = []

    for beam, color in beams:
        # Draw the beam
        window.fill(color, beam)
        # Move the beam
        new_x, new_y = move_beam(*beam.topleft)
        # Beam has not collided with the keyboard yet
        if new_y + key_width < MAX_Y:
            beam.topleft = (new_x, new_y)
            new_beams.append([beam, color])
        # Beam reached the keyboard
        else:
            # The origin of the explosion should be in the middle of the top of the beam
            explosions.append(explode(new_x + key_width // 2, new_y, color))
    beams = new_beams

    for explosion in explosions:
        draw_explosion(window, explosion)
        next_explosion_placement = move_explosion(explosion)
        if next_explosion_placement:
            new_explosions.append(next_explosion_placement)
    explosions = new_explosions

    for highlight, color, ticks_left in note_highlights:
        draw_highlight(window, color, highlight)
        if ticks_left - 1 > 0:
            new_highlights.append([highlight, color, ticks_left - 1])
    note_highlights = new_highlights

    clock.tick(fps)
    pygame.display.flip()
