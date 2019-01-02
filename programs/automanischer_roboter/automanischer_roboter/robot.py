import random
import sys
import asyncio
import atexit

from ev3dev2.motor import OUTPUT_C, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sound import Sound

from programs.automanischer_roboter.automanischer_roboter.robot_locomotion import RobotLocomotion
from programs.automanischer_roboter.automanischer_roboter.thrower import Thrower
from programs.automanischer_roboter.automanischer_roboter.touchy_arm import TouchyArm


class Robot(object):
    def __init__(self):
        self.locomotion = RobotLocomotion(OUTPUT_C, OUTPUT_B)
        self.eyes = UltrasonicSensor(INPUT_1)
        self.should_run = True
        self.wink_arm = TouchyArm(OUTPUT_A, INPUT_4)
        self.throw_arm = Thrower(OUTPUT_D)
        self.has_ball = True
        self.voice = Sound()
        atexit.register(self.reset)
        self.reset()

    def reset(self):
        self.locomotion.on(0, 0)
        self.wink_arm.reset()
        self.throw_arm.reset()

    def start(self):
        print('Starting automanischer ROBOTER!')
        self.voice.play_file('programs/automanischer_roboter/sounds/automan.wav')
        sys.stdout.flush()
        self.loop()

    def stop(self):
        self.should_run = False
        self.locomotion.stop()

    def loop(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run(loop))
        loop.close()

    async def run(self, loop):
        start_task = asyncio.ensure_future(self.handle_start(loop))
        distance_task = asyncio.ensure_future(self.keep_distance(loop))

        while self.should_run:
            self.locomotion.update()
            await asyncio.sleep(0)

        await start_task
        await distance_task

    async def keep_distance(self, loop):
        try:
            while self.should_run:
                if self.eyes.distance_centimeters < 50:
                    await self.back_off(loop)
                    if self.has_ball:
                        await self.attack(loop)
                    else:
                        await self.reload(loop)
                    start_task = asyncio.ensure_future(self.handle_start(loop))

                await asyncio.sleep(0)
        except Exception as e:
            print('Failed keeping distance with message')
            print(str(e))

    async def back_off(self, loop):
        self.voice.play_file('programs/automanischer_roboter/sounds/R2D2c.wav',
                             play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.locomotion.cancel_acceleration()
        await self.locomotion.accelerate(0, -30, 2, loop)
        await asyncio.sleep(2)
        await self.locomotion.accelerate(0, 0, 1, loop)
        await asyncio.sleep(1)

    async def reload(self, loop):
        self.voice.play_file('programs/automanischer_roboter/sounds/R2D2a.wav',
                             play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        self.throw_arm.reset()
        await asyncio.sleep(1)
        winking_task = asyncio.ensure_future(self.wink_arm.winking())
        await self.wink_arm.wait_until_pressed()
        self.wink_arm.stop_winking()
        self.has_ball = True
        await asyncio.sleep(1.5)

    async def attack(self, loop):
        if random.random() > 0.5:
            await self.throw_when_pressed(loop)
        else:
            await self.throw_directly(loop)
        self.has_ball = False

    async def throw_directly(self, loop):
        self.wink_arm.put_down()
        await asyncio.sleep(1)
        self.voice.play_file('programs/automanischer_roboter/sounds/R2D2e.wav',
                             play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.throw_arm.throw()
        await asyncio.sleep(1)
        self.wink_arm.put_up()

    async def throw_when_pressed(self, loop):
        self.voice.play_file('programs/automanischer_roboter/sounds/R2D2e.wav',
                             play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        winking_task = asyncio.ensure_future(self.wink_arm.winking())
        await self.wink_arm.wait_until_pressed()
        self.wink_arm.stop_winking()

        self.throw_arm.throw()
        await asyncio.sleep(1)

    async def handle_start(self, loop):
        print('start accelerating')
        sys.stdout.flush()
        try:
            await self.locomotion.accelerate(0, 30, 3, loop)
            steering = random.uniform(-20, 20)
            print('steering ' + str(steering))
            self.locomotion.on(steering, 30)
        except:
            print('Start procedure canceled')

        print('done accelerating')
        sys.stdout.flush()
