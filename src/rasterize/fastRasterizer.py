import numpy as np
from ...lib.rgb import hexToRGB

def blendOver(canvas: np.ndarray, mask: np.ndarray, colorRGB, opacity: float) -> None: # Porter-Duff
    if opacity <= 0:
        return

    idx = mask.astype(bool)
    if not idx.any():
        return

    srcA = float(opacity)
    dstA = canvas[idx, 3].astype(np.float32) / 255.0
    outA = srcA + dstA * (1.0 - srcA)

    srcRGB = np.asarray(colorRGB, dtype=np.float32)
    dstRGB = canvas[idx, :3].astype(np.float32)

    safe = outA > 1e-6
    blended = srcRGB * srcA + dstRGB * dstA[:, None] * (1.0 - srcA)
    outRGB = np.zeros_like(blended)
    outRGB[safe] = blended[safe] / outA[safe, None]

    canvas[idx, :3] = np.clip(outRGB, 0, 255).astype(np.uint8)
    canvas[idx, 3] = np.clip(outA * 255.0, 0, 255).astype(np.uint8)


def clipBB(bbox, height, width):
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    x1, y1 = min(width, int(x1)), min(height, int(y1))
    if x1 <= x0 or y1 <= y0:
        return None
    return x0, y0, x1, y1


def rasterizeShape(shape, canvas: np.ndarray, height: int, width: int) -> None:
    clipped = clipBB(shape.boundingBox(), height, width)
    if clipped is None:
        return

    x0, y0, x1, y1 = clipped
    region = canvas[y0:y1, x0:x1]

    if getattr(shape, "inner", None) is not None:
        mask = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
        shape.paintOnMask(mask, filled=True, origin=(x0, y0))
        blendOver(region, mask, hexToRGB(shape.inner.color), shape.inner.opacity)

    if getattr(shape, "outer", None) is not None:
        mask = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
        shape.paintOnMask(mask, filled=False, origin=(x0, y0))
        blendOver(region, mask, hexToRGB(shape.outer.color), shape.outer.opacity)


def rasterize(svg, height: int, width: int) -> np.ndarray:
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    for elm in svg.data:
        rasterizeShape(elm, canvas, height, width)
    return canvas