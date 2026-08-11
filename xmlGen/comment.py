def comment(s: str) -> str:
    """Produce a comment from the given string.

    The produced comment is to be added to a xml code

    Parameters
    ----------
    s : str
        comment content

    Returns
    -------
    comment : str
        xml comment
    """
    return f"<!-- {s} -->"
