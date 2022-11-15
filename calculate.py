from math import cos, pi, sin
from random import gauss, uniform

from const import DROPLET_STEP, EXPLOSION_MAX_TICKS


def move_droplet(x, y):
    return x, y + DROPLET_STEP


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
        boom_particles.append([[x, y], color, EXPLOSION_MAX_TICKS])
    return boom_particles


def move_explosion(explosion):
    next_explosion_placement = []
    for particle in explosion:
        particle_coords, color, ticks_left = particle
        x, y = particle_coords
        if ticks_left - 1 > 0:
            next_explosion_placement.append([[x, y + 1], color, ticks_left - 1])
    return next_explosion_placement