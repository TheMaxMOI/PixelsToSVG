from cv2 import (
    COLOR_BGR2RGB,
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
from .config import MAX_ITER, SRC_IMAGE_PATH
from .mutator import Mutator
from .score import mse
from .utils import bytesToImage

targetImg = imread(SRC_IMAGE_PATH, IMREAD_UNCHANGED)
if targetImg.shape[2] == 4:
    targetImg = cvtColor(targetImg, COLOR_BGRA2RGBA)
else:
    targetImg = cvtColor(targetImg, COLOR_BGR2RGB)

scoring = lambda svg: mse(
    targetImg,
    bytesToImage(SVGtoBytes(svg.export(), (targetImg.shape[0], targetImg.shape[1]))),
)


currSVG = getBaseSVG(targetImg)
currScore = scoring(currSVG)

for _ in range(MAX_ITER):
    candidate = currSVG.copy()

    m = Mutator(candidate)
    candidate = m.get()

    score = scoring(candidate)
    if score < currScore:
        currScore = score
        currSVG = candidate


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
