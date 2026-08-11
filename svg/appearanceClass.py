class Appearance:
    color_key = ""

    def __init__(self, color: str, opacity: float):
        if type(self) == Appearance:
            raise TypeError("User should not initialize such a class (trigger by Appearance)!")

        self.color = color
        self.opacity = opacity

    def use(self) -> list[tuple[str, str]]:
        return [
            (self.color_key, f"{self.color}"),
            ("opacity", f"{self.opacity}"),
        ]


class Outline(Appearance):
    color_key = "stroke"

    def __init__(self, stroke: str, width: float, opacity: float):
        self.width = width
        super().__init__(stroke, opacity)

    def use(self) -> list[tuple[str, str]]:
        attributes = super().use()
        attributes.append(("stroke-width", f"{self.width}"))
        return attributes


class Coloring(Appearance):
    color_key = "fill"

    def __init__(self, fill: str, opacity: float):
        super().__init__(fill, opacity)
