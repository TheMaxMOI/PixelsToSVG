from cv2 import IMREAD_UNCHANGED, destroyAllWindows, imdecode, imshow, waitKey
from numpy import frombuffer, uint8, where

from lib.png import SVGtoBytes

from ..detectShape import findArea, findOutline, findPolygon
from ..majorColor import findPrimary
from ..shapingRoughly import getfittestShape
from .models.circle import getCircle
from .models.ellipse import getEllipse
from .models.line import getLine
from .models.rectangle import getRectangle

models = [getCircle(), getLine(), getEllipse(), getRectangle()]
modelNames = ["circle", "line", "ellipse", "rectangle"]

for i, m in enumerate(models):
    imgBytes = SVGtoBytes(m)
    arr = frombuffer(imgBytes, uint8)
    img = imdecode(arr, IMREAD_UNCHANGED)

    color = findPrimary(img)
    outline = findOutline(findArea(img, color))
    points = findPolygon(outline)

    shape = getfittestShape(points, color)

    print(modelNames[i], shape.name)