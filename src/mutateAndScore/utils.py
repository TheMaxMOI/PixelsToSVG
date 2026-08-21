from cv2 import IMREAD_UNCHANGED, imdecode, setNumThreads

setNumThreads(0)

from numpy import frombuffer, uint8


def bytesToImage(bytes):
    arr = frombuffer(bytes, uint8)
    return imdecode(arr, IMREAD_UNCHANGED)
