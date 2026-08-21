import numpy as np
from scipy.spatial import ConvexHull, QhullError

from lib.svg import Circle, Coloring, Ellipse, Line, Outline, Polygon, Rectangle

from .utils import distToLineVec

EXACT_SEARCH_LIMIT = 2500


def pairwiseDiameterSearch(hullPoints: np.ndarray):
    h = len(hullPoints)
    idx_i, idx_j = np.triu_indices(h, k=1)

    vectors = hullPoints[idx_i] - hullPoints[idx_j]
    norms = np.linalg.norm(vectors, axis=1)

    maxPos = int(np.argmax(norms))
    i, j = idx_i[maxPos], idx_j[maxPos]
    u = np.array([hullPoints[i], hullPoints[j]])
    uVec = vectors[maxPos]

    keep = np.ones(len(vectors), dtype=bool)
    keep[maxPos] = False

    otherVectors = vectors[keep]
    otherNorms = norms[keep]
    idx_i_o = idx_i[keep]
    idx_j_o = idx_j[keep]

    orthogonality = np.abs(otherVectors @ uVec)

    m1 = orthogonality.max() if orthogonality.size else 0
    m2 = otherNorms.max() if otherNorms.size else 0
    if m1:
        orthogonality = orthogonality / m1
    normedOtherNorms = otherNorms / m2 if m2 else otherNorms

    coeff = orthogonality - normedOtherNorms
    otherIdx = int(np.argmin(coeff))

    vi, vj = idx_i_o[otherIdx], idx_j_o[otherIdx]
    v = np.array([hullPoints[vi], hullPoints[vj]])

    return u, v


def degenerateDiameter(points: np.ndarray):
    centered = points - points.mean(axis=0)

    if points.shape[0] < 2:
        z = np.zeros(2)
        return np.array([points[0], points[0]]), np.array([z, z])

    try:
        _, _, vt = np.linalg.svd(centered, full_matrices=False)
        direction = vt[0]
    except np.linalg.LinAlgError:
        direction = np.array([1.0, 0.0])

    proj = centered @ direction
    iMax, iMin = int(np.argmax(proj)), int(np.argmin(proj))
    u = np.array([points[iMax], points[iMin]])

    if vt.shape[0] > 1 and np.linalg.norm(vt[1]) > 0:
        orthDir = vt[1]
    else:
        orthDir = np.array([-direction[1], direction[0]])

    orthProj = centered @ orthDir
    halfSpread = float(np.max(np.abs(orthProj))) if orthProj.size else 0.0
    centroid = points.mean(axis=0)
    v = np.array([centroid + orthDir * halfSpread, centroid - orthDir * halfSpread])

    return u, v


def diameters(points: list[tuple[int, int]] | np.ndarray):
    points = np.asarray(points, dtype=float)

    if len(points) < 3:
        return degenerateDiameter(points)

    if len(points) <= EXACT_SEARCH_LIMIT:
        return pairwiseDiameterSearch(points)

    try:
        hull = ConvexHull(points)
        hullPoints = points[hull.vertices]
    except QhullError:
        return degenerateDiameter(points)

    if len(hullPoints) < 2:
        return degenerateDiameter(points)

    return pairwiseDiameterSearch(hullPoints)


def circleScore(points: np.ndarray, r: float, c: np.ndarray):
    onDisk = ((points - c) ** 2).sum(axis=1) <= r**2
    if np.all(onDisk):
        return np.pi * r**2
    else:
        return np.inf


def ellipseScore(points: np.ndarray, rX: float, rY: float, c: np.ndarray):
    onEllipse = ((points - c) ** 2 / np.array([rX**2, rY**2])).sum(axis=1) <= 1
    if np.all(onEllipse):
        return np.pi * rX * rY
    else:
        return np.inf


def rectangleScore(points: np.ndarray, w: float, h: float, topLeft: np.ndarray):
    onRectangle = np.all(
        (points >= topLeft) & (points <= topLeft + np.array([w, h])), axis=1
    )
    if np.all(onRectangle):
        return w * h
    else:
        return np.inf


def lineScore(points: np.ndarray, a: np.ndarray, b: np.ndarray, width: float):
    dists = distToLineVec(points, a, b)
    if np.all(dists <= width / 2):
        return np.linalg.norm(a - b) * width
    else:
        return np.inf


def fittestShape(points: list[tuple[int, int]] | np.ndarray):
    if len(points) < 2:
        return None
    elif len(points) == 2:
        return Line(*points), 1

    bestArea = np.inf
    bestFit = None

    points = np.asarray(points)

    # Center based shapes
    u, v = diameters(points)
    center = (u.sum(axis=0) + v.sum(axis=0)) / 4
    r_rX, rY = np.linalg.norm(u[0] - u[1]) / 2, np.linalg.norm(v[0] - v[1]) / 2

    score = circleScore(points, r_rX, center)
    if score < bestArea:
        bestFit = Circle(r_rX, center)
        bestArea = score
    score = ellipseScore(points, r_rX, rY, center)
    if score < bestArea:
        bestFit = Ellipse(r_rX, rY, center)
        bestArea = score

    # Rectangle
    topLeft = np.min(points, axis=0)
    bottomRight = np.max(points, axis=0)
    w, h = bottomRight - topLeft

    score = rectangleScore(points, w, h, topLeft)
    if score < bestArea:
        bestFit = Rectangle(h, w, topLeft)
        bestArea = score

    # Line
    width = rY * 2
    score = lineScore(points, u[0], u[1], width)
    if score < bestArea:
        bestFit = Line(u[0], u[1]), width
        bestArea = score

    if bestArea == np.inf:
        return None

    return bestFit


def getfittestShape(points: list[tuple[int, int]] | np.ndarray, color: str):
    res = fittestShape(points)

    if res is None:
        return Polygon(points, Coloring(color))
    elif type(res) == tuple:  # Line
        l, w = res
        for attr in Outline(color, w).use():
            l.addAttribute(attr)

        return l
    elif isinstance(res, (Circle, Ellipse, Rectangle)):
        return res.addAttribute(Coloring(color).use()[0])
