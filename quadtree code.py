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



class Circle:
    def __init__(self,x=200,y=200,r=10):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.r, width=1)


class Qt:
    def __init__(self, x, y, w, h, capacity=1, divided=False):
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
        try:
            self.nw.draw()
            self.ne.draw()
            self.sw.draw()
            self.se.draw()
        except:
            pass
        if len(self.points) < self.capacity:
            pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h], width=1)
        else:
            pygame.draw.rect(screen, RED, [self.x, self.y, self.w, self.h], width=1)

    def highlight(self):
        pygame.draw.rect(screen, CYAN, [self.x, self.y, self.w, self.h], width=1)

    def intersect(self, area):
        return not(self.x>area.x+area.r or self.x+self.w<area.x-area.r or
                   self.y>area.y+area.r or self.y+self.w<area.y-area.r)

    def query(self, area):
        result = []
        if self.intersect(area):
            if not self.divided:
                for point in self.points:
                    if point.contained(area):
                        result.append(point)
            else:
                for point in self.points:
                    if point.contained(area):
                        result.append(point)
                result.extend(self.nw.query(area) + self.ne.query(area) + self.se.query(area) + self.sw.query(area))
        return result

    def subdivide(self):
        #print("Subtrees created")
        self.divided = True
        self.nw = Qt(self.x, self.y, self.w/2, self.h/2)
        self.ne = Qt(self.x+self.w/2, self.y, self.w/2, self.h/2)
        self.sw = Qt(self.x, self.y+self.h/2, self.w/2, self.h/2)
        self.se = Qt(self.x+self.w/2, self.y+self.h/2, self.w/2, self.h/2)


class Particle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = random.randint(-3,3)
        self.vy = random.randint(-3,3)

    def checkcollision(self):
        qresults = qt.query(Circle(self.x, self.y, self.r))
        try:
            if len(qresults)>1:
                for qresult in qresults:
                    qresult.highlight()

        except:
            pass

    def contained(self, area):
        #if area.x-area.r <= self.x <= area.x+area.r and area.y-area.r <= self.y <= area.y+area.r:
        if (self.x-area.x)**2 + (self.y-area.y)**2 <= (self.r*2)**2:
            return True
        return False

    def drawparticle(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.r)

    def highlight(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x-self.r < 0 or self.x+self.r > WIDTH:
            self.vx *= -1


        if self.y-self.r<0 or self.y+self.r>HEIGHT:
            self.vy *= -1

particles=[Particle(random.randint(1,WIDTH),random.randint(1,HEIGHT), 3) for i in range(1000)]
qt=Qt(0,0,WIDTH,HEIGHT)


print(qt.__dict__)
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



    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        x,y = pygame.mouse.get_pos()
        particles.append(Particle(x,y,10))
        qt.addpoint(Particle(x,y,10))

    #qt.draw()

    s=time.perf_counter()
    qt=Qt(0,0,WIDTH,HEIGHT)
    for particle in particles:
        particle.move()
        qt.addpoint(particle)
        particle.drawparticle()

        particle.checkcollision()

    print(1/(time.perf_counter()-s))
    pygame.display.update()