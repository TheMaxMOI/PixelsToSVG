from math import cos as C
from math import floor
from math import radians as r
from math import sin as S


class Rounder:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def __call__(self, x: float, y: float) -> tuple[int, int]:
        newX = floor(self.dx + x)
        newY = floor(self.dy + y)
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
