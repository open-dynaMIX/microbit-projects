from microbit import *
import random
import utime
from common import Dot, HS, Game


ME_BRIGHTNESS = 9
PARA_BRIGHTNESS = 7


class Ship(Game):
    def __init__(self, hs):
        super().__init__(hs)
        self.me = Dot(2, 4, ME_BRIGHTNESS)
        self.me.show()

        self.paras = []
        self.para_amount = 1
        self.speed = 500

        self.side_effects = [
            (10, self.change_speed, 400),
            (25, self.increase_para_amount, 1),
            (40, self.change_speed, 300),
        ]

    @staticmethod
    def get_new_para():
        return Dot(
            random.randint(0, 4),
            0,
            PARA_BRIGHTNESS
        )

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
            if para.y + 1 > 4:
                para.show(0)
                self.paras.remove(para)
                continue
            para.set(y=para.y + 1)
        while len(self.paras) < self.para_amount:
            if any([p.y in [0, 1] for p in self.paras]):
                break
            self.paras.append(self.get_new_para())
            self.paras[-1].show()

    def handle_button_presses(self):
        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll(self.hs_val)

        presses = button_a.get_presses()
        if presses:
            self.me.set(
                x=(self.me.x - presses) if (self.me.x - presses) >= 0 else 4,
                b=ME_BRIGHTNESS,
            )

        presses = button_b.get_presses()
        if presses:
            self.me.set(
                x=(self.me.x + presses) if (self.me.x + presses) <= 4 else 0,
                b=ME_BRIGHTNESS,
            )

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
        valid = True
        while True:
            self.handle_button_presses()
            if utime.ticks_diff(utime.ticks_ms(), start) > self.speed:
                if not valid and not self.validate():
                    break
                self.handle_paras()
                start = utime.ticks_ms()
                valid = self.validate()

    def run(self):
        self._run()
        if self.score > self.hs_val:
            self.hs.set(self.score)
            display.scroll("1ST")
        self.print_ints(self.score, loop=True)


hs = HS()
game = Ship(hs)
game.run()
