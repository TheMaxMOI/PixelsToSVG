import numpy as np

MAX_UINT8 = 256


def findPrimary(img: np.ndarray):
    assert len(img.shape) == 3

    nChannels = img.shape[2]
    pixelsArray = img.reshape(-1, nChannels)

    if nChannels >= 4:
        visiblePixels = pixelsArray[pixelsArray[:, 3] > 0]
        if visiblePixels.size == 0:
            return np.zeros(nChannels, dtype=img.dtype)
        pixelsArray = visiblePixels

    foundColors, freq = np.unique(pixelsArray, axis=0, return_counts=True)
    return foundColors[np.argmax(freq)]
