MAX_UINT8 = 256


def rgb(r: int, g: int, b: int):
    return f"#{r % MAX_UINT8:02X}{g % MAX_UINT8:02X}{b % MAX_UINT8:02X}"
