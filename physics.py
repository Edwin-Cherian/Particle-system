from __future__ import annotations
from pygame import Vector2, Rect, Surface, Color, draw
from typing import Dict, List, Union, Tuple
from dataclasses import dataclass
from abc import ABC
import math


class Utility:
    @staticmethod
    def clamp(value: Union[int, float], mini: Union[int, float], maxi: Union[int, float]) -> Union[int, float]:
        """Return a clamped value."""
        return max(mini, min(value, maxi))


@dataclass
class Particle:
    """Particle data class to store position, velocity, radius, mass."""
    id: int
    pos: Vector2
    prev_pos: Vector2
    vel: Vector2
    radius: float
    mass: float

    count: int = 0

    def __init__(self, x: float, y: float, vx: float, vy: float, radius: float, mass: float = 1) -> None:
        self.id = Particle.count
        Particle.count += 1
        self.pos = Vector2(x, y)
        self.prev_pos = self.pos
        self.vel = Vector2(vx, vy)
        self.radius = radius
        self.mass = mass
        self.collided = False

    def __hash__(self) -> int:
        """Calculate unique hash code."""
        return self.id


class ParticleManager(ABC):
    """Abstract class for square particle storage systems."""
    def add_child(self, child: Particle) -> bool:
        """Add an object to the grid."""
        pass

    def remove_child(self, child: Particle) -> bool:
        """Remove an object from the grid."""
        pass

    def get_children(self) -> List[Particle]:
        """Return a list of all the particles in the manager."""
        pass

    def get_near(self, child: Particle) -> List[Particle]:
        """Get possible collisions (particles near to child)."""
        pass

    def update(self) -> int:
        """Return the number of particles moved between cells after updating."""
        pass

    def is_in_bounds_x(self, particle: Particle) -> bool:
        """Return whether the particle's x is within the bounds."""
        pass

    def is_in_bounds_y(self, particle: Particle) -> bool:
        """Return whether the particle's y is within the bounds."""
        pass


# Ideal grid size is probably just bigger than the smallest particle diameter
class FixedGrid(ParticleManager):
    """A square fixed grid to store particles."""
    size: float
    divs: int
    cell_size: float
    cells: List[Union[None, Particle]]
    children: Dict[Particle, Union[Particle, None]]

    def __init__(self, size: float, divs: int = 50) -> None:
        self.size = size
        self.divs = divs
        self.cell_size = size / divs
        self.cells = [None for _ in range(divs ** 2)]  # Each cell stores a reference to the first child
        self.children = {}  # Each child stores a reference to the next child in the cell

    @classmethod
    def from_cell_size(cls, size: float, cell_size: float):
        return FixedGrid(size, math.floor(size / cell_size))

    def is_valid(self, x: float, y: float) -> bool:
        """Return whether coords lie within the grid."""
        return 0 <= x < self.divs and 0 <= y < self.divs

    def get_cell_xy(self, pos: Vector2) -> Tuple[int, int]:
        """Return the x and y of the cell a particle lies in."""
        return math.floor(pos.x / self.cell_size), math.floor(pos.y / self.cell_size)

    def ci(self, x: int, y: int) -> int:
        """Return the cell index of the cell at x, y."""
        return y * self.divs + x

    def get_children(self) -> List[Particle]:
        return list(self.children.keys())

    def get_cell_children(self, x: int, y: int) -> List[Particle]:
        """Return a list of children contained within the cell."""
        children = []
        # Check if the cell has any children
        if (curr_child := self.cells[self.ci(x, y)]) is None:
            return children
        # If so, traverse the children, adding them to the array
        children.append(curr_child)
        while (curr_child := self.children[curr_child]) is not None:
            children.append(curr_child)
        return children

    def add_child_to_cell(self, child: Particle) -> bool:
        """Add a particle to a cell."""
        x, y = self.get_cell_xy(child.pos)
        if not self.is_valid(x, y):
            return False
        # if the cell is None, then point the cell to the new child
        if (curr_child := self.cells[self.ci(x, y)]) is None:
            self.cells[self.ci(x, y)] = child
            return True
        # Otherwise traverse to the last element that is None, and replace it with a reference to the new child
        while self.children[curr_child] is not None:
            curr_child = self.children[curr_child]
        self.children[curr_child] = child
        return True

    def add_child(self, child: Particle) -> bool:
        self.children[child] = None
        return self.add_child_to_cell(child)

    def remove_child_from_cell(self, child: Particle, use_prev: bool = False) -> bool:
        """Remove a particle from a cell."""
        if child not in self.children.keys():
            return False
        # if the cell points to the child, just point the cell to the child's pointer
        x, y = self.get_cell_xy(child.prev_pos if use_prev else child.pos)
        if (curr_child := self.cells[self.ci(x, y)]) == child:
            self.cells[self.ci(x, y)] = self.children[child]
            self.children[child] = None
            return True
        # otherwise traverse until you find the pointer to the child, and replace that with the child's pointer
        while self.children[curr_child] != child:
            curr_child = self.children[curr_child]
        self.children[curr_child] = self.children[child]
        self.children[child] = None
        return True

    def remove_child(self, child: Particle) -> bool:
        result = self.remove_child_from_cell(child)
        self.children.pop(child, None)
        return result

    def get_near(self, child: Particle) -> List[Particle]:
        # Approach 1: Check all possible cells - Less efficient in testing
        # cx, cy = self.get_cell_xy(child.pos)
        # cells_radius = math.ceil(child.radius / self.cell_size)
        # min_cx, min_cy = cx - cells_radius, cy - cells_radius
        # max_cx, max_cy = cx + cells_radius, cy + cells_radius
        # Approach 2: Check all possible cells for current particle location - More efficient in testing
        min_x, min_y = child.pos.x - child.radius, child.pos.y - child.radius
        max_x, max_y = child.pos.x + child.radius, child.pos.y + child.radius
        min_cx, min_cy = math.floor(min_x / self.cell_size), math.floor(min_y / self.cell_size)
        max_cx, max_cy = math.floor(max_x / self.cell_size), math.floor(max_y / self.cell_size)
        # for each cell that could contain a collision, get all the particles and add them to the return list
        # note the +1 to the maximum, as we want to include this value, which we normally exclude in range()
        children = []
        for y in range(Utility.clamp(min_cy, 0, self.divs), Utility.clamp(max_cy + 1, 0, self.divs)):
            for x in range(Utility.clamp(min_cx, 0, self.divs), Utility.clamp(max_cx + 1, 0, self.divs)):
                children += self.get_cell_children(x, y)
        return children

    def update(self) -> int:
        count = 0
        # for each cell, if the child is not in the right cell, move it to the right cell
        for child in self.children:
            x, y = self.get_cell_xy(child.pos)
            if child not in self.get_cell_children(x, y):
                self.remove_child_from_cell(child, True)
                self.add_child_to_cell(child)
                count += 1
        return count

    def is_in_bounds_x(self, particle: Particle) -> bool:
        return particle.pos.x - particle.radius >= 0 and particle.pos.x + particle.radius <= self.size

    def is_in_bounds_y(self, particle: Particle) -> bool:
        return particle.pos.y - particle.radius >= 0 and particle.pos.y + particle.radius <= self.size


class QuadTree(ParticleManager):
    """Inefficient quad tree based on Edwin's code."""
    rect: Rect
    children: List[Particle]
    capacity: int
    divided: bool
    nw: Union[None, QuadTree]
    ne: Union[None, QuadTree]
    sw: Union[None, QuadTree]
    se: Union[None, QuadTree]

    def __init__(self, rect: Rect, capacity: int = 1) -> None:
        self.rect = rect
        self.children = []
        self.capacity = capacity
        self.divided = False
        self.nw = self.ne = self.sw = self.se = None

    def subdivide(self) -> None:
        self.divided = True
        half_w = self.rect.width / 2
        half_h = self.rect.height / 2
        self.nw = QuadTree(Rect(self.rect.x, self.rect.y, half_w, half_h), self.capacity)
        self.ne = QuadTree(Rect(self.rect.x + half_w, self.rect.y, half_w, half_h), self.capacity)
        self.sw = QuadTree(Rect(self.rect.x, self.rect.y + half_h, half_w, half_h), self.capacity)
        self.se = QuadTree(Rect(self.rect.x + half_w, self.rect.y + half_h, half_w, half_h), self.capacity)

    def add_child(self, child: Particle) -> bool:
        if self.is_in_bounds_x(child) and self.is_in_bounds_y(child):
            if len(self.children) > self.capacity:
                self.children.append(child)
            else:
                if not self.divided:
                    self.subdivide()
                self.nw.add_child(child)
                self.ne.add_child(child)
                self.sw.add_child(child)
                self.se.add_child(child)
            return True
        return False

    def remove_child(self, child: Particle) -> bool:
        pass

    def get_children(self) -> List[Particle]:
        pass

    def get_near(self, child: Particle) -> List[Particle]:
        pass

    def update(self) -> int:
        # reconstruct tree :(
        pass

    def is_in_bounds_x(self, particle: Particle) -> bool:
        return self.rect.x < particle.pos.x <= self.rect.x + self.rect.width

    def is_in_bounds_y(self, particle: Particle) -> bool:
        return self.rect.y < particle.pos.y <= self.rect.y + self.rect.height


# TODO Handle > 2 particles colliding
class ParticleEngine:
    """Class to handle collisions and movement of particles."""
    rect: Rect
    manager: ParticleManager

    def __init__(self, size: float, manager: ParticleManager) -> None:
        self.size = size
        self.manager = manager

    def update_particle(self, particle: Particle, delta_time: float) -> None:
        """Update the position and velocity of a particle, without handling collisions."""
        particle.prev_pos = Vector2(particle.pos)
        particle.pos += particle.vel * delta_time
        if not self.manager.is_in_bounds_x(particle):
            particle.vel.x *= -1
            particle.pos.x = Utility.clamp(particle.pos.x, particle.radius, self.size - particle.radius)
        if not self.manager.is_in_bounds_y(particle):
            particle.vel.y *= -1
            particle.pos.y = Utility.clamp(particle.pos.y, particle.radius, self.size - particle.radius)

    @staticmethod
    def test_collide(a: Particle, b: Particle) -> bool:
        """Return whether two particles are colliding."""
        return (b.pos - a.pos).length_squared() < ((a.radius + b.radius) ** 2)

    @staticmethod
    def collide(a: Particle, b: Particle) -> None:
        """Calculate the new position and velocity of two colliding particles."""
        a.collided = True
        b.collided = True

    @staticmethod
    def draw_particle(screen: Surface, particle: Particle, default_col: Color, collide_col: Color) -> None:
        """Draw the particle to the screen, accounting for whether it is colliding or not."""
        draw.circle(screen, collide_col if particle.collided else default_col, particle.pos, particle.radius)
        if particle.collided:
            particle.collided = False

    def step(self, delta_time: float) -> int:
        """Step through the simulation and return the number of collisions."""
        # TODO don't check other object when collided
        count = 0
        for particle in self.manager.get_children():
            self.update_particle(particle, delta_time)
        self.manager.update()
        for particle in self.manager.get_children():
            possible_collisions = self.manager.get_near(particle)
            for possible_collision in possible_collisions:
                if possible_collision != particle and self.test_collide(particle, possible_collision):
                    self.collide(particle, possible_collision)
                    count += 1
        return count
