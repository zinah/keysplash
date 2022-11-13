from random import randint, sample
import sys

import pygame

pygame.init()

game_running = True
max_x = 1024
max_y = 768
background_color = (30, 30, 30)

pygame.display.set_caption("KeySplash!")
window = pygame.display.set_mode((max_x, max_y))
window.fill(background_color)
pygame.display.update()

clock = pygame.time.Clock()
fps = 60
speed = 20
next_tick = 500

step = 5
beam_width = 20
beams = []
explosions = []
explosion_max_ticks = 100

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
def explode(origin_x, color):
    number_of_points = 30
    boom_particles = []
    # TODO make it more of a round explosion, use a point of origin and radius instead
    # and find random points within a half-circle
    x_coords = sample(range(origin_x - 150, origin_x + 150), number_of_points)
    y_coords = sample(range(max_y - 200, max_y - 5), number_of_points)
    for i, x in enumerate(x_coords):
        boom_particles.append([[x, y_coords[i]], color, explosion_max_ticks])
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
                new_beam = pygame.Rect(*[randint(0, 800 - beam_width), 0], 20, 20)
                # TODO choose color that is not too close to the background color
                key_color = get_key_color(pygame.key.get_pressed())
                beams.append([new_beam, key_color])
    ticks = pygame.time.get_ticks()
    new_beams = []
    new_explosions = []
    if ticks > next_tick:
        next_tick += speed
        window.fill(background_color)

        for beam, color in beams:
            new_x, new_y = move_beam(*beam.topleft)
            if new_y < max_y:
                beam.topleft = (new_x, new_y)
                new_beams.append([beam, color])
            else:
                # the origin of the explosion should be in the middle of the top of the beam
                explosions.append(explode(new_x + beam_width // 2, color))
            window.fill(color, beam)
        beams = new_beams

        for explosion in explosions:
            next_explosion_placement = draw_and_move_explosion(explosion)
            if next_explosion_placement:
                new_explosions.append(next_explosion_placement)
        explosions = new_explosions

        clock.tick(fps)
        pygame.display.flip()
