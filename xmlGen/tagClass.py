from __future__ import annotations

from .utils import hasAttribute


def isAttributeList(lst):
    return (
        type(lst) == list
        and len(lst) != 0
        and type(lst[0]) == tuple
        and len(lst[0]) == 2
        and type(lst[0][0]) == type(lst[0][1]) == str
    )


def isData(lst):
    return type(lst) == list and len(lst) != 0 and type(lst[0]) in (Tag, str)


def isEmptyList(lst):
    return type(lst) == list and len(lst) == 0


def toString(elm):
    if isAttributeList(elm):
        s = ""
        isFirst = True
        for key, value in elm:
            s = f'{s}{"" if isFirst else " "}{key}="{value}"'
            isFirst = False
        return s
    elif isData(elm) or isEmptyList(elm):
        s = ""
        for e in elm:
            if s:
                s += "\n"
            s += str(e)
        return s
    else:
        return str(elm)


def indent(s: str):
    INDENT = " " * 4
    lines = s.splitlines(keepends=True)

    string = ""
    for line in lines:
        string = f"{string}{INDENT}{line}"

    return string


def areUniqueAttributes(lst):
    if not lst:
        return True

    attributes = set()
    for key, _ in lst:
        attributes.add(key)

    return len(lst) == len(attributes)


class Tag:
    def __init__(
        self, name: str, attributes: list[tuple[str, str]] | None = None, isEmpty=False
    ):
        self.name = name
        self.attributes = list(attributes) if attributes is not None else []
        self.data = None if (isEmpty) else []  # if not None then list[str|Tag]

        if not areUniqueAttributes(self.attributes):
            raise ValueError("Tag: __init__: All given attributes must be unique!")

    def addAttribute(self, attr: tuple[str, str]):
        if hasAttribute(attr[0], self.attributes):
            raise ValueError("Tag: __init__: All attributes must be unique!")

        self.attributes.append(attr)
        return self  # so the addAttributes can be chained

    def setData(self, data: list[str | Tag]):
        if self.data == None:
            raise TypeError(
                f"Tag: setData: The tag name {self.name} is meant to be empty!"
            )

        self.data = data

        return self  # chaining possible but really for declaration with update

    def copy(self):
        isEmpty = self.data == None
        t = Tag(self.name, self.attributes, isEmpty)

        if not isEmpty:
            data = []
            for elm in self.data:
                if type(elm) == str:
                    data.append(elm)
                else:
                    data.append(elm.copy())

            t.setData(data)

        return t

    def __repr__(self):
        s = f"<{self.name}"

        if self.attributes:
            s += f" {toString(self.attributes)}"

        if self.data == None:
            s += "/>"
            return s

        s += ">\n"
        data = toString(self.data)
        if data:
            s += indent(data)
            s += "\n"
        s += f"</{self.name}>"

        return s
