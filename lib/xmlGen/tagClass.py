from __future__ import annotations

from copy import deepcopy

from .config import INDENT
from .utils import hasAttribute


def isAttributeList(lst) -> bool:
    """Check an object is a list of attributes."""
    return (
        type(lst) == list
        and len(lst) != 0
        and type(lst[0]) == tuple
        and len(lst[0]) == 2
        and type(lst[0][0]) == type(lst[0][1]) == str
    )


def isData(lst) -> bool:
    """Check an object is a list of data."""
    return type(lst) == list and len(lst) != 0 and isinstance(lst[0], (Tag, str))


def isEmptyList(lst) -> bool:
    """Check an object is an empty list."""
    return type(lst) == list and len(lst) == 0


def toString(elm) -> str:
    """Wrap the str function to extend it to lists of attributes or data."""
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


def indent(s: str) -> str:
    """Indent lines from a string."""
    lines = s.splitlines(keepends=True)

    string = ""
    for line in lines:
        string = f"{string}{INDENT}{line}"

    return string


def areUniqueAttributes(lst: list[tuple[str, str]]) -> bool:
    """Check if a list of attributes is unique."""
    if not lst:
        return True

    attributes = set()
    for key, _ in lst:
        attributes.add(key)

    return len(lst) == len(attributes)


class Tag:
    """A class to represent an XML tag.

    xml is a tree-like structure where each node is a tag with multiple attributes or simple strings.

    Parameters
    ----------
    name : str
        The name of the tag.

    attributes : list[tuple[str, str]], optional
        List of attributes for the tag. Each attribute is a tuple of name and value.

    isEmpty : bool, optional
        If True, the tag is considered empty and cannot have data.

    Attributes
    ----------
    name : str
        The name of the tag.

    attributes : list[tuple[str, str]]
        List of attributes.

    data : list[str | Tag] | None
        List of string or tags that are children.
        None if the tag instance can't have children.

    """

    def __init__(
        self, name: str, attributes: list[tuple[str, str]] | None = None, isEmpty=False
    ):
        self.name = name
        self.attributes = list(attributes) if attributes is not None else []
        self.data = None if (isEmpty) else []  # if not None then list[str|Tag]

        if not areUniqueAttributes(self.attributes):
            raise ValueError("Tag: __init__: All given attributes must be unique!")

    def addAttribute(self, attr: tuple[str, str]):
        """Add an attribute to the tag.

        Parameters
        ----------
        attr : tuple[str, str]
            The attribute to add.

        Returns
        -------
        self : Tag
            The updated tag instance. This allows chaining.

        Raises
        ------
        ValueError
            If the tag already has the given attribute.
        """
        if hasAttribute(attr[0], self.attributes):
            raise ValueError("Tag: __init__: All attributes must be unique!")

        self.attributes.append(attr)
        return self

    def setData(self, data: list[str | Tag]):
        """Set the data for the tag.

        Parameters
        ----------
        data : list[str | Tag]
            List of strings or Tag instances to set as tag's children nodes.

        Returns
        -------
        self : Tag
            The updated tag instance. This allows chaining even though it's not super helpful for this method.

        Raises
        ------
        TypeError
            If the tag was declared as empty.
        """
        if self.data == None:
            raise TypeError(
                f"Tag: setData: The tag name {self.name} is meant to be empty!"
            )

        self.data = data

        return self

    def copy(self) -> Tag:
        """Create a copy of the tag instance.

        Returns
        -------
        t : Tag
            A new Tag instance with the exact name, attributes, and data.
        """
        return deepcopy(self)

    def __repr__(self) -> str:
        """Convert the tag to code.

        Returns
        -------
        s : str
            code representation of the tag.
        """
        attrs = f" {toString(self.attributes)}" if self.attributes else ""

        if self.data is None:
            return f"<{self.name}{attrs}/>"

        data = toString(self.data)
        content = f"\n{indent(data)}\n" if data else "\n"
        
        return f"<{self.name}{attrs}>{content}</{self.name}>"

    def visit(self, func) -> None:
        """Visit the tree while applying a function

        Parameters
        ----------
        func : callable
            A function to apply on each node wheter it's a tag or a string.

        Returns
        -------
        result : None
            For that matter, one should use nonlocal variables to store useful information.
        """
        func(self)

        if self.data:
            for child in self.data:
                if isinstance(child, Tag):
                    child.visit(func)
