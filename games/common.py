from microbit import *


class Dot:
    def __init__(self, x, y, b):
        self.x = x
        self.y = y
        self.b = b  # brightness

    def show(self, b=None):
        display.set_pixel(self.x, self.y, b if b is not None else self.b)

    def set(self, x=None, y=None, b=9):
        self.show(b=0)
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.b = b if b is not None else self.b
        self.show()

    def __eq__(self, other):
        return [self.x, self.y] == [other.x, other.y]


class HS:  # HIGHSCORE
    def __init__(self, fname="score.txt"):
        self.fname = fname
        self.create()

    def create(self):
        try:
            self.read()
        except OSError:
            self.set(0)

    def read(self):
        with open(self.fname, 'r') as hs_file:
            return int(hs_file.read())

    def set(self, value):
        with open(self.fname, 'w') as hs_file:
            hs_file.write(str(value))
        return value


class Game:
    def __init__(self, hs):
        self.score = 0
        self.hs = hs  # highscore
        self.hs_val = self.hs.read()

    def print_ints(self, value, loop=False):
        if self.score < 10:
            display.show(value, loop=loop)
        else:
            display.scroll(value, loop=loop)

    def validate(self):
        raise NotImplementedError()

    def _run(self):
        raise NotImplementedError()

    def run(self):
        self._run()
        if self.score > self.hs_val:
            self.hs.set(self.score)
            display.scroll("1ST")
        self.print_ints(self.score, loop=True)
