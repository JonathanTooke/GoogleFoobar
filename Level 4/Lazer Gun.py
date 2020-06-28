from collections import namedtuple, deque
from math import sqrt, ceil
from fractions import gcd

Coords = namedtuple('Coords', ['x', 'y']) #using a named tuple for readability

def solution(dimensions, your_position, guard_position, distance):
    """
    Use a mirroring approach where reflections of the original 'battle field'
    are iteratively created until the reflections exceed the range of the lazer 
    """
    #1. Initialize variables
    origin, dims, your_pos, guard_pos, grid_dims = initialize_variables(dimensions, your_position, guard_position, distance)

    #2. Create the grid of mirrored landscapes with dims equal to (1 + grid_dims.x*2, 1 + grid_dims.y*2)
    x_landscape = deque()
    x_landscape.append(Landscape(Person(False, your_pos, your_pos), Person(True, guard_pos, your_pos), origin, dims))

    for i in range(grid_dims.x): 
        ls = x_landscape[-1].reflect('east', original_dims=dims, shooter=your_pos)
        x_landscape.append(ls)

    for i in range(grid_dims.x):
        ls = x_landscape[0].reflect('west', original_dims=dims, shooter=your_pos)
        x_landscape.appendleft(ls)
    
    grid = deque()
    grid.append(list(x_landscape))

    for i in range(grid_dims.y):
        grid.append(map(lambda ls: ls.reflect('north', original_dims=dims, shooter=your_pos), grid[-1]))
    
    for i in range(grid_dims.y):
        grid.appendleft(map(lambda ls: ls.reflect('south', original_dims=dims, shooter=your_pos), grid[0]))

    grid = [landscape for x_landscape in list(grid) for landscape in x_landscape] #flatten to 1D list

    #3. Extract the People from the landscapes
    people = [landscape.guard for landscape in grid] + [landscape.you for landscape in grid]

    #4. Filter People by distance and sort by distance
    people = filter(lambda p: p.in_range(distance), people)
    people.sort(key=lambda p: p.dist)

    #5. Count valid shots
    shots = 0
    invalid_bearings = set()
    for person in people:
        if person.is_enemy and person.bear not in invalid_bearings:
            shots += 1
        invalid_bearings.add(person.bear)

    return shots

def initialize_variables(dimensions, your_position, guard_position, distance):
    """Initialize the base variables"""
    origin = Coords(0,0)
    dims = Coords(dimensions[0], dimensions[1])
    your_pos = Coords(your_position[0], your_position[1])
    guard_pos = Coords(guard_position[0], guard_position[1]) 
    grid = Coords(int(ceil(float(distance)/dims.x)), int(ceil(float(distance)/dims.y))) 

    return origin, dims, your_pos, guard_pos, grid

class Person:
    """Class used to represent the location of a guard or a shooter in any mirrored reflection"""

    def __init__(self, is_enemy, position, shooter):
        """
        :param enemy: bool where true is a guard and false is you
        :param position: Position (named tuple) with x and y values relative to origin
        :param shooter: Position (named tuple) with x and y values of you (the shooter) in the original block
        """
        self.is_enemy = is_enemy
        self.pos = position
        self.dist = self.distance(position, shooter)
        self.bear = self.bearing(position, shooter)

    def distance(self, pos, shooter):
        """Calculates the distance between this person and the original shooter"""
        return sqrt((pos.x - shooter.x)** 2 + (pos.y - shooter.y)**2)
    
    def bearing(self, pos, shooter):
        """Calculate the vector bearing from the shooter to this person"""
        x_delta = shooter.x - pos.x
        y_delta = shooter.y - pos.y
        div = abs(gcd(x_delta, y_delta))
        if div == 0:
            bearing = (x_delta, y_delta)
        else:
            bearing = (x_delta/div, y_delta/div)

        return bearing 
        
    def in_range(self, firing_range):
        """Checks whether this person falls within the firing range"""
        return self.dist <= firing_range

class Landscape:
    """Class used to represent a landscape after a given reflection"""
    def __init__(self, you, guard, start_dims, end_dims):
        """
        :param you: Person object storing information about your reflection in the landscape
        :param guard: Person object storing information about the guard's reflection in the landscape
        :param start_dims: Coords tuple representing the bottom left x and y values
        :param end_dims: Coords tuple representing the top right x and y values
        """
        self.you = you
        self.guard = guard
        self.start_dims = start_dims
        self.end_dims = end_dims

    def reflect(self, direction, original_dims, shooter):
        """Reflect a landscape in the specified direction"""
        if direction == 'west':
            return Landscape(
                Person(False, Coords(2*self.start_dims.x - self.you.pos.x, self.you.pos.y), shooter),
                Person(True, Coords(2*self.start_dims.x - self.guard.pos.x, self.guard.pos.y), shooter),
                Coords(self.start_dims.x - original_dims.x, self.start_dims.y),
                Coords(self.end_dims.x - original_dims.x, self.end_dims.y)
            )
        elif direction == 'east':
            return Landscape(
                Person(False, Coords(2*self.end_dims.x - self.you.pos.x, self.you.pos.y), shooter),
                Person(True, Coords(2*self.end_dims.x - self.guard.pos.x, self.guard.pos.y), shooter),
                Coords(self.start_dims.x + original_dims.x, self.start_dims.y),
                Coords(self.end_dims.x + original_dims.x, self.end_dims.y)
            )
        elif direction == 'north':
            return Landscape(
                Person(False, Coords(self.you.pos.x, 2*self.end_dims.y - self.you.pos.y), shooter),
                Person(True, Coords(self.guard.pos.x, 2*self.end_dims.y - self.guard.pos.y), shooter),
                Coords(self.start_dims.x, self.start_dims.y + original_dims.y),
                Coords(self.end_dims.x, self.end_dims.y + original_dims.y)
            )
        elif direction == 'south':
            return Landscape(
                Person(False, Coords(self.you.pos.x, 2*self.start_dims.y - self.you.pos.y), shooter),
                Person(True, Coords(self.guard.pos.x, 2*self.start_dims.y - self.guard.pos.y), shooter),
                Coords(self.start_dims.x, self.start_dims.y - original_dims.y),
                Coords(self.end_dims.x, self.end_dims.y - original_dims.y)
            )
        else:
            raise Exception('Invalid reflection direction {}, expected direction in [north, east, south, west]'.format(direction))