from math import cos, pi, sin
from random import choice, gauss, randint, uniform
import sys

import pygame

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
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def draw_and_move_explosion(explosion):
    next_explosion_placement = []
    for particle in explosion:
        particle_coords, color, ticks = particle
        x, y = particle_coords
        pygame.draw.circle(window, color, particle_coords, randint(1, 3), 1)
        if ticks - 1 > 0:
            next_explosion_placement.append([[x, y + 1], color, ticks - 1])
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
        # TODO make it more of a round explosion, use a point of origin and radius instead
        # and find random points within a half-circle
        # x_coords = sample(range(origin_x - 150, origin_x + 150), number_of_points)
        # y_coords = sample(range(max_y - 200, max_y - 5), number_of_points)
        # for i, x in enumerate(x_coords):
        boom_particles.append([[x, y], color, explosion_max_ticks])
    return boom_particles


# creating a running loop
while game_running:
    # creating a loop to check events that are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # checking if keydown event happened
        # TODO Choose color and postion based on which key was pressed
        if event.type == pygame.KEYDOWN:
            new_beam = pygame.Rect(*[choice(white_keys_x_coords + black_keys_x_coords), 0], key_width, key_width)
            # TODO choose color that is not too close to the background color
            key_color = get_key_color(pygame.key.get_pressed())
            beams.append([new_beam, key_color])
    ticks = pygame.time.get_ticks()
    new_beams = []
    new_explosions = []

    # Setup background and keyboard
    window.fill(background_color)
    draw_keyboard()

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

    clock.tick(fps)
    pygame.display.flip()
