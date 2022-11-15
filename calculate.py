from math import cos, pi, sin
from random import gauss, uniform

from const import (
    DROPLET_STEP,
    EXPLOSION_MAX_TICKS,
    EXPLOSION_MEAN_RADIUS,
    EXPLOSION_NUMBER_OF_POINTS,
    EXPLOSION_SIGMA_RADIUS,
    EXPLOSION_STEP,
)


Coordinates = tuple[int, int]
RGBColor = tuple[int, int, int]
TickCounter = int
Explosion = list[Coordinates, RGBColor, TickCounter]


def move_droplet(x: int, y: int) -> Coordinates:
    """
    Move the droplet a step downward.
    """
    return x, y + DROPLET_STEP


def explode(origin_x: int, origin_y: int, color: RGBColor) -> Explosion:
    """
    Create a list of coordinates, colors and initial tick counters for particles
    being a result of a drop of origin coordinates meeting the keyboard
    boundaries.
    """
    boom_particles = []

    for i in range(EXPLOSION_NUMBER_OF_POINTS):
        theta = uniform(0, 2 * pi)
        radius = gauss(EXPLOSION_MEAN_RADIUS, EXPLOSION_SIGMA_RADIUS)
        x = origin_x + radius * cos(theta)
        y = origin_y + radius * sin(theta)
        boom_particles.append([[x, y], color, EXPLOSION_MAX_TICKS])
    return boom_particles


def move_explosion(explosion: Explosion) -> Explosion:
    """
    Move the coordinates of particles in an explosion a step downwards
    and reduce the tick counter.
    """
    next_explosion_placement = []
    for particle in explosion:
        particle_coords, color, ticks_left = particle
        x, y = particle_coords
        if ticks_left - 1 > 0:
            next_explosion_placement.append(
                [[x, y + EXPLOSION_STEP], color, ticks_left - 1]
            )
    return next_explosion_placement
