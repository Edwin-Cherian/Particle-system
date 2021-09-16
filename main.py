# todo update to use multiple physics loops per draw loop
# todo view collisions
from physics import ParticleEngine, FixedGrid, Particle
from pygame import Color
import pygame
import random

# settings
SIZE = 800
PARTICLES = 1000
CELL_SIZE = 5
MIN_VELOCITY = -100
MAX_VELOCITY = 100
MIN_RADIUS = 2
MAX_RADIUS = 2
TIMESCALE = 1
FPS = 600000

# performance tracking stuff
frame_rates = [0. for _ in range(60)]  # used to get average framerate over x frames

# colours
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
BLUE = Color(0, 0, 255)
LIGHT_BLUE = Color(128, 128, 255)

# setup pygame
pygame.init()
pygame.display.set_caption("Particle Collisions")
screen = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()
running = True

# setup particles
grid = FixedGrid.from_cell_size(SIZE, CELL_SIZE)
engine = ParticleEngine(SIZE, grid)
for i in range(PARTICLES):
    x, y = [random.randint(0, SIZE - 1) for _ in range(2)]
    vx, vy = [MIN_VELOCITY + (MAX_VELOCITY - MIN_VELOCITY) * random.random() for _ in range(2)]
    radius = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * random.random()
    grid.add_child(Particle(x, y, vx, vy, radius))

# program loop
while running:
    delta_t = clock.tick(FPS)
    screen.fill(WHITE)

    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update particles then draw
    engine.step(delta_t / 1000 * TIMESCALE)
    for particle in grid.children:
        engine.draw_particle(screen, particle, BLACK, RED)

    # update display
    pygame.display.flip()
    # print framerate to console
    frame_rates.pop(0)
    frame_rates.append(clock.get_fps())
    print("\r", flush=True, end="")
    print(f"{sum(frame_rates) / len(frame_rates):.2f}", end="", flush=False)
