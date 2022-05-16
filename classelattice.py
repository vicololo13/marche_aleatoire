__author__ = 'Victor'
__Filename = 'LatticeBase'
__Creationdate__ = '10/03/2021' 

import random as rand
import typing as tp
from enum import Enum

class Lattice:

    def __init__(self: 'Lattice', size: int = 0, seed:tp.Any = 0) -> None:
        self.size = size - size%2
        self.seed = seed
        self.rand = rand.Random(self.seed)
        self.setupSeed()

    @property
    def isInfinite(self: 'Lattice') -> bool:
        return self.size == 0

    def setupSeed(self: 'Lattice') -> None:
        rand.seed(None if self.seed == 0 or self.seed is None else self.seed)

    def canGoTo(self: 'Lattice', x: int, y:int) -> bool:
      return False

    def getAvailableDirections(self: 'Lattice', x: int, y:int) -> tp.List['Direction']:
        return []




class Direction(Enum):
    NONE = "NoDirection"
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def rotateRight(self: 'Direction', n:int = 1) -> 'Direction':
        v = self.value + n
        return Direction(v % 4)

    def rotateLeft(self: 'Direction', n:int = 1) -> 'Direction':
        return self.rotateRight(-n)

    @staticmethod
    def generateRandomDirection(d :'Direction' = None, rng : rand.Random = rand) -> 'Direction':
        if(d is None or d is Direction.NONE):
            return Direction(rng.randrange(4))
        if(d.isVertical):
            return Direction(rng.randrange(2) * 2)
        if(d.isHorizontal):
            return  Direction(rng.randrange(2) * 2 + 1)

    @property
    def isHorizontal(self: 'Direction') -> bool:
        return self is Direction.EAST or self is Direction.WEST

    @property
    def isVertical(self: 'Direction') -> bool:
        return self is Direction.NORTH or self is Direction.SOUTH

    @property
    def offset(self: 'Direction') -> int:
        if(self is Direction.NORTH or self is Direction.EAST):
            return 1
        if(self is Direction.SOUTH or self is Direction.WEST):
            return -1
        return 0

    def isSameDirection(self: 'Direction', dire : 'Direction'):
        return (self.isHorizontal and dire.isHorizontal) or (self.isVertical and dire.isVertical)

    #NORTH <-> EAST
    #WEST <-> SOUTH
    def changeDirection(self: 'Direction') -> 'Direction':
        if(self is Direction.NORTH):
            return Direction.EAST
        if(self is Direction.EAST):
            return Direction.NORTH
        if(self is Direction.SOUTH):
            return Direction.WEST
        if(self is Direction.WEST):
            return Direction.SOUTH

    #NORTH <-> SOUTH
    #WEST <-> EAST
    def reverse(self: 'Direction') -> 'Direction':
        if(self is Direction.NORTH):
            return Direction.SOUTH
        if(self is Direction.EAST):
            return Direction.WEST
        if(self is Direction.SOUTH):
            return Direction.NORTH
        if(self is Direction.WEST):
            return Direction.EAST

    def __str__(self : 'Direction') -> str:
        return self.name


class UnOrderedLattice(Lattice):
    def __init__(self: 'UnOrderedLattice', size: int = 0, seed:tp.Any = 0) -> None:
        super().__init__(size, seed)

    def canGoTo(self: 'UnOrderedLattice', x: int, y:int):
        return self.isInfinite or  (-self.size / 2 <= x < self.size / 2 and -self.size / 2 <= y < self.size / 2 )

    def getAvailableDirections(self: 'UnOrderedLattice', x: int, y:int) -> tp.List['Direction']:
        res = []
        for dire in Direction:
            if(dire.isHorizontal):
                if(self.canGoTo(x + dire.offset, y)):
                    res.append(dire)
            if(dire.isVertical):
                if(self.canGoTo(x, y + dire.offset)):
                    res.append(dire)
        return res




class OrderedLattice(Lattice):
    def __init__(self: 'OrderedLattice', size: int = 0, seed:tp.Any = 0, generateFunc : tp.Callable[[Direction, int, rand.Random], Direction] = lambda d, x, r : Direction.generateRandomDirection(d, r)) -> None:
        super().__init__(size, seed)
        self.horizontalStreets = []
        self.verticalStreets = []
        self.generateFunc = generateFunc

        self.generateLattice()


    def generateLattice(self: 'OrderedLattice'):
        for i in range(self.size):
            self.horizontalStreets.append(self.generateFunc(Direction.EAST, int(i - self.size/2), self.rand))
            self.verticalStreets.append(self.generateFunc(Direction.NORTH, int(i - self.size/2), self.rand))


    def canGoTo(self: 'Lattice', x: int, y: int):
        return self.isInfinite or  (-self.size / 2 <= x < self.size / 2 and -self.size / 2 <= y < self.size / 2 )

    def getAvailableDirections(self: 'OrderedLattice', x: int, y:int) -> tp.List['Direction']:
        res = []

        h = self.horizontalStreets[int(y - self.size / 2)]
        if(self.canGoTo(x + h.offset, y)):
             res.append(h)

        v = self.verticalStreets[int(x - self.size / 2)]
        if(self.canGoTo(x, y + v.offset)):
            res.append(v)
        return res






Lattice().canGoTo(0,0)
