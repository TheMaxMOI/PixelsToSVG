from sys import stderr

from .tagClass import Tag
from .utils import getAttrValue

allowedAttributes = ["version", "encoding", "standalone"]
mandatoryAttr = "version"


class Declaration(Tag):
    """Class for XML declaration.

    Declaration is often discarded by xml parsers but keeping it might be useful for some applications.

    Parameters
    ----------
    attributes : list of attributes represented as tuples (name, value)

    Attributes
    ----------
    name : str
        name = "xml"

    attributes : list[tuple[str, str]]
        List of attributes.

    """
    def __init__(self, attributes):
        super().__init__("xml", attributes, True)

        for key, _ in self.attributes:
            if key not in allowedAttributes:
                raise ValueError(f"Declaration: __init__: {key} is not allowed!")

    def __repr__(self):
        """Convert the declaration to code.

        Returns
        -------
        s : str
            code representation of the declaration.

        Raises
        ------
        ValueError
            If the declaration misses mandatory attributes or has invalid values.

        Writes
        ------
        stderr
            If the declaration has an unofficial version.
        """
        if mandatoryAttr not in [key for (key, _) in self.attributes]:
            raise ValueError(
                f"Declaration: __repr__: declaration must have {mandatoryAttr}"
            )

        if getAttrValue("version", self.attributes) not in ["1.0", "1.1"]:
            print("You are using an unofficial version of XML", file=stderr)

        if getAttrValue("standalone", self.attributes) not in [None, "yes", "no"]:
            raise ValueError(
                'The attribute "standalone" must have the value "yes" or "no"'
            )

        s = super().__repr__()
        return s[0] + "?" + s[1:-2] + "?" + s[-1]
