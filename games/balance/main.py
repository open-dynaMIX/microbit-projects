from microbit import *
import random
from common import Dot, Highscore, Game


class Balance(Game):
    def __init__(self, highscore):
        super().__init__(highscore)

        self.me = Dot(2, 2, 0, 0)
        self.set(self.me, 9)

        self.fruit = self.get_fruit()
        self.set(self.fruit, 5)

    def get_fruit(self):
        while True:
            new_fruit = Dot(
                random.randint(0, 4),
                random.randint(0, 4),
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
            display.scroll(self.highscore_val)
            self.set(self.me, 9)
            self.set(self.fruit, 5)

    def _run(self):
        while True:
            self.handle_button_presses()
            x, x_val = self.get_movement("x")
            y, y_val = self.get_movement("y")
            new_pos = Dot(x, y, x_val, y_val)
            if abs(new_pos.x_val - self.me.x_val) < 40:
                new_pos.x, new_pos.x_val = self.me.x, self.me.x_val
            if abs(new_pos.y_val - self.me.y_val) < 40:
                new_pos.y, new_pos.y_val = self.me.y, self.me.y_val

            if -1 in [new_pos.x, new_pos.y]:
                break

            if not new_pos == self.me:
                self.set(self.me, 0)
                self.set(new_pos, 9)
            self.me = new_pos
            if self.validate():
                self.score += 1
                self.fruit = self.get_fruit()
                self.set(self.fruit, 5)


highscore = Highscore()
game = Balance(highscore)
game.run()