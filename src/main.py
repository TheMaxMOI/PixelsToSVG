import numpy as np
from cv2 import IMREAD_UNCHANGED, destroyAllWindows, imdecode, imread, imshow, waitKey

from lib.png import SVGtoBytes
from src.randomize import getSVG

# from imageAnalysis.fittestShape import *
# from imageAnalysis.primaryColor import *

# img = imread("img_output/hexagone_small.png", IMREAD_UNCHANGED)

# outline = findOutline(findArea(img, findPrimary(img)))
# i = np.where(outline[..., None], img, 0)

# print(findPolygon(outline))

imgBytes = SVGtoBytes(getSVG(40).export())
arr = np.frombuffer(imgBytes, np.uint8)
img = imdecode(arr, IMREAD_UNCHANGED)

imshow("image", img)
waitKey(0)
destroyAllWindows()
