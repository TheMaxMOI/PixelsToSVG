import numpy as np
from scipy import ndimage
from skimage.morphology import dilation

from lib.svg import Circle, Ellipse, Line, Rectangle


def neighbours(i,j, mat: np.ndarray):
    N = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(0, -1),  (0, 1)],
        [(1, -1), (1, 0), (1, 1)],
    ]

    for line in N:
        for dx, dy in line:
            x, y = i + dx, j + dy
            if 0 <= x < mat.shape[0] and 0 <= y < mat.shape[1]:
                yield x, y

def neighbourValues(i, j, mat: np.ndarray):
    h, w = mat.shape[:2]
    hSlice = (max(0, i - 1), min(h, i + 2))
    vSlice = (max(0, j - 1), min(w, j + 2))

    sample = mat[hSlice[0] : hSlice[1], vSlice[0] : vSlice[1]].reshape(
        -1, *mat.shape[2:]
    )

    rowCenter = i - hSlice[0]
    colCenter = j - vSlice[0]
    width = vSlice[1] - vSlice[0]
    center = rowCenter * width + colCenter

    return np.delete(sample, center, axis=0)

def findArea(img, color):
    assert len(img.shape) == 3

    mask = np.all(img == color, axis=2)
    labels, _ = ndimage.label(mask)
    counts = np.bincount(labels.ravel())
    counts[0] = 0

    bigClass = counts.argmax()
    return labels == bigClass

def findOutline(mask):
    mask = mask.astype(bool)
    dilated = dilation(mask)
    return dilated & ~mask

def dfs(i, j, mask, func):
    if not mask[i, j]:
        return

    func(i, j)
    mask[i, j] = False
    for n in neighbours(i, j, mask):
        dfs(n[0], n[1], mask, func)

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


def locatedSmoother(points, begin, end, eps):
    if end - begin < 3:
        return [points[begin], points[end - 1]]

    distMax = 0
    idxMax = 0

    for i in range(begin + 1, end - 1):
        dist = distToLine(points[i], points[begin], points[end - 1])
        if dist > distMax:
            distMax = dist
            idxMax = i

    if distMax > eps:
        left = locatedSmoother(points, begin, idxMax + 1, eps)
        right = locatedSmoother(points, idxMax, end, eps)
        return left[:-1] + right
    else:
        return [points[begin], points[end - 1]]


def smoothPolygon(points, eps=1.0):  # RDP Ramer-Douglas-Peucker
    return locatedSmoother(points, 0, len(points), eps)

def findPolygon(mask):
    points = []
    mask = mask.copy()
    collect = lambda x, y: points.append((x, y))

    i, j = 0, 0
    while i < mask.shape[0] and j < mask.shape[1]:
        if mask[i, j]:
            dfs(i, j, mask, collect)
            break

        j += 1
        if j == mask.shape[1]:
            j = 0
            i += 1

    return smoothPolygon(points) # because most of the time an edge is described by too many points.

def findfittestShape(points):
    pass # TODO -> Making everything a polygon is maybe not the fittest...