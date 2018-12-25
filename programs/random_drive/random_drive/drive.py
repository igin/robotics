#!/usr/bin/env python3
import random
import signal
import sys
import time

from ev3dev2.motor import SpeedPercent, OUTPUT_B, OUTPUT_C, MoveTank, MoveSteering


def drive():
    tank = MoveTank(OUTPUT_C, OUTPUT_B)
    tank_steering = MoveSteering(OUTPUT_C, OUTPUT_B)

    def signal_handler(sig, frame):
        stop(tank)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    random_walk(tank_steering, 10)
    stop(tank)


def random_walk(tank_steering, walking_time):
    start_time = time.time()
    end_time = start_time + walking_time
    while True:
        current_time = time.time()
        if current_time > end_time:
            break

        steering = random.uniform(-1, 1) * 50
        speed = SpeedPercent(random.uniform(0.3, 1) * 100)

        tank_steering.on(steering, speed)

        time.sleep(1)


def stop(tank):
    tank.on(0, 0)
