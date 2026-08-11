def hasAttribute(attrName: str, attributes: list[tuple[str, str]]) -> bool:
    for key, _ in attributes:
        if key == attrName:
            return True
    return False


def getAttrValue(key: str, attributes: list[tuple[str, str]]) -> str | None:
    """Get the value of an attribute from a list of attributes.

    Parameters
    ----------
    key : str
        The name of the attribute to search for.

    attributes : list[tuple[str, str]]
        The list of attributes to search in.

    Returns
    -------
    value : str or None
        The value of the attribute if found, otherwise None.
    """
    for k, value in attributes:
        if k == key:
            return value
    return None
