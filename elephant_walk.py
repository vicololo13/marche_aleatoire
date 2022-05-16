__author__ = 'Victor'
__Filename = 'ElephantWalk'
__Creationdate__ = '18/02/2021'

import random as rand;
import matplotlib.pyplot as plt


def proba(proba):
    return 1 if rand.random() < proba else -1 ;


class ElephantWalk1D:

    def __init__(self, p, q):
        self.p = p;
        self.q = q;
        self.listX = []


    def walk(self, stepNumber):
        x = 0;
        self.listX = [x];

        listSigma = [proba(self.q)];
        x += listSigma[0]
        self.listX.append(x)

        for i in range(stepNumber):
            t = rand.randrange(len(listSigma))
            sigma = proba(self.p) * listSigma[t];
            x += sigma
            self.listX.append(x)
            listSigma.append(sigma)


    def draw(self):
        plt.plot(range(len(self.listX)), self.listX)
        plt.grid()
        plt.show()


def sign(a):
    return 1 if a > 0 else 0 if a == 0 else -1;


changeDirection = {1:2, 2:1, -1:-2, -2:-1}

class ElephantWalk2D:

    def __init__(self, p, q, r, s):
        self.p = p;
        self.q = q;
        self.r = r;
        self.s = s;
        self.listX = []
        self.listY = []



    def walk(self, stepNumber):
        x = 0;
        y = 0;
        self.listX = [x];
        self.listY = [y];

        listSigma = [proba(self.q) * (proba(self.s) + 3 )/2];           # signe pour le sens, nombre pour la direction
                                                                        # 1/-1 selon x, 2/-2 pour y
        if listSigma[0] % 2 == 1:
            x += sign(listSigma[0])
        else:
            y += sign(listSigma[0])

        self.listX.append(x)
        self.listY.append(y)

        for i in range(stepNumber):
            sigmaChosen = listSigma[rand.randrange(len(listSigma))]

            # sigma = proba(self.p) * (changeDirection[sigmaChosen] if proba(self.r) == -1 else sigmaChosen);

            if sigma % 2 == 1:
                x += sign(sigma)
            else:
                y += sign(sigma)

            self.listX.append(x)
            self.listY.append(y)

            listSigma.append(sigma)


    def draw(self):
        plt.plot(self.listX, self.listY)
        plt.grid()
        plt.show()


#elephant = ElephantWalk1D(0, 0.5)
elephant = ElephantWalk2D(0.5, 0.5, 0.5, 0.5)
elephant.walk(500)
elephant.draw()
