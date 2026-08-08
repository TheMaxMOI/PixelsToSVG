def hasAttribute(attrName, attributes):
    for (key,_) in attributes:
        if key == attrName:
            return True
    return False

def getAttrValue(key, attributes):
    for k,value in attributes:
        if k == key:
            return value
    return None
