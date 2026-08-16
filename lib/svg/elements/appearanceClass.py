from ...rgb import MAX_UINT8, rgb
from .utils.mathHelpers import randint, random


class Appearance:
    color_key = ""

    def __init__(self, color: str, opacity: float = 1):
        if type(self) == Appearance:
            raise TypeError(
                "User should not initialize such a class (trigger by Appearance)!"
            )

        self.color = color
        self.opacity = opacity

    def use(self) -> list[tuple[str, str]]:
        return [
            (self.color_key, f"{self.color}"),
            (f"{self.color_key}-opacity", f"{self.opacity}"),
        ]

class Outline(Appearance):
    color_key = "stroke"

    def __init__(self, stroke: str, width: float, opacity: float = 1):
        self.width = width
        super().__init__(stroke, opacity)

    def use(self) -> list[tuple[str, str]]:
        attributes = super().use()
        attributes.append(("stroke-width", f"{self.width}"))
        return attributes

    @staticmethod
    def generate():
        return Outline(rgb(*randint(0, MAX_UINT8, 3)), randint(0, 10), round(random(), 2))


class Coloring(Appearance):
    color_key = "fill"

    def __init__(self, fill: str, opacity: float = 1):
        super().__init__(fill, opacity)

    @staticmethod
    def generate():
        return Coloring(rgb(*randint(0, MAX_UINT8, 3)), round(random(), 2))
