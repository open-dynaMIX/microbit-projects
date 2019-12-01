from microbit import *
import random
import utime
from common import Dot, Highscore, Game


ME_BRIGHTNESS = 9
PARA_BRIGHTNESS = 7


class Ship(Game):
    def __init__(self, highscore):
        super().__init__(highscore)
        self.me = Dot(2, 4, 0, 0)
        self.set(self.me)

        self.paras = []
        self.para_amount = 1
        self.speed = 500

        self.side_effects = [
            (10, self.change_speed, 400),
            (25, self.increase_para_amount, 1),
            (40, self.change_speed, 300),
        ]

    def get_new_para(self):
        while True:
            new_para = Dot(
                random.randint(0, 4),
                0,
            )
            if new_para not in self.paras:
                return new_para

    def print_ints(self, value, loop=False):
        if self.score < 10:
            display.show(value, loop=loop)
        else:
            display.scroll(value, loop=loop)

    def set(self, dot, amount=ME_BRIGHTNESS):
        display.set_pixel(dot.x, dot.y, amount)

    def change_speed(self, speed):
        self.speed = speed

    def increase_para_amount(self, amount):
        self.para_amount += amount

    def run_side_effects(self):
        if len(self.side_effects):
            if self.side_effects[0][0] == self.score:
                side_effect = self.side_effects.pop(0)
                side_effect[1](side_effect[2])

    def handle_paras(self):
        self.run_side_effects()
        for para in list(self.paras):
            self.set(para, 0)
            para.y += 1
            if para.y > 4:
                self.paras.remove(para)
            else:
                self.set(para, PARA_BRIGHTNESS)
        while len(self.paras) < self.para_amount:
            if any([p.y in [0, 1] for p in self.paras]):
                break
            self.paras.append(self.get_new_para())
            self.set(self.paras[-1], PARA_BRIGHTNESS)
        self.set(self.me)

    def handle_button_presses(self):
        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll(self.highscore_val)
        if not self.me.x == 0:
            presses = button_a.get_presses()
            if presses:
                self.set(self.me, 0)
                self.me.x -= presses
                self.set(self.me)
        if not self.me.x == 4:
            presses = button_b.get_presses()
            if presses:
                self.set(self.me, 0)
                self.me.x += presses
                self.set(self.me)

    def validate(self):
        for para in self.paras:
            if para.y == 4:
                if self.me == para:
                    self.score += 1
                    self.paras.remove(para)
                else:
                    return False
        return True

    def _run(self):
        start = utime.ticks_ms()
        valid = False
        while True:
            self.handle_button_presses()
            if utime.ticks_diff(utime.ticks_ms(), start) > self.speed:
                valid = self.validate()
                if not valid:
                    break
                else:
                    valid = False
                self.handle_paras()
                start = utime.ticks_ms()
                valid = self.validate()


    def run(self):
        self._run()
        if self.score > self.highscore_val:
            self.highscore.set(self.score)
            display.scroll("HIGHSCORE")
        self.print_ints(self.score, loop=True)


highscore = Highscore()
game = Ship(highscore)
game.run()