import numpy as np

MAX_UINT8 = 256


def visiblePixels(img: np.ndarray):
    nChannels = img.shape[2]
    pixelsArray = img.reshape(-1, nChannels)

    if nChannels >= 4:
        pixelsArray = pixelsArray[pixelsArray[:, 3] > 0]

    return pixelsArray, nChannels


def colorHistogram(pixelsArray: np.ndarray):
    pixelsArray = np.ascontiguousarray(pixelsArray)

    if pixelsArray.size == 0:
        return pixelsArray, np.array([], dtype=np.intp)

    voidDtype = np.dtype((np.void, pixelsArray.dtype.itemsize * pixelsArray.shape[1]))
    viewed = pixelsArray.view(voidDtype).ravel()

    _, firstIdx, counts = np.unique(viewed, return_index=True, return_counts=True)
    colors = pixelsArray[firstIdx]

    return colors, counts


def findPrimary(img: np.ndarray):
    assert len(img.shape) == 3

    pixelsArray, nChannels = visiblePixels(img)

    if pixelsArray.size == 0:
        return np.zeros(nChannels, dtype=img.dtype)

    colors, counts = colorHistogram(pixelsArray)
    return colors[np.argmax(counts)]


def findBackground(img: np.ndarray, primaryColor: np.ndarray | None = None):
    assert len(img.shape) == 3

    pixelsArray, nChannels = visiblePixels(img)

    if pixelsArray.size == 0:
        return np.zeros(nChannels, dtype=img.dtype)

    primaryColor = primaryColor if (primaryColor is not None) else findPrimary(img)

    colors, counts = colorHistogram(pixelsArray)

    mask = ~np.all(colors == primaryColor, axis=1)
    otherColors = colors[mask]
    otherCounts = counts[mask]

    if len(otherCounts) == 0:
        return np.zeros(nChannels, dtype=img.dtype)

    return np.sum(otherColors * otherCounts[:, np.newaxis], axis=0) / np.sum(
        otherCounts
    )


def findPrimaryAndBackground(img: np.ndarray):
    assert len(img.shape) == 3

    pixelsArray, nChannels = visiblePixels(img)

    if pixelsArray.size == 0:
        z = np.zeros(nChannels, dtype=img.dtype)
        return z, z

    colors, counts = colorHistogram(pixelsArray)

    primaryIdx = np.argmax(counts)
    primaryColor = colors[primaryIdx]

    mask = np.ones(len(colors), dtype=bool)
    mask[primaryIdx] = False
    otherColors = colors[mask]
    otherCounts = counts[mask]

    if len(otherCounts) == 0:
        backgroundColor = np.zeros(nChannels, dtype=img.dtype)
    else:
        backgroundColor = np.sum(
            otherColors * otherCounts[:, np.newaxis], axis=0
        ) / np.sum(otherCounts)

    return primaryColor, backgroundColor
