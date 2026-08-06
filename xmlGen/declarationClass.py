from .tagClass import Tag
from sys import stderr

allowedAttributes=["version", "encoding", "standalone"]
mandatoryAttr="version"

def getAttrValue(key, attributes):
    for k,value in attributes:
        if k == key:
            return value
    return None

class Declaration(Tag):
    def __init__(self, attributes):
        super().__init__("xml", attributes, True)

        for key,_ in self.attributes:
            if key not in allowedAttributes:
                raise ValueError(f"Declaration: __init__: {key} is not allowed!")

    def __repr__(self):
        if mandatoryAttr not in [key for (key, _) in self.attributes]:
            raise ValueError(f"Declaration: __repr__: declaration must have {mandatoryAttr}")

        if getAttrValue("version", self.attributes) not in ["1.0", "1.1"]:
            print("You are using an unofficial version of XML", file=stderr)

        if getAttrValue("standalone", self.attributes) not in [None, "yes", "no"]:
            raise ValueError("The attribute \"standalone\" must have the value \"yes\" or \"no\"")

        s=super().__repr__()
        return s[0] + '?' + s[1:-2] + '?' + s[-1]