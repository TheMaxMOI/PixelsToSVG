import numpy as np

from lib.svg import Circle, Coloring, Ellipse, Line, Outline, Polygon, Rectangle

from .utils import distToLine


def diameters(points: list[tuple[int, int]] | np.ndarray):
    points = np.array(points)

    vectors = []
    refs = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            vectors.append(points[i] - points[j])
            refs.append((points[i], points[j]))

    vectors = np.array(vectors)
    refs = np.array(refs)
    norms = np.linalg.norm(vectors, axis=1)

    maxIdx = np.argmax(norms)

    u = refs[maxIdx]

    otherVectors = np.delete(vectors, maxIdx, axis=0)
    otherRefs = np.delete(refs, maxIdx, axis=0)
    otherNorms = np.delete(norms, maxIdx, axis=0)

    orthogonality = np.abs(otherVectors @ vectors[maxIdx])

    m1 = np.max(orthogonality)
    m2 = np.max(otherNorms)
    if m1:
        orthogonality = orthogonality / m1
    if m2:
        otherNorms = otherNorms / m2

    coeff = orthogonality - otherNorms
    otherIdx = np.argmin(coeff)

    v = otherRefs[otherIdx]

    return u, v


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
    onLine = np.array([distToLine(p, a, b) for p in points]) <= width / 2
    if np.all(onLine):
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
