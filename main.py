# todo update to use multiple physics loops per draw loop
# todo view collisions
from physics import Solver, FixedGrid, Particle
from pygame import Color
import pygame
import random

# settings
<<<<<<< Updated upstream
SIZE = 400
PARTICLES = 500
GRID_DIVISIONS = 75
MIN_VELOCITY = 20
MAX_VELOCITY = 100
MIN_RADIUS = 2
MAX_RADIUS = 5
FPS = 1000

# performance tracking stuff
frame_rates = [60. for _ in range(600)]  # used to get an average framerate from the past x frames
=======
SIZE = 800
PARTICLES = 1000
GRID_DIVISIONS = 75
MIN_VELOCITY = -50
MAX_VELOCITY = 50
MIN_RADIUS = 3
MAX_RADIUS = 6
FPS = 1000

# performance tracking stuff
frame_rates = [60. for _ in range(15)]  # used to get an average framerate from the past x frames
>>>>>>> Stashed changes

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
grid = FixedGrid(SIZE, GRID_DIVISIONS)
solver = Solver(SIZE, grid)
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
    solver.step(delta_t / 1000)
    for particle in grid.children:
<<<<<<< Updated upstream
        pygame.draw.circle(screen, BLACK, particle.pos, particle.radius)
=======
        if not particle.collided:
            pygame.draw.circle(screen, BLACK, particle.pos, particle.radius)
        else:
            pygame.draw.circle(screen, RED, particle.pos, particle.radius)
            particle.collided = False
>>>>>>> Stashed changes

    # update display
    pygame.display.flip()
    # print framerate to console
    frame_rates.pop(0)
    frame_rates.append(clock.get_fps())
    print("\r", flush=True, end="")
<<<<<<< Updated upstream
    print(f"{sum(frame_rates) / len(frame_rates):.2f}", end="", flush=False)
=======
    print(f"{sum(frame_rates) / len(frame_rates):.2f}", end="", flush=False)
>>>>>>> Stashed changes
