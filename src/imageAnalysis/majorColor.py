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

def findBackground(img:np.ndarray, primaryColor=None):
    assert len(img.shape) == 3

    primaryColor = primaryColor if (primaryColor) else findPrimary(img)

    nChannels = img.shape[2]
    pixelsArray = img.reshape(-1, nChannels)

    if nChannels >= 4:
        visiblePixels = pixelsArray[pixelsArray[:, 3] > 0]
        if visiblePixels.size == 0:
            return np.zeros(nChannels, dtype=img.dtype)
        pixelsArray = visiblePixels

    foundColors, freq = np.unique(pixelsArray, axis=0, return_counts=True)

    mask = ~np.all(foundColors == primaryColor, axis=1)
    
    otherColors = foundColors[mask]
    otherFreq = freq[mask]
    
    if len(otherFreq) == 0:
        return np.zeros(nChannels, dtype=img.dtype)
    
    return np.sum(otherColors * otherFreq[:, np.newaxis], axis=0) / np.sum(otherFreq)
