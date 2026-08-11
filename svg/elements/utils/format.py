def stringify(points):
    s = ""

    isFirst = True
    for x, y in points:
        s = f"{s}{'' if isFirst else ' '}{x},{y}"
        isFirst = False

    return s