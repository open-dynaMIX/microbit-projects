from microbit import *
from microbit import display
from random import randint


def roll():
    rand = randint(0, 1)
    if rand == 1:
        display.show(Image.YES)
    else:
        display.show(Image.NO)


def animation():
    frames = [
        Image("00000:" "00000:" "00900:" "00000:" "00000"),
        Image("00000:" "00900:" "09090:" "00900:" "00000"),
        Image("00900:" "09090:" "90009:" "09090:" "00900"),
        Image("09090:" "90009:" "00000:" "90009:" "09090"),
        Image("90009:" "00000:" "00000:" "00000:" "90009"),
        Image("00000:" "00000:" "00000:" "00000:" "00000"),
    ]

    for f in frames:
        display.show(f)
        sleep(100)
    sleep(150)


animation()
while True:
    if button_a.is_pressed() and button_b.is_pressed():
        animation()
        roll()
        sleep(500)
    sleep(100)
