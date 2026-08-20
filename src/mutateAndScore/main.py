from time import time

from cv2 import (
    COLOR_BGR2RGBA,
    COLOR_BGRA2RGBA,
    IMREAD_UNCHANGED,
    WINDOW_NORMAL,
    cvtColor,
    destroyAllWindows,
    imread,
    imshow,
    namedWindow,
    resizeWindow,
    waitKey,
)

from lib.png import SVGtoBytes

from ..imageAnalysis.baseSVG import getBaseSVG
from ..progressBar import ProgressBar
from .config import MAX_ITER, SRC_IMAGE_PATH
from .mutator import Mutator
from .score import mse
from .utils import bytesToImage

targetImg = imread(SRC_IMAGE_PATH, IMREAD_UNCHANGED)
height, width = targetImg.shape[0], targetImg.shape[1]
if targetImg.shape[2] == 4:
    targetImg = cvtColor(targetImg, COLOR_BGRA2RGBA)
else:
    targetImg = cvtColor(targetImg, COLOR_BGR2RGBA)

scoring = lambda svg: mse(
    targetImg,
    bytesToImage(SVGtoBytes(svg.export(), (width, height))),
)
mutator = lambda svg: Mutator(svg, height, width).get()

currSVG = getBaseSVG(targetImg)
currScore = scoring(currSVG)

start = time()
bar = ProgressBar()
bar.set(0, MAX_ITER - 1)
bar.print()
for i in range(MAX_ITER):
    candidate = currSVG.copy()
    candidate = mutator(candidate)

    score = scoring(candidate)
    if score < currScore:
        currScore = score
        currSVG = candidate

    bar.set(i, MAX_ITER - 1)
    bar.print()

end = time()


print(
    f"The following SVG was found after {MAX_ITER} iterations and has a MSE of {currScore}."
)
print(
    f"It ran for {end - start}ms for an average of {(end - start) / MAX_ITER}ms per interations."
)
print()
print(currSVG.export())

img = bytesToImage(
    SVGtoBytes(currSVG.export(), (targetImg.shape[0], targetImg.shape[1]))
)

windowName = "Final Image"
namedWindow(windowName, WINDOW_NORMAL)
resizeWindow(windowName, 1920, 1080)
imshow(windowName, img)
waitKey(0)
destroyAllWindows()
