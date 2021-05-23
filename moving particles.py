import pygame
import random
import time


#----WINDOW SETTINGS---->
WIDTH = 900
HEIGHT = 900

#<----COLOURS---->
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)


#<----SETUP PYGAME WINDOW---->
pygame.init()
pygame.display.set_caption("Pairwise collision detection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60


#<----SIMULATION VARIABLES---->
MINVELOCITY = -5
MAXVELOCITY = 5
PARTICLES = 100


class Particle:
    def __init__(self, x, y, xvel, yvel, size=3):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.xvel = random.randint(MINVELOCITY, MAXVELOCITY)
        self.yvel = random.randint(MINVELOCITY, MAXVELOCITY)
        self.size = size


    def checkcollision(self, particles):
        for particle in particles:
            # checking if 2 particles are overlapping
            if not (self.x+self.size<particle.x-particle.size or self.x-self.size>particle.x+particle.size or
                self.y+self.size<particle.y-particle.size or self.y-self.size>particle.y+particle.size):
                if particle != self:
                    self.highlight()


    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x,self.y), self.size)


    def highlight(self):
        pygame.draw.circle(screen, RED, (self.x,self.y), self.size)


    def move(self, particles):
        self.x += self.xvel
        self.y += self.yvel
        if self.x-self.size < 0 or self.x+self.size > WIDTH:
            self.xvel *= -1

        if self.y-self.size<0 or self.y+self.size>HEIGHT:
            self.yvel *= -1

        self.draw()
        self.checkcollision(particles)





particles = [Particle() for i in range(100)]

#<----RUN PROGRAM IN PYGAME---->
run = True
while run:
    clock.tick(fps)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pass
    s=time.perf_counter()
    for particle in particles:
        particle.move(particles)
    #print(1/(time.perf_counter()-s)) # outputs fps for running the collision detection
    pygame.display.update()
