__author__ = 'Victor'
__Filename = 'Walk'
__Creationdate__ = '18/02/2021'

import sys
import random as rand
import matplotlib.pyplot as plt
import typing as tp
from Serious.Lattices import Lattice, OrderedLattice
from Serious.Lattices import Direction
from Serious.Lattices import UnOrderedLattice

# def proba(proba, rng: rand.Random = rand):
#     return 1 if rng.random() < proba else -1

def probab(proba, rng: rand.Random = rand):
    return rng.random() < proba

class ElephantWalk1D:

    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.listX = []


    def walk(self, stepNumber):
        x = 0
        self.listX = [x]

        listSigma = [proba(self.q)]
        x += listSigma[0]
        self.listX.append(x)

        for i in range(stepNumber):
            t = rand.randrange(len(listSigma))
            sigma = proba(self.p) * listSigma[t]
            x += sigma
            self.listX.append(x)
            listSigma.append(sigma)


    def draw(self):
        plt.plot(range(len(self.listX)), self.listX)
        plt.grid()
        plt.show()


def sign(a):
    return 1 if a > 0 else 0 if a == 0 else -1


changeDirection = {1:2, 2:1, -1:-2, -2:-1}


class Walk:
    def __init__(self:'Walk', lattice: Lattice, seed: tp.Any):
        self.seed = seed
        self.rand = rand.Random(self.seed)

        self.lattice = lattice

    def walk(self: 'Walk', stepNumber: int) -> None:
        return

    def draw(self:'Walk') -> None:
        return


class ElephantWalk2D(Walk):

    # p la probabilité de d'aller dans le même sens
    # q la probabilité de départ de p
    # r la probabilité d'aller dans la même direction

    def __init__(self: 'ElephantWalk2D', p: float, q: float, r: float, s: float, lattice: Lattice, seed: tp.Any):
        super().__init__(lattice, seed)
        self.p = p
        self.q = q
        self.r = r
        self.s = s
        self.listX = []
        self.listY = []



    def walk(self: 'ElephantWalk2D', stepNumber: int) -> None:
        x = 0
        y = 0

        self.listX = [x]
        self.listY = [y]

        #listSigma = [proba(self.q) * (proba(self.s) + 3 )/2]           # signe pour le sens, nombre pour la direction
                                                                        # 1/-1 selon x, 2/-2 pour y
        direc = Direction.NORTH
        if(probab(self.s, self.rand)):
            direc = direc.changeDirection()
        if(probab(self.q, self.rand)):
            direc = direc.reverse()

        listeAvailableDirections = self.lattice.getAvailableDirections(0, 0)

        if(not direc in listeAvailableDirections):
            d = direc
            for direcF in listeAvailableDirections:
                if direc.isSameDirection(direcF):
                    d = direcF
            if(direc is d):
                direc = listeAvailableDirections[0]
            else:
                direc = d

        listSigma = [direc]

        if direc.isHorizontal:
            x += direc.offset
        else:
            y += direc.offset

        self.listX.append(x)
        self.listY.append(y)

        for i in range(stepNumber):
            sigmaChosen = listSigma[rand.randrange(len(listSigma))]

            #sigma = proba(self.p) * (changeDirection[sigmaChosen] if proba(self.r) == -1 else sigmaChosen);

            if(probab(self.p, self.rand)):
                sigmaChosen = sigmaChosen.reverse()
            if(probab(self.r, self.rand)):
                sigmaChosen = sigmaChosen.changeDirection()

            listeAvailableDirections = self.lattice.getAvailableDirections(x, y)

            if(not sigmaChosen in listeAvailableDirections):
                d = sigmaChosen
                for direcF in listeAvailableDirections:
                    if sigmaChosen.isSameDirection(direcF):
                        d = direcF
                if(sigmaChosen is d):
                    sigmaChosen = listeAvailableDirections[0]
                else:
                    sigmaChosen = d


            if sigmaChosen.isHorizontal:
                x += sigmaChosen.offset
            else:
                y += sigmaChosen.offset

            self.listX.append(x)
            self.listY.append(y)

            print("x : " + str(x) + ",   y : " + str(y) + ",   direction : " + str(sigmaChosen))

            listSigma.append(sigmaChosen)


    def draw(self:'ElephantWalk2D') -> None:
        plt.plot(self.listX, self.listY)
        plt.grid()
        plt.show()


class RandomWalk(Walk):

    def __init__(self: 'RandomWalk', p:float, q:float, r:float, s:float, lattice:Lattice, seed: tp.Any):
        super().__init__(lattice, seed)
        self.p = p
        self.q = q
        self.r = r
        self.s = s

        self.listX = []
        self.listY = []


    def walk(self: 'RandomWalk', stepNumber: int) -> None:

        x = 0
        y = 0

        self.listX = [x]
        self.listY = [y]

        for i in range(stepNumber):
            direc = Direction.NORTH
            if (probab(self.s, self.rand)):
                direc = direc.changeDirection()
            if (probab(self.q, self.rand)):
                direc = direc.reverse()

            listeAvailableDirections = self.lattice.getAvailableDirections(x, y)

            if (not direc in listeAvailableDirections):
                d = direc
                for direcF in listeAvailableDirections:
                    if direc.isSameDirection(direcF):
                        d = direcF
                if (direc is d):
                    direc = listeAvailableDirections[0]
                else:
                    direc = d
            
            if(direc.isHorizontal):
                x += direc.offset
            if(direc.isVertical):
                y += direc.offset

            self.listX.append(x)
            self.listY.append(y)


    def draw(self:'RandomWalk') -> None:
        plt.plot(self.listX, self.listY)
        plt.grid()
        plt.show()


class RandomWalkWithRandomJumps(Walk):
    def __init__(self: 'RandomWalkWithRandomJumps', p: float, q: float, r: float, s: float, lattice: Lattice, seed: tp.Any, pi: tp.Callable[[int, int], float] = lambda x,y : 0.5):
        super().__init__(lattice, seed)
        self.p = p
        self.q = q
        self.r = r
        self.s = s

        self.listX = []
        self.listY = []

    def walk(self: 'RandomWalkWithRandomJumps', stepNumber: int) -> None:

        x = 0
        y = 0

        self.listX = [x]
        self.listY = [y]

        for i in range(stepNumber):
            direc = Direction.NORTH
            if (probab(self.s, self.rand)):
                direc = direc.changeDirection()
            if (probab(self.q, self.rand)):
                direc = direc.reverse()

            listeAvailableDirections = self.lattice.getAvailableDirections(x, y)

            if (not direc in listeAvailableDirections):
                d = direc
                for direcF in listeAvailableDirections:
                    if direc.isSameDirection(direcF):
                        d = direcF
                if (direc is d):
                    direc = listeAvailableDirections[0]
                else:
                    direc = d

            if (direc.isHorizontal):
                x += direc.offset
            if (direc.isVertical):
                y += direc.offset

            self.listX.append(x)
            self.listY.append(y)

    def draw(self: 'RandomWalkWithRandomJumps') -> None:
        plt.plot(self.listX, self.listY)
        plt.grid()
        plt.show()


class RandomAlternativeWalk(Walk):
    def __init__(self: 'RandomAlternativeWalk', p: float, q: float, r: float, s: float, lattice: Lattice, seed: tp.Any, probabilityFunc : tp.Callable[[int, int], float] = lambda x, n : 1 if n == 0 else 1/n):
        super().__init__(lattice, seed)
        self.p = p
        self.q = q
        self.r = r
        self.s = s

        self.listX = []
        self.listY = []

        self.probabilityFunc = probabilityFunc

    def walk(self: 'RandomAlternativeWalk', stepNumber: int) -> None:

        x = 0
        y = 0

        self.listX = [x]
        self.listY = [y]

        for i in range(stepNumber):
            direc = Direction.NORTH
            if (probab(self.s, self.rand)):
                direc = direc.changeDirection()
            if (probab(self.q, self.rand)):
                direc = direc.reverse()

            listeAvailableDirections = self.lattice.getAvailableDirections(x, y)
            if(len(listeAvailableDirections) == 0):
                break
            if (not direc in listeAvailableDirections):
                d = direc
                for direcF in listeAvailableDirections:
                    if direc.isSameDirection(direcF):
                        d = direcF
                if (direc is d):
                    direc = listeAvailableDirections[0]
                else:
                    direc = d


            distanceToWalk = 1
            rng = self.rand.random()
            rngTotal = 0
            for j in range(1, i):
                nextRngTotal = rngTotal + self.probabilityFunc(j, i);
                if(rngTotal <= rng < nextRngTotal):
                    distanceToWalk = j
                    break;
                rngTotal = nextRngTotal


            if (direc.isHorizontal):
                if(not self.lattice.isInfinite):
                    distanceToWalk = min(distanceToWalk, self.lattice.size / 2 - direc.offset * x)
                x += direc.offset * distanceToWalk
            if (direc.isVertical):
                if (not self.lattice.isInfinite):
                    distanceToWalk = min(distanceToWalk, self.lattice.size / 2 - direc.offset * y)
                y += direc.offset * distanceToWalk

            print(distanceToWalk)

            self.listX.append(x)
            self.listY.append(y)


    def draw(self: 'RandomAlternativeWalk') -> None:
        plt.plot(self.listX, self.listY)
        plt.grid()
        plt.show()


def sudEast(d: 'Direction', x: int, rng: rand.Random) -> 'Direction':
    if(d.isVertical):
        return Direction.SOUTH
    if(d.isHorizontal):
        return Direction.EAST

def nordOuest(d: 'Direction', x: int, rng: rand.Random) -> 'Direction':
    if(d.isVertical):
        return Direction.NORTH if -100<x<100 else Direction.SOUTH
    if(d.isHorizontal):
        return Direction.WEST

#elephant = ElephantWalk1D(0, 0.5)
seedChosen = rand.randrange(sys.maxsize)
#seedChosen = 1259557030
#seedChosen = 1816265777
#seedChosen = 43316513
#RandomWalk :
#seedChosen = 836852345
elephant = RandomAlternativeWalk(0.5, 0.5, 0.5, 0.5, OrderedLattice(500, seedChosen), seedChosen)
elephant.walk(100)
print("Seed : " + str(seedChosen))
elephant.draw()
