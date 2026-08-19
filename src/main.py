import numpy as np
from cv2 import (
    COLOR_BGR2RGB,
    COLOR_BGRA2RGBA,
    IMREAD_UNCHANGED,
    cvtColor,
    destroyAllWindows,
    imdecode,
    imshow,
    waitKey,
)

from lib.png import SVGtoBytes

from .imageAnalysis.baseSVG import getBaseSVG
from .imageAnalysis.tests.models.circle import getCircle
from .imageAnalysis.tests.models.rectangle import getRectangle

src = getCircle()
srcBytes = SVGtoBytes(src)
arr0 = np.frombuffer(srcBytes, np.uint8)
srcImg = imdecode(arr0, IMREAD_UNCHANGED)
if srcImg.shape[2] == 4:  # cv2 opens the image in BGR
    srcImg = cvtColor(srcImg, COLOR_BGRA2RGBA)
else:
    srcImg = cvtColor(srcImg, COLOR_BGR2RGB)

res = getBaseSVG(srcImg,background=True)
svgStr = res.export()
print(svgStr)

imgBytes = SVGtoBytes(svgStr)
arr = np.frombuffer(imgBytes, np.uint8)
img = imdecode(arr, IMREAD_UNCHANGED)

imshow("image", img)
waitKey(0)
destroyAllWindows()
