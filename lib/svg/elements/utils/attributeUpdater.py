def update(attrName: str, newVal: str, attributes: list[tuple[str, str]]) -> None:
    """Update an attribute's value in-place, or append it if it doesn't exist."""
    for i, (key, _) in enumerate(attributes):
        if key == attrName:
            attributes[i] = (attrName, str(newVal))
            return
    attributes.append((attrName, str(newVal)))