import asyncio
import time


class Acceleration(object):
    def __init__(self, initial_speed, target_speed, acceleration_time, loop):
        start_time = time.time()
        self.total_time = acceleration_time
        self.end_time = start_time + acceleration_time
        self.initial_speed = initial_speed
        self.speed_delta = target_speed - initial_speed
        self.canceled = False
        self.done_future = loop.create_future()
        update_task = asyncio.ensure_future(self.update())

    def get_current_speed(self):
        current_time = time.time()
        current_progress = 1 - (self.end_time - current_time) / self.total_time
        current_progress = max(min(1.0, current_progress), 0.0)
        return self.initial_speed + current_progress * self.speed_delta

    def is_done(self):
        return time.time() > self.end_time

    async def wait_until_done(self):
        await self.done_future

    async def update(self):
        while True:
            if self.canceled:
                break

            if self.is_done():
                self.done_future.set_result(True)
                break

            await asyncio.sleep(0)

    def cancel(self):
        self.canceled = True

        if self.done_future:
            self.done_future.cancel()
