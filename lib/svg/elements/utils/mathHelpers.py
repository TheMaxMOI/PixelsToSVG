from math import cos as COS
from math import floor, pi, sqrt
from math import log as ln
from math import radians as rad
from math import sin as SIN
from math import tan as TAN
from random import randint as RANDN
from random import random as RAND


def my_round(x, p):
    return round(floor(x * 10**p) / 10**p, ndigits=3)


class Rounder:
    def __init__(self, precision=0):
        self.dx = 0
        self.dy = 0
        self.precision = precision

    def __call__(self, x: float, y: float) -> tuple[int, int]:
        newX = my_round(self.dx + x, self.precision)
        newY = my_round(self.dy + y, self.precision)
        self.dx += x - newX
        self.dy += y - newY

        return newX, newY


def sin(angle):
    return SIN(rad(angle))


def cos(angle):
    return COS(rad(angle))


def norm2(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def dist2(a, b):
    return norm2((a[0] - b[0], a[1] - b[1]))


def normInf(v):
    return max(abs(v[0]), abs(v[1]))


def distInf(a, b):
    return normInf((a[0] - b[0], a[1] - b[1]))


def randint(a, b=None, len=1):
    if b is None:
        b = a
        a = 0

    if len > 1:
        return (RANDN(a, b) for _ in range(len))
    else:
        return RANDN(a, b)


a = 2 * pi / 3
I = (3 / pi) * ln(2 + sqrt(3)) - 0.96
K = 1 / I


def f(x):  # distribution
    return K * (1 / (a * (x - 0.5)) - 0.96)


def F(x):  # repartition
    u = a * (x - 0.5)
    return K * ((1 / a) * (ln(1 / COS(u) + TAN(u)) + ln(2 + sqrt(3))) - 0.96 * x)


def random():
    u = RAND()
    x = u
    eps = 1e-9
    for _ in range(6):
        if abs(x - 0.5) < eps:
            x += eps

        fx = f(x)
        if fx != 0:
            x -= (F(x) - u) / fx

        x = min(max(x, eps), 1 - eps)
    return x
