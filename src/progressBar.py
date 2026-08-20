DONE = "█"
LAST_2_DONE = "▒"
LEFT = "░"


class ProgressBar:
    def __init__(self):
        self.current = 0
        self.max = 0

    def set(self, current, max):
        self.current = current
        self.max = max

    def print(self):
        x = 100
        if self.max <= 0 or self.current >= self.max:
            t = 100
        else:
            x = self.current * 100 / self.max
            t = int(x)

        if t == 100:
            s = DONE * 100
            end = "\n"
        elif t >= 2:
            s = DONE * (t - 2) + LAST_2_DONE * 2 + LEFT * (100 - t)
            end = "\r"
        else:
            s = LAST_2_DONE * t + LEFT * (100 - t)
            end = "\r"

        s += f" {x:.2f}%"

        print(s, end=end, flush=True)
