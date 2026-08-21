import numpy as np
from scipy import ndimage
from skimage import measure
from skimage.morphology import dilation

from .utils import distToLineVec


def neighbours(i: int, j: int, mat: np.ndarray):
    N = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(0, -1), (0, 1)],
        [(1, -1), (1, 0), (1, 1)],
    ]

    for line in N:
        for dx, dy in line:
            x, y = i + dx, j + dy
            if 0 <= x < mat.shape[0] and 0 <= y < mat.shape[1]:
                yield x, y


def neighbourValues(i: int, j: int, mat: np.ndarray):
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


def findArea(img, color: np.ndarray):
    assert len(img.shape) == 3

    mask = np.all(img == color, axis=2)
    labels, _ = ndimage.label(mask)
    counts = np.bincount(labels.ravel())
    counts[0] = 0

    bigClass = counts.argmax()
    return labels == bigClass


def findOutline(mask: np.ndarray):
    mask = mask.astype(bool)
    dilated = dilation(mask)
    return dilated & ~mask


def findPolygon(mask: np.ndarray):
    mask = np.asarray(mask, dtype=bool)

    if not mask.any():
        return []

    contours = measure.find_contours(mask.astype(np.uint8), level=0.5)
    if not contours:
        return []

    largest = max(contours, key=len)
    return [(round(r), round(c)) for r, c in largest]


def smoothPolygon(points: list, eps: float = 1.0):  # Ramer-Douglas-Peucker
    n = len(points)
    if n < 3:
        return list(points)

    pts = np.asarray(points, dtype=float)
    keepIdx = {0, n - 1}

    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        if hi - lo < 2:
            continue

        a, b = pts[lo], pts[hi]
        segment = pts[lo + 1 : hi]

        dists = distToLineVec(segment, a, b)
        localMax = int(np.argmax(dists))
        distMax = dists[localMax]
        idxMax = lo + 1 + localMax

        if distMax > eps:
            keepIdx.add(idxMax)
            stack.append((lo, idxMax))
            stack.append((idxMax, hi))

    return [points[i] for i in sorted(keepIdx)]
