import numpy as np

det = lambda u,v : np.linalg.det(np.column_stack((u, v)))

def isConvex(points: np.ndarray, errors=1):
    N = len(points)
    sign = 0
    for i in range(N):
        u,v,w = points[i], points[(i+1)%N], points[(i+2)%N]
        p = det((w - v), (v - u))
        if p*sign < 0:
            if errors > 0:
                errors-=1
            else:
                return False
        else:
            sign = p
    return True


def circleScore(points):
    if len(points) <= 2:
        return 0

    points = np.array(points)

    if not isConvex(points):
        return 0

    M = points.mean(axis=0)  # center of mass
    dist = np.linalg.norm(points - M, axis=1)
    radiusMean = dist.mean()

    if radiusMean == 0:
        return 0

    coeff = dist.std() / radiusMean

    return max(0, 1 - coeff)

def ellipseScore(points):
    points = np.asarray(points, dtype=float)
    if len(points) <= 2 or not isConvex(points):
        return 0

    centered = points - points.mean(axis=0)

    # principal directions
    cov = np.cov(centered, rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    
    if np.any(vals <= 1e-12):
        return 0

    # reshaped to have a "circle"
    normalized_points = (centered @ vecs) / np.sqrt(vals)

    dist = np.linalg.norm(normalized_points, axis=1)
    radiusMean = dist.mean()

    if radiusMean == 0:
        return 0

    coeff = dist.std() / radiusMean

    return max(0.0, 1.0 - coeff)

def scoreLine(points):
    if len(points) < 2 :
        return 0

    points = np.array(points)
     # TODO