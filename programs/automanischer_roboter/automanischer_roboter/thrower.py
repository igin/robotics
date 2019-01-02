from ev3dev2.motor import SpeedPercent, Motor


class Thrower(object):
    def __init__(self, output):
        self.motor = Motor(output)

    def throw(self):
        self.motor.on_to_position(SpeedPercent(100), 50)

    def reset(self):
        self.motor.on_to_position(SpeedPercent(20), 0, block=False)
