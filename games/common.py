from microbit import *


class Dot:
    def __init__(self, x, y, x_val=None, y_val=None):
        self.x = x
        self.y = y
        self.x_val = x_val
        self.y_val = y_val

    def coor(self):
        return self.x, self.y

    def __eq__(self, other):
        return [self.x, self.y] == [other.x, other.y]


class Highscore:
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        self.create()

    def create(self):
        try:
            self.read()
        except OSError:
            self.set(0)

    def read(self):
        with open(self.filename, 'r') as highscore_file:
            return int(highscore_file.read())

    def set(self, value):
        with open(self.filename, 'w') as highscore_file:
            highscore_file.write(str(value))
        return value


class Game:
    def __init__(self, highscore):
        self.score = 0
        self.highscore = highscore
        self.highscore_val = self.highscore.read()

    def set(self, dot, amount):
        display.set_pixel(dot.x, dot.y, amount)

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
        if self.score > self.highscore_val:
            self.highscore.set(self.score)
            display.scroll("HIGHSCORE")
        self.print_ints(self.score, loop=True)
