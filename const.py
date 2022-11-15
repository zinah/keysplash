import pygame

WINDOW_TITLE = "KeySplash!"
FPS = 60

# TODO better naming, these are boundaries of the space where droplets can fall
MAX_X = 1024
MAX_Y = 568
BACKGROUND_COLOR = (30, 30, 30)

SF_PATH = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

# The speed of the droplet falling, pixels per tick
DROPLET_STEP = 5

# The speed of the particles in an explosion falling
EXPLOSION_STEP = 1
# How long the explosion stays behind
EXPLOSION_MAX_TICKS = 100
EXPLOSION_NUMBER_OF_POINTS = 100
# Parameters for Gauss distribution of the explosion radius - mean and stadard
# deviation
EXPLOSION_MEAN_RADIUS = 20
EXPLOSION_SIGMA_RADIUS = 50

NOTES_KEYBINDS = {
    pygame.K_1: ("C", 3),
    pygame.K_2: ("D", 3),
    pygame.K_3: ("E", 3),
    pygame.K_4: ("F", 3),
    pygame.K_5: ("G", 3),
    pygame.K_6: ("A", 3),
    pygame.K_7: ("B", 3),
    pygame.K_q: ("C", 4),
    pygame.K_w: ("D", 4),
    pygame.K_e: ("E", 4),
    pygame.K_r: ("F", 4),
    pygame.K_t: ("G", 4),
    pygame.K_y: ("A", 4),
    pygame.K_u: ("B", 4),
    pygame.K_a: ("C", 5),
    pygame.K_s: ("D", 5),
    pygame.K_d: ("E", 5),
    pygame.K_f: ("F", 5),
    pygame.K_g: ("G", 5),
    pygame.K_h: ("A", 5),
    pygame.K_j: ("B", 5),
    pygame.K_z: ("C", 6),
    pygame.K_x: ("D", 6),
    pygame.K_c: ("E", 6),
    pygame.K_v: ("F", 6),
    pygame.K_b: ("G", 6),
    pygame.K_n: ("A", 6),
    pygame.K_m: ("B", 6),
    pygame.K_SPACE: ("C", 7),
}
