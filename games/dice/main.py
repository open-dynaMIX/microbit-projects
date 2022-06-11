from microbit import *
from microbit import display
from random import randint


def roll_oracle():
    rand = randint(0, 1)
    if rand == 1:
        display.show(Image.YES)
    else:
        display.show(Image.NO)


def roll_dice():
    display.show(str(randint(1, 6)))


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
    sleep(120)


animation()
while True:
    a_pressed = button_a.is_pressed()
    b_pressed = button_b.is_pressed()
    if a_pressed or b_pressed:
        animation()
        if a_pressed:
            roll_oracle()
        elif b_pressed:
            roll_dice()
        sleep(300)
    sleep(100)
