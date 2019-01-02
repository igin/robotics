import asyncio
import random

from ev3dev2.motor import SpeedPercent, Motor
from ev3dev2.sensor.lego import TouchSensor


class TouchyArm(object):
    def __init__(self, output, address):
        self.motor = Motor(output)
        self.sensor = TouchSensor(address)
        self.should_wink = False

    def put_down(self):
        self.motor.on_to_position(SpeedPercent(20), 90, block=True)

    def put_up(self):
        self.motor.on_to_position(SpeedPercent(20), 0, block=True)

    def reset(self):
        self.motor.on_to_position(SpeedPercent(20), 0)

    async def winking(self):
        self.should_wink = True
        while self.should_wink:
            self.motor.on_for_degrees(SpeedPercent(100), -20, block=True)
            self.motor.on_for_degrees(SpeedPercent(50), 20, block=True)
            await asyncio.sleep(random.uniform(0.5, 2))
            self.motor.on_for_degrees(SpeedPercent(100), -20, block=True)
            self.motor.on_for_degrees(SpeedPercent(50), 20, block=True)
            await asyncio.sleep(random.uniform(2, 3))

    def stop_winking(self):
        self.should_wink = False

    async def wait_until_pressed(self):
        while True:
            if self.sensor.is_pressed:
                break

            await asyncio.sleep(0.1)
