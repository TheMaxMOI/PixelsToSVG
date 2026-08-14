import numpy as np
from scipy import ndimage
from skimage.morphology import dilation


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


def findPolygon(mask):
    points = []
    mask = mask.copy()
    i, j = 0, 0
    while i < mask.shape[0] and j < mask.shape[1]:
        if mask[i, j]:
            dfs(i, j, mask, lambda x, y: points.append((x, y)))
            break
        j += 1
        if j == mask.shape[1]:
            j = 0
            i += 1
    return np.array(points)
