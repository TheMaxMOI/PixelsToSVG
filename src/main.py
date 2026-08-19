import numpy as np
from cv2 import IMREAD_UNCHANGED, destroyAllWindows, imdecode, imread, imshow, waitKey

from lib.png import SVGtoBytes

from .imageAnalysis.baseSVG import getBaseSVG
from .imageAnalysis.tests.models.circle import getCircle

src=getCircle()
srcBytes = SVGtoBytes(src)
arr0 = np.frombuffer(srcBytes, np.uint8)
srcImg = imdecode(arr0, IMREAD_UNCHANGED)

res = getBaseSVG(srcImg)
svgStr = res.export()
print(svgStr)

imgBytes = SVGtoBytes(svgStr)
arr = np.frombuffer(imgBytes, np.uint8)
img = imdecode(arr, IMREAD_UNCHANGED)

imshow("image", img)
waitKey(0)
destroyAllWindows()
