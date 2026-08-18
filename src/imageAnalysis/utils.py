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