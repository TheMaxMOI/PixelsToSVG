from time import time

from .config import PROGRESS_BAR, SMOOTHING

from .config import MAX_ITER, SRC_IMAGE_PATH


def getImage(path=SRC_IMAGE_PATH):
    from cv2 import (
        COLOR_BGR2RGBA,
        COLOR_BGRA2RGBA,
        IMREAD_UNCHANGED,
        cvtColor,
        imread,
        setNumThreads,
    )

    targetImg = imread(path, IMREAD_UNCHANGED)
    if targetImg is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    if targetImg.ndim == 2:
        return cvtColor(targetImg, COLOR_BGR2RGBA)
    if targetImg.shape[2] == 4:
        targetImg = cvtColor(targetImg, COLOR_BGRA2RGBA)
    else:
        targetImg = cvtColor(targetImg, COLOR_BGR2RGBA)

    return targetImg


def loopMutateScore(targetImg, barDisplay: bool = True):
    height, width = targetImg.shape[0], targetImg.shape[1]
    scoring = lambda svg: mse(targetImg, rasterize(svg, height, width))
    mutator = lambda svg: Mutator(svg, height, width).get()

    currSVG = getBaseSVG(targetImg, smoothed=SMOOTHING)
    currScore = scoring(currSVG)

    start = time()
    if barDisplay:
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

        if barDisplay:
            bar.set(i, MAX_ITER - 1)
            bar.print()

    end = time()
    return end - start, currSVG.export(), currScore


def summary(elapsedTime, svg: str, svgScore, shape, imgDisplay: bool):
    print(
        f"The following SVG was found after {MAX_ITER} iterations and has a MSE of {svgScore}."
    )
    print(
        f"It ran for {elapsedTime}s for an average of {(elapsedTime) / MAX_ITER}s per interations."
    )
    print()
    print(svg)

def main():
    targetImg = getImage()
    elapsed, svg, score = loopMutateScore(targetImg, PROGRESS_BAR)
    summary(elapsed, svg, score, targetImg.shape, False)

if __name__ == "__main__":
    main()