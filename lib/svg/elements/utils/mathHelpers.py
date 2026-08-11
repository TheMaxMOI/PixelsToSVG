from math import cos as C
from math import floor
from math import radians as r
from math import sin as S


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
    return S(r(angle))


def cos(angle):
    return C(r(angle))


def norm2(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def dist2(a, b):
    return norm2((a[0] - b[0], a[1] - b[1]))


def normInf(v):
    return max(abs(v[0]), abs(v[1]))


def distInf(a, b):
    return normInf((a[0] - b[0], a[1] - b[1]))
