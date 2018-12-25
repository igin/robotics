import time

from ev3dev2.motor import SpeedPercent


def accelerate(tank, start_speed_percentage, target_speed_percentage, acceleration_time):
    start_time = time.time()
    end_time = start_time + acceleration_time

    speed_percentage_difference = target_speed_percentage - start_speed_percentage

    while True:
        current_time = time.time()
        if current_time > end_time:
            break

        interpolator = 1 - (end_time - current_time) / acceleration_time
        current_speed_percent = start_speed_percentage + speed_percentage_difference * interpolator

        print(current_speed_percent)
        current_speed = SpeedPercent(current_speed_percent)
        tank.on(current_speed, current_speed)
