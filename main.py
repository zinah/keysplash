import fluidsynth
import pygame

from colors import get_key_color, linear_gradient
from calculate import explode, move_droplet, move_explosion
from const import (
    BACKGROUND_COLOR,
    FPS,
    MAX_X,
    MAX_Y,
    EXPLOSION_NUMBER_OF_PARTICLES,
    EXPLOSION_MAX_TICKS,
    SF_PATH,
    WINDOW_TITLE,
)
from draw import (
    draw_droplet,
    draw_explosion,
    draw_highlight,
    draw_keyboard,
    make_droplet,
    make_highlight,
    key_width,
    white_keys,
)
from events import check_note_pressed, check_quit_game
from music import play_note


def main():
    pygame.init()
    game_running = True

    pygame.display.set_caption(WINDOW_TITLE)
    window = pygame.display.set_mode((MAX_X, MAX_Y + 200))
    window.fill(BACKGROUND_COLOR)
    pygame.display.update()

    clock = pygame.time.Clock()

    fs = fluidsynth.Synth()
    fs.start(driver="alsa")
    sfid = fs.sfload(SF_PATH)
    fs.program_select(0, sfid, 0, 0)

    gradient = dict(
        zip(
            white_keys,
            linear_gradient((255, 0, 0), (0, 0, 255), len(white_keys.keys())),
        )
    )

    droplets = []
    explosions = []
    note_highlights = []

    while game_running:
        # Check for events
        for event in pygame.event.get():
            # Clean up if the game has ended
            check_quit_game(event, fs)

            note, octave = check_note_pressed(event)
            if note and octave:
                play_note(fs, note, octave)
                key_color = get_key_color(gradient, (note, octave))
                note_highlights.append([make_highlight(note, octave), key_color, 15])
                droplets.append([make_droplet(note, octave), key_color])

        # Reset display
        window.fill(BACKGROUND_COLOR)
        draw_keyboard(window, BACKGROUND_COLOR, 0, MAX_Y, MAX_X, 200)

        new_droplets = []
        new_explosions = []
        new_highlights = []

        for droplet, color in droplets:
            # Draw the droplet
            draw_droplet(window, color, droplet)
            # Move the droplet
            new_x, new_y = move_droplet(*droplet.topleft)
            # droplet has not collided with the keyboard yet
            if new_y + key_width < MAX_Y:
                droplet.topleft = (new_x, new_y)
                new_droplets.append([droplet, color])
            # droplet reached the keyboard
            else:
                # The origin of the explosion should be in the middle of the top of the droplet
                explosions.append(
                    explode(
                        new_x + key_width // 2,
                        new_y,
                        color,
                        EXPLOSION_NUMBER_OF_PARTICLES,
                        EXPLOSION_MAX_TICKS,
                    )
                )
        droplets = new_droplets

        # Draw and move explosions
        for explosion in explosions:
            draw_explosion(window, explosion)
            next_explosion_placement = move_explosion(explosion)
            if next_explosion_placement:
                new_explosions.append(next_explosion_placement)
        explosions = new_explosions

        # Draw the highlights on the pressed keys
        for highlight, color, ticks_left in note_highlights:
            draw_highlight(window, color, highlight)
            if ticks_left - 1 > 0:
                new_highlights.append([highlight, color, ticks_left - 1])
        note_highlights = new_highlights

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
