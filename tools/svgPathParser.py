import re

numberRegex = re.compile(r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?")

InstrToNumOfArgsNonNull = {
    "M": 2,
    "L": 2,
    "H": 1,
    "V": 1,
    "Q": 4,
    "C": 6,
    "T": 2,
    "S": 4,
    "A": 7,
}


def makeInstr(fmt, numOfArgs):
    def instr(*args):
        if len(args) != numOfArgs:
            raise TypeError(f"Expected {numOfArgs} arguments but got {len(args)}")

        return fmt.format(*args)

    return instr


InstrToNumOfArgs = InstrToNumOfArgsNonNull | {"Z": 0}
M = makeInstr(".moveTo({},{})", InstrToNumOfArgs["M"])
L = makeInstr(".LineTo({},{})", InstrToNumOfArgs["L"])
H = makeInstr(".horizontalTo({})", InstrToNumOfArgs["H"])
V = makeInstr(".verticalTo({})", InstrToNumOfArgs["V"])
Q = makeInstr(".quadraticTo({},{},{},{})", InstrToNumOfArgs["Q"])
C = makeInstr(".cubicTo({},{},{},{},{},{})", InstrToNumOfArgs["C"])
T = makeInstr(".smoothQuadraticTo({},{})", InstrToNumOfArgs["T"])
S = makeInstr(".smoothCubicTo({},{},{},{})", InstrToNumOfArgs["S"])
A = makeInstr(".ellipticalArcTo({},{},{},{},{},{},{})", InstrToNumOfArgs["A"])
Z = makeInstr(".stopHere()", InstrToNumOfArgs["Z"])

charToInstr = {
    "M": M,
    "L": L,
    "H": H,
    "V": V,
    "Q": Q,
    "C": C,
    "T": T,
    "S": S,
    "A": A,
    "Z": Z,
}


class Item:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)


class Letter(Item):
    def __init__(self, val):
        super().__init__(val)


class Number(Item):
    def __init__(self, val):
        super().__init__(val)


class Separator(Item):
    def __init__(self, val):
        super().__init__(val)


class Lexer:
    def streamifier(self, s: str):
        i = 0
        while i < len(s):
            char = s[i]
            command = char.upper()

            if command in charToInstr:
                yield Letter(char)
                i += 1
            elif char.isspace() or char == ",":
                yield Separator(char)
                i += 1
            else:
                match = numberRegex.match(s, i)
                if match is None:
                    raise ValueError(f"Invalid number at position {i}")

                value = match.group()

                yield Number(value)
                i += len(value)

    def __init__(self, s):
        self.stream = self.streamifier(s)
        self.peeked_token = None

    def get(self):
        if self.peeked_token is not None:
            token = self.peeked_token
            self.peeked_token = None

            return token
        try:
            return next(self.stream)
        except StopIteration:
            return None

    def peek(self):
        if self.peeked_token is None:
            try:
                self.peeked_token = next(self.stream)
            except StopIteration:
                self.peeked_token = None

        return self.peeked_token


def parser(s):
    instructions = []
    current_point = (0.0, 0.0)
    subpath_start = current_point

    def add(func, *args):
        instructions.append(func(*args))

    def skipSeparators():
        while isinstance(lexer.peek(), Separator):
            lexer.get()

    def getNumber():
        skipSeparators()
        tk = lexer.get()
        if not isinstance(tk, Number):
            raise TypeError(f"Expected a number but got {tk}")
        try:
            return float(tk.val)
        except ValueError as error:
            raise ValueError(f"Invalid number: {tk.val}") from error

    def makeAbsolute(command, args, relative):
        nonlocal current_point, subpath_start
        x, y = current_point

        if command in ("M", "L", "T"):
            next_point = (args[0] + x, args[1] + y) if relative else (args[0], args[1])
            if command == "M":
                subpath_start = next_point
            current_point = next_point
            return next_point
        if command == "H":
            current_point = (x + args[0], y) if relative else (args[0], y)
            return (current_point[0],)
        if command == "V":
            current_point = (x, y + args[0]) if relative else (x, args[0])
            return (current_point[1],)
        if command == "Q":
            values = (
                (
                    args[0] + x,
                    args[1] + y,
                    args[2] + x,
                    args[3] + y,
                )
                if relative
                else tuple(args)
            )
            current_point = values[2:4]
            return values
        if command in ("C", "S"):
            values = (
                tuple(
                    value + (x if index % 2 == 0 else y)
                    for index, value in enumerate(args)
                )
                if relative
                else tuple(args)
            )
            current_point = values[-2:]
            return values
        if command == "A":
            values = list(args)
            if relative:
                values[5] += x
                values[6] += y
            current_point = (values[5], values[6])
            return tuple(values)
        raise ValueError(f"Unsupported SVG path command: {command}")

    lexer = Lexer(s)
    while True:
        skipSeparators()

        tk = lexer.get()
        if tk is None:
            break
        if not isinstance(tk, Letter):
            raise TypeError(f"Expected a command but got {tk}")

        command = tk.val.upper()
        relative = tk.val.islower()
        if command == "Z":
            add(Z)
            current_point = subpath_start
            continue

        if command not in InstrToNumOfArgsNonNull:
            raise ValueError(f"Unknown command: {command}")

        argCount = InstrToNumOfArgsNonNull[command]
        isFirstGroup = True
        while True:
            args = [getNumber() for _ in range(argCount)]

            theCommand = "L" if command == "M" and not isFirstGroup else command
            AbsArgs = makeAbsolute(theCommand, args, relative)

            add(charToInstr[theCommand], *AbsArgs)
            isFirstGroup = False

            skipSeparators()
            if not isinstance(lexer.peek(), Number):
                break

    return "\n".join(instructions)


### On the fly example
# curve="M13.968,15.171a2.7,2.7,0,0,1-2.427-1.251,6.713,6.713,0,0,1-.813-3.644,7.215,7.215,0,0,1,.868-3.9,2.784,2.784,0,0,1,2.481-1.343,2.684,2.684,0,0,1,2.468,1.251,7.283,7.283,0,0,1,.772,3.76,6.981,6.981,0,0,1-.861,3.8A2.79,2.79,0,0,1,13.968,15.171ZM14.05,6.3a1.365,1.365,0,0,0-1.289.981,7.967,7.967,0,0,0-.414,2.943,7.039,7.039,0,0,0,.414,2.758,1.345,1.345,0,0,0,1.268.919,1.323,1.323,0,0,0,1.268-.94,7.716,7.716,0,0,0,.393-2.827A7.991,7.991,0,0,0,15.3,7.258,1.315,1.315,0,0,0,14.05,6.3Z"
# print(parser(curve))
