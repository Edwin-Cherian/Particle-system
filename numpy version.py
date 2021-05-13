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
fps = 60
particles = 1000



def createpoints(n):
    coords = np.random.randint(50, 850, size=(n,2))
    velocities = np.random.randint(-10, 10, size=(n,2))
    colours = np.zeros((n,1))
    radii = np.random.randint(1,2, size=(n,2))
    return np.concatenate((coords,velocities,colours,radii),axis=1)

def updatepoints(points):
    points[:,0] = points[:,0] + points[:,2] ## updates all the x coords by adding on the x velocities
    points[:,1] = points[:,1] + points[:,3] ## updates all the y coords by adding on the y velocities
    points[:,2] = np.where((points[:,0]>50) & (points[:,0]<850),points[:,2], -points[:,2]) ## prevents particles from escaping to the left/right
    points[:,3] = np.where((points[:,1]>50) & (points[:,1]<850),points[:,3], -points[:,3]) ## prevents particles from escaping to the top/bottom

    coords = points[:,:2] ## gets xy coords of all points
    differences = coords.reshape(particles,1,2)-coords ## gets the x and y difference between every particle from every other particle
    i = np.arange(particles)
    differences[i,i] = np.inf ## prevents nearest neighbour being the particle itself
    distances = (differences**2).sum(2) ## gets euclidean distance from every other point
    neighbours = np.argmin(distances,1) ## returns indexes of nearest particle for every particle
    neighbourdist = (coords - coords[neighbours]) ## gets the x and y difference of the particle and the nearest particle to it
    euclideandist = (neighbourdist**2).sum(1) ## gets the squared euclidian distance between a particle and its nearest neighbour
    points[:,4] = np.where(euclideandist[:]<(points[:,5]+points[neighbours,5])**2,1,0) ## checks if particle is close enough to its nearest neighbour to be colliding essentially checking is distance is less than or equal to double the radius of the particle


    return points

def drawpoint(x,y,colour,radius):
    if colour == 0: ## this is 0 when a particle is not colliding with another particle
        pygame.draw.circle(screen, GREEN, (x,y), radius)
    else: ## otherwise it will be 1 if it is colliding with another particle
        pygame.draw.circle(screen, RED, (x,y), radius)



drawpoint = np.frompyfunc(drawpoint, 4, 0) ##(function, No.inputs, No.outputs)

points = createpoints(particles)

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

    drawpoint(points[:,0], points[:,1], points[:,4], points[:,5]) ##plots all points
    print(1/(time.perf_counter()-start))

    pygame.display.update()
