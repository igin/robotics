from ev3dev2.motor import MoveSteering, SpeedPercent

from programs.automanischer_roboter.automanischer_roboter.acceleration import Acceleration


class RobotLocomotion(MoveSteering):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.acceleration = None
        self.current_speed = 0
        self.last_steering = 0

    def update(self):
        if self.acceleration is None:
            return

        self.current_speed = self.acceleration.get_current_speed()
        current_steering = self.last_steering

        self.on(current_steering, SpeedPercent(self.current_speed))

    def cancel_acceleration(self):
        if self.acceleration is not None:
            self.acceleration.cancel()

    async def accelerate(self, steering, target_speed, acceleration_time, loop=None):
        self.last_steering = steering
        self.acceleration = Acceleration(
            initial_speed=self.current_speed,
            target_speed=target_speed,
            acceleration_time=acceleration_time,
            loop=loop
        )

        await self.acceleration.wait_until_done()
        self.acceleration = None

    def is_accelerating(self):
        return self.acceleration is not None

    def stop(self, motors=None):
        super().stop()
        self.acceleration = None
