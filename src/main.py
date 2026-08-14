from cv2 import IMREAD_UNCHANGED, destroyAllWindows, imread, imshow, waitKey

from fittestShape import *
from primaryColor import *

img = imread("img_output/hexagone_small.png", IMREAD_UNCHANGED)
outline = findOutline(findArea(img, findPrimary(img)))

i = np.where(outline[..., None], img, 0)
print(findPolygon(outline))

imshow("image", i)
waitKey(0)
destroyAllWindows()
