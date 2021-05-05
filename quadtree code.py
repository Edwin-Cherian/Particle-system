import random
import pygame
import time


#----WINDOW SETTINGS---->
WIDTH = 800
HEIGHT = 800


#<----COLOURS---->
WHITE = (100,100,100)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CYAN = (0,255,255)


#<----SETUP PYGAME WINDOW---->
pygame.init()
pygame.display.set_caption("Quad tree")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 100


class Rectangle:
    def __init__(self,x=200,y=200,w=200,h=200):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        pygame.draw.rect(screen, BLUE, [self.x, self.y, self.w, self.h], width=1)

        
class Qt:
    def __init__(self, x, y, w, h, capacity=2, divided=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.points = []
        self.capacity = capacity
        self.divided = divided

    def addpoint(self, point):
        if self.x < point.x <= self.x+self.w and self.y < point.y <= self.y+self.h:
            if len(self.points) < self.capacity:
                self.points.append(point)              
            else:
                if not self.divided:
                    self.subdivide()
                self.nw.addpoint(point)
                self.ne.addpoint(point)
                self.sw.addpoint(point)
                self.se.addpoint(point)

    def draw(self):
        if len(self.points) < self.capacity:
            pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h], width=1)
        else:
            pygame.draw.rect(screen, RED, [self.x, self.y, self.w, self.h], width=1)
        if self.divided:
            self.nw.draw()
            self.ne.draw()
            self.sw.draw()
            self.se.draw()

    def highlight(self):
        pygame.draw.rect(screen, CYAN, [self.x, self.y, self.w, self.h], width=1)

    def intersect(self, area):
        return not(self.x>area.x+area.w or self.x+self.w<area.x or
                   self.y>area.y+area.w or self.y+self.w<area.y)

    def query(self, area):
        result = []
        if self.intersect(area):
            if area.x<=self.x and self.x+self.w<=area.x+area.w and area.y<=self.y and self.y+self.h<=area.y+area.h:##qt fits fully inside query
                if not self.divided:
                    result.extend(self.points)
                else:
                    result.extend(self.points + self.nw.query(area) + self.ne.query(area) + self.sw.query(area) + self.se.query(area))
                    self.highlight()
            else:
                if not self.divided:
                    for point in self.points:
                        if point.contained(area):
                            result.append(point)
                else:
                    for point in self.points:
                        if point.contained(area):
                            result.append(point)
                    result.extend(self.nw.query(area) + self.ne.query(area) + self.sw.query(area) + self.se.query(area))
        return result

    def subdivide(self):
        self.divided = True
        self.nw = Qt(self.x, self.y, self.w/2, self.h/2)
        self.ne = Qt(self.x+self.w/2, self.y, self.w/2, self.h/2)
        self.sw = Qt(self.x, self.y+self.h/2, self.w/2, self.h/2)
        self.se = Qt(self.x+self.w/2, self.y+self.h/2, self.w/2, self.h/2)

        
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def contained(self, area):
        if area.x <= self.x <= area.x+area.w and area.y <= self.y <= area.y+area.h:
            return True
        return False

    def drawparticle(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 10)

    def highlight(self):
        pygame.draw.circle(screen, CYAN, (self.x, self.y), 10)

        
particles=[Particle(random.randint(1,WIDTH),random.randint(1,HEIGHT)) for i in range(0)]
qt=Qt(0,0,WIDTH,HEIGHT)
for particle in particles:
    qt.addpoint(particle)
    

#<----RUN PROGRAM IN PYGAME---->
run = True
while run:
    clock.tick(fps)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_KP_PLUS:
                fps += 1
            elif event.key == pygame.K_KP_MINUS:
                fps -= 1
            elif event.key == pygame.K_r:
                qt = Qt(0,0,WIDTH,HEIGHT)
                particles = []

    search = Rectangle(pygame.mouse.get_pos()[0]-100,pygame.mouse.get_pos()[1]-100,200,200)

    s=time.perf_counter()
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        x,y = pygame.mouse.get_pos()
        particles.append(Particle(x,y))
        qt.addpoint(Particle(x,y))

    qt.draw()
    for particle in particles:
        particle.drawparticle()
    search.draw()

    qresults = qt.query(search)
    try:
        for qresult in qresults:
            qresult.highlight()
    except:
        pass
    print(len(qresults))
    print(1/(time.perf_counter()-s))
    pygame.display.update()
