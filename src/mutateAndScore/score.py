import numpy as np


def mse(target: np.ndarray, candidate: np.ndarray):  # Mean Square Error
    diff = target - candidate
    return np.mean(diff * diff)
