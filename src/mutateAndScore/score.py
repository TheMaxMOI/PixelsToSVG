import numpy as np


def mse(target: np.ndarray, candidate: np.ndarray):  # Mean Square Error
    return np.mean((target.astype(np.float32) - candidate.astype(np.float32)) ** 2)
