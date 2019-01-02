#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, SpeedPercent
from ev3dev2.sound import Sound


def start():
    print('Start minimal example')

    motor = Motor(OUTPUT_A)
    motor.on_for_seconds(SpeedPercent(50), 2)

    sound = Sound()
    sound.play_file('/home/robot/programs/minimal_example/R2D2a.wav')


if __name__ == '__main__':
    start()
