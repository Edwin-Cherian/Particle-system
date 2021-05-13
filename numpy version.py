import numpy as np
import pygame
import time
import random


#----WINDOW SETTINGS---->
WIDTH = 900
HEIGHT = 900

#<----COLOURS---->
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)


#<----SETUP PYGAME WINDOW---->
pygame.init()
pygame.display.set_caption("moving particles")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 600



def createpoints(n):
    coords = np.random.randint(50, 850, size=(n,2))
    velocities = np.random.randint(-10, 10, size=(n,2))
    colours = np.zeros((n,1))
    return np.concatenate((coords,velocities,colours),axis=1)

def updatepoints(points):
    points[:,0] = points[:,0] + points[:,2]
    points[:,1] = points[:,1] + points[:,3]
    points[:,2] = np.where((points[:,0]>50) & (points[:,0]<850),points[:,2], -points[:,2])
    points[:,3] = np.where((points[:,1]>50) & (points[:,1]<850),points[:,3], -points[:,3])

    coords = points[:,:2]
    differences = coords.reshape(1000,1,2)-coords
    i = np.arange(1000)
    differences[i,i] = np.inf
    distances = (differences**2).sum(2) ## gets euclidean distance from every other point
    neighbours = np.argmin(distances,1) ## returns indexes of nearest particle for every particle
    neighbourdist = (coords - coords[neighbours])
    neighbourdist = (neighbourdist**2).sum(1)
    points[:,4] = np.where(neighbourdist[:]<100,1,0)
    return points

def wallcollision():
    pass

def drawpoint(x,y,colour):
    if colour == 0:
        pygame.draw.circle(screen, GREEN, (x,y), 5)
    else:
        pygame.draw.circle(screen, RED, (x,y), 5)



drawpoint = np.frompyfunc(drawpoint, 3, 0) ##(function, No.inputs, No.outputs)

points = createpoints(1000)

stop = False
#<----RUN PROGRAM IN PYGAME---->
run = True
while run:
    clock.tick(fps)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pass
    start=time.perf_counter()
    if not stop:
        c=0
        points = updatepoints(points)
        points

    drawpoint(points[:,0], points[:,1], points[:,4]) ##plots all points
    print(1/(time.perf_counter()-start))

    pygame.display.update()