import numpy as np


def mse(target, candidate): # Mean Square Error
    return np.mean((target - candidate) ** 2)
