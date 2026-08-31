MAX_UINT8 = 256


def rgb(r: int, g: int, b: int):
    r, g, b = int(r), int(g), int(b)
    return f"#{r % MAX_UINT8:02X}{g % MAX_UINT8:02X}{b % MAX_UINT8:02X}"

def hexToRGB(hexColor: str) -> tuple[int, int, int]:
    h = hexColor.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))