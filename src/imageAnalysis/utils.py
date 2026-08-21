import numpy as np


def distToLine(p, a, b):
    p = np.array(p, dtype=float)
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if np.all(a == b):
        return np.linalg.norm(p - a)

    v = b - a
    t = np.dot(p - a, v) / np.dot(v, v)
    proj = a + t * v

    return np.linalg.norm(p - proj)


def distToLineVec(points, a, b):
    points = np.atleast_2d(np.asarray(points, dtype=float))
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    v = b - a
    vNorm2 = np.dot(v, v)

    if vNorm2 == 0:
        return np.linalg.norm(points - a, axis=1)

    t = (points - a) @ v / vNorm2
    proj = a + t[:, None] * v

    return np.linalg.norm(points - proj, axis=1)
