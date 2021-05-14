# todo update to use multiple physics loops per draw loop
# todo add resizable
"""
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZEABLE)
...
if event.type == pygame.VIDEO_RESIZE:
    screen = pygame.display.set_mode((event.x, event.y), pygame.RESIZEABLE)

reformat functions using WIDTH, HEIGHT to use screen.get_size() or assign values to WIDTH, HEIGHT

if you are drawing before resizing:
...
if event.type === pygame.VIDEO_RESIZE:
    old_screen = screen
    screen = pygame.display.set_mode((event.x, event.y), pygame.RESIZEABLE)
    screen.blit(old_screen)
    del old_screen
"""
from physics import Solver, FixedGrid, Particle
from pygame import Color, Vector2
import pygame
import random

# pygame settings
WIDTH = 400
HEIGHT = 400
FPS = 60

# performance tracking stuff
frame_rates = [0. for _ in range(600)]  # used to get an average framerate from the past x frames

# colours
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
BLUE = Color(0, 0, 255)
LIGHT_BLUE = Color(128, 128, 255)

# setup pygame
pygame.init()
pygame.display.set_caption("Particle Collisions")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# setup particles
grid = FixedGrid(screen.get_rect(), 75)
solver = Solver(screen.get_rect(), grid)
for i in range(500):
    x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
    vx, vy = 100 * random.random(), 100 * random.random()
    radius = 3 * random.random() + 2
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
    solver.step(delta_t / 1000)
    for particle in grid.children:
        pygame.draw.circle(screen, BLACK, particle.pos, particle.radius)

    # update display
    pygame.display.flip()
    # print framerate to console
    frame_rates.pop(0)
    frame_rates.append(clock.get_fps())
    print("\r", flush=True, end="")
    print(f"{sum(frame_rates) / len(frame_rates):.2f}", end="", flush=False)
