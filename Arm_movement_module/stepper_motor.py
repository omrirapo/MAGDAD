import typing
from typing import Callable

#from gpiozero import Servo
#from gpiozero.pins.pigpio import PiGPIOFactory


class StepperMotor:
    def __init__(self, GPIO: int, steps_per_rotation: int, radius: int = None):
        self._steps_per_rotation = steps_per_rotation
        self._radius = radius
        self.angle = 0

    def move_to_angle(self, new_angle):
        self.angle = new_angle

    def get_angle(self):
        return self.angle

    def move_to_x(self, new_x):
        if self._radius is None:
            raise Exception("radius is None")
        self.angle = new_x / self._radius

    def get_x(self):
        if self._radius is None:
            raise Exception("radius is None")
        return self.angle * self._radius
