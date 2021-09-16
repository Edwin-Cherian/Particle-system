import pygame
import time
import random


#----WINDOW SETTINGS---->
WIDTH = 800
HEIGHT = 800

#<----COLOURS---->
WHITE = (55,55,55)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,55,0)
BLUE = (0,0,255)
CYAN = (0,255,255)


#<----SETUP PYGAME WINDOW---->
pygame.init()
pygame.display.set_caption("Edwin's epic fixed grid")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60000

particles = 1000
dt = .1
divisions = 50

min_velocity = -10
max_velocity = 10
min_radius = 2
max_radius = 2



# performance tracking stuff
frame_rates = [60. for _ in range(50)]  # used to get an average framerate from the past x frames
avg_collisions = [60. for _ in range(50)]
collisions = 0


class Grid:
    def __init__(self,x,y,w,h,divisions):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.divisions = divisions
        self.cells = [None for i in range(self.divisions**2)]
        self.cellsize = WIDTH/self.divisions

    def create_cells(self):

        for i in range(self.divisions**2):
            self.cells[i] = Cell((i%self.divisions)*self.cellsize, (i//self.divisions)*self.cellsize, WIDTH/self.divisions, HEIGHT/self.divisions)
        #print(self.cells)

    def get_cell_xy(self, x, y):
        return int(y//self.cellsize), int(x//self.cellsize)

    def get_cell_index(self, x, y):
        row,col = self.get_cell_xy(x,y)
        return row*self.divisions + col # double check this makes sense

    def get_near(self, x, y, r):
        index = self.get_cell_index(x,y)
        cell = self.cells[index]
        other_cells  = [index]

        if x-r <= cell.x and y-r <= cell.y:
            other_cells.extend([index - 1, index - divisions - 1, index - divisions])#tl cell

        elif x+r >= cell.x + cell.w and y-r <= cell.y:
            other_cells.extend([index - divisions, index - divisions + 1, index + 1])#tr cell

        elif x-r <= cell.x and y+r >= cell.y + cell.h:
            other_cells.extend([index - 1, index + divisions - 1, index + divisions])#bl cell

        elif x+r >= cell.x + cell.w and y+r >= cell.y + cell.h:
            other_cells.extend([index + divisions, index + divisions + 1, index + 1])#br cell

        if x-r <= cell.x:
            other_cells.append(index - 1)

        elif x+r >= cell.x + cell.w:
            other_cells.append(index + 1)

        if y-r <= cell.y:
            other_cells.append(index - divisions)

        elif y+r >= cell.y + cell.h:
            other_cells.append(index + divisions)

        return other_cells #only gives indexes

    def add_particle(self, particle):
        index = self.get_cell_index(particle.x,particle.y) #maybe just use xy
        self.cells[index].add_particle(particle)
        particle.cell = self.cells[index]

    def remove_particle(self, particle):
        index = self.get_cell_index(particle.x,particle.y) #maybe just use xy

        self.cells[index].remove_particle()

    def update_grid(self):
        global collisions
        for cell in self.cells:
            #cell.draw()
            #cell.highlight()
            for particle in cell.particles:
                particle.update_pos()
                particle.test_collision() #Not drawing particles here cus it causes a jitter for some reason
                if particle.collided:
                    collisions +=1

        for cell in self.cells:
            for particle in cell.particles:
                particle.draw()


class Cell:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def remove_particle(self, particle):
        self.particles.remove(particle)

    def draw(self):
        pygame.draw.rect(screen, BLACK, [self.x, self.y, self.w, self.h], 1)

    def highlight(self):
        pygame.draw.rect(screen, CYAN, [self.x, self.y, self.w, self.h], 1) #used for debugging stuff

    def contains(self, particle):
        return not(self.x>particle.x+particle.r or self.x+self.w<particle.x-particle.r or
                   self.y>particle.y+particle.r or self.y+self.w<particle.y-particle.r)


class Particle:
    def __init__(self, x, y, r, vx, vy):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.cell = grid.cells[grid.get_cell_index(self.x, self.y)]
        self.collided = False

    def update_pos(self):
        self.x += self.vx*dt
        self.y += self.vy*dt
        if not self.r <= self.x <= WIDTH - self.r:
            self.vx *= -1
            self.x = max(self.r,min(self.x, WIDTH-self.r))

        if not self.r <= self.y <= HEIGHT - self.r:
            self.vy *= -1
            self.y = max(self.r,min(self.y, HEIGHT-self.r))

        if not self.cell.contains(self):
            """checks if particle has moved out of the cell it was just in"""
            self.cell.remove_particle(self)
            grid.add_particle(self)

    def draw(self):
        if self.collided:
            pygame.draw.circle(screen, RED, (self.x, self.y), self.r)
            self.collided = False
        else:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), self.r)

    def test_collision(self):
        if not self.collided:
            cells_to_search = grid.get_near(self.x, self.y, self.r) #only gives indexes
            for cell in cells_to_search:
                try: #try used because particles at the bottom will try to check cells outside the grid
                    for particle in grid.cells[cell].particles:
                        if particle != self:
                            if (self.x-particle.x)**2 + (self.y-particle.y)**2 <= (self.r+particle.r)**2:
                                self.collided = True
                                particle.collided = True

                except:
                    pass



grid = Grid(0,0,WIDTH, HEIGHT, divisions)
grid.create_cells()

for i in range(particles):
    x,y = random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)
    vx,vy = random.randint(min_velocity, max_velocity), random.randint(min_velocity, max_velocity)
    radius = random.randint(min_radius, max_radius)
    grid.add_particle(Particle(x, y, radius, vx, vy))



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
    s = time.perf_counter()
    grid.update_grid()

    # update display
    pygame.display.flip()

    #print framerate and avg_collisions to console
    frame_rates.pop(0)
    frame_rates.append(clock.get_fps())
    avg_collisions.pop(0)
    avg_collisions.append(collisions)
    print("\r", flush=True, end="")
    print(f"fps: {sum(frame_rates) / len(frame_rates):.2f} avg_collisions: {sum(avg_collisions) / len(avg_collisions):.0f}", end="", flush=False)
    collisions = 0



