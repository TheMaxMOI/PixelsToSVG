def updateAttribute(attrName, newVal, attributes):
    i = 0
    for key, _ in attributes:
        if key == attrName:
            break
        i += 1

    if i < len(attributes):
        attributes[i] = (attrName, newVal)
        return True

    return False


update = lambda attrName, newVal, attributes: (
    None
    if updateAttribute(attrName, newVal, attributes)
    else attributes.append((attrName, newVal))
)
