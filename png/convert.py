from pathlib import Path

import resvg_py

DEFAULT_FOLD = "img_output"

dest_fold = Path(DEFAULT_FOLD)
if not dest_fold.exists():
    raise NameError(f"The path {dest_fold} doesn't exist!")


def SVGtoPNG(
    svg: str,
    name="output",
    dest=dest_fold,
    targetSize: tuple[int, int] | None = None,
):

    theName = Path(name).with_suffix(".png")
    theDest = dest / theName

    renderOpts = {}
    if targetSize is not None:
        renderOpts["width"], renderOpts["height"] = targetSize

    theDest.write_bytes(resvg_py.svg_to_bytes(svg_string=svg, **renderOpts))

    return theDest


# # On the fly example
# svg='<?xml version="1.0" encoding="UTF-8"?>\n<svg viewBox="-1 -1 42 37" fill-opacity="0" width="420" height="370" xmlns="http://www.w3.org/2000/svg">\n    <polygon stroke="#ff0000" stroke-width="1" points="30.0,34.64 10.0,34.64 0,17.32 10.0,0 30.0,0 40,17.32"/></svg>'
# toPNG(svg, "hexagone")
# toPNG(svg, "hexagone_small", targetSize=(42,37))
