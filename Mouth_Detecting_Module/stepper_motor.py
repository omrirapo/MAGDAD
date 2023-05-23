import typing
from typing import Callable

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO

DELAY = 0.00324
CW = 1
CCW = 0


class StepperMotor:
    def __init__(self, DIR: int, STEP: int, steps_per_rotation: int, circ: float = None):
        """

        :param DIR:
        :param STEP:
        :param steps_per_rotation:
        :param circ:
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CCW)

        self._DIR = DIR
        self._STEP = STEP
        self._steps_per_rotation = steps_per_rotation
        self._circ = circ
        self.angle = 0

    def step(self):
        """

        :return:
        """
        GPIO.output(self._STEP, GPIO.HIGH)
        sleep(DELAY)
        GPIO.output(self._STEP, GPIO.LOW)
        sleep(DELAY)

    def move_to_angle(self, new_angle):
        """

        :param new_angle:
        :return:
        """
        rotations = (new_angle - self.angle) / 360
        steps = round(self._steps_per_rotation * rotations)
        if rotations > 0:
            GPIO.output(self._DIR, CW)

        else:
            GPIO.output(self._DIR, CCW)
            steps *= -1
        for i in range(steps):
            self.step()

        self.angle = new_angle

    def get_angle(self):
        """

        :return:
        """
        return self.angle

    def move_to_x(self, new_x):
        """

        :param new_x:
        :return:
        """
        if self._circ is None:
            raise Exception("radius is None")
        self.move_to_angle(360 * ((new_x - self.get_x()) / self._circ))

    def get_x(self):
        """

        :return:
        """
        if self._circ is None:
            raise Exception("radius is None")
        return self.angle / 360 * self._circ
