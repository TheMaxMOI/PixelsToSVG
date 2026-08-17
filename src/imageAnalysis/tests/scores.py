from cv2 import IMREAD_UNCHANGED, destroyAllWindows, imdecode, imshow, waitKey
from numpy import frombuffer, uint8, where

from lib.png import SVGtoBytes

from ..fittestShape import findArea, findOutline, findPolygon
from ..primaryColor import findPrimary
from ..scoringShape import circleScore, ellipseScore
from .models.circle import getCircle
from .models.ellipse import getEllipse
from .models.line import getLine
from .models.rectangle import getRectangle

models = [getCircle(), getLine(), getEllipse(), getRectangle()]
modelNames = ["circle", "line", "ellipse", "rectangle"]

for i,m in enumerate(models):
    imgBytes = SVGtoBytes(m)
    arr = frombuffer(imgBytes, uint8)
    img = imdecode(arr, IMREAD_UNCHANGED)


    outline = findOutline(findArea(img, findPrimary(img)))
    # i = where(outline[..., None], img, 0)

    # imshow("image", i)
    # waitKey(0)
    # destroyAllWindows()

    points = findPolygon(outline)
    print(points)

    print(modelNames[i],ellipseScore(points))
