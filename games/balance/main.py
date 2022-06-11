from microbit import *
import random
from common import Dot as DotCo, HS, Game


ME_BRIGHTNESS = 9
FRUIT_BRIGHTNESS = 5


class Dot(DotCo):
    def __init__(self, x, y, xv, yv, b):
        super().__init__(x, y, b)
        self.xv =xv
        self.yv = yv


class Balance(Game):
    def __init__(self, hs):
        super().__init__(hs)

        self.me = Dot(2, 2, 0, 0, ME_BRIGHTNESS)
        self.me.show()

        self.fruit = self.get_fruit()
        self.fruit.show()

    def get_fruit(self):
        while True:
            new_fruit = Dot(
                random.randint(0, 4),
                random.randint(0, 4),
                None,
                None,
                FRUIT_BRIGHTNESS,
            )
            if not new_fruit == getattr(self, "fruit", None):
                return new_fruit

    def get_movement(self, direction):
        reading = getattr(accelerometer, "get_" + direction)()
        if -350 > reading or 350 < reading:
            return -1, reading
        elif 75 > reading > -75:
            return 2, reading
        elif 75 < reading < 225:
            return 3, reading
        elif reading > 225:
            return 4, reading
        elif -75 > reading > -225:
            return 1, reading
        else:
            return 0, reading

    def validate(self):
        if self.fruit == self.me:
            return True

    def handle_button_presses(self):
        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll(self.hs_val)
            self.set(self.me, 9)
            self.set(self.fruit, 5)

    def _run(self):
        while True:
            self.handle_button_presses()
            x, xv = self.get_movement("x")
            y, yv = self.get_movement("y")
            new_pos = Dot(x, y, xv, yv, ME_BRIGHTNESS)
            if abs(new_pos.xv - self.me.xv) < 40:
                new_pos.x, new_pos.xv = self.me.x, self.me.xv
            if abs(new_pos.yv - self.me.yv) < 40:
                new_pos.y, new_pos.yv = self.me.y, self.me.yv

            if -1 in [new_pos.x, new_pos.y]:
                break

            if not new_pos == self.me:
                self.me.show(b=0)
                self.me = new_pos
                self.me.show(b=ME_BRIGHTNESS)

            if self.validate():
                self.score += 1
                self.fruit = self.get_fruit()
                self.fruit.show()


hs = HS()
game = Balance(hs)
game.run()