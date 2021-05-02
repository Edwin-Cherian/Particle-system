import pygame
import random
import math
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
pygame.display.set_caption("Moving particles")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60

class Particle:
    def __init__(self, x=0, y=0, vel=0, angle=0, acc=0, size=10):
        self.x = random.randint(50,700)
        self.y = random.randint(50,700)
        self.vel = random.randint(10,12)
        self.angle = random.random()*2*math.pi
        self.acc = acc
        self.size = size

    def move(self):
        self.x += self.vel * math.cos(self.angle)
        self.y += self.vel * math.sin(self.angle)
        if self.x<0 or self.x>WIDTH:
            self.angle = self.angle*-1 + math.pi

        if self.y<0 or self.y>HEIGHT:
            self.angle *= -1




particles = [Particle() for i in range(5)]
print(particles[0].__dict__)

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
        pygame.draw.circle(screen, BLACK, (particle.x, particle.y), particle.size)
        particle.move()
    #print(1/(time.perf_counter()-s))
    pygame.display.update()