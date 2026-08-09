from pathlib import Path

import resvg_py


def toPNG(
    svg: str,
    name="output",
    dest="img_output",
    targetSize: tuple[int, int] | None = None,
):
    dir = Path(dest)
    if not dir.exists():
        raise NameError(f"The path {dir} doesn't exist!")

    theName = Path(name).with_suffix(".png")
    theDest = dir / theName

    renderOpts = {}
    if targetSize is not None:
        renderOpts["width"], renderOpts["height"] = targetSize

    theDest.write_bytes(
        resvg_py.svg_to_bytes(svg_string=svg, **renderOpts)
    )

    return theDest

# # On the fly example
# svg='<?xml version="1.0" encoding="UTF-8"?>\n<svg viewBox="-1 -1 42 37" fill-opacity="0" width="420" height="370" xmlns="http://www.w3.org/2000/svg">\n    <polygon stroke="#ff0000" stroke-width="1" points="30.0,34.64 10.0,34.64 0,17.32 10.0,0 30.0,0 40,17.32"/></svg>'
# toPNG(svg, "hexagone")
# toPNG(svg, "hexagone_small", targetSize=(42,37))
