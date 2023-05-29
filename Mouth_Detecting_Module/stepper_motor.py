import typing
from typing import Callable

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import time
import math
import RPi.GPIO as GPIO

DELAY = 0.00324
CW = 1
CCW = 0


class StepperMotor:
    def __init__(self, DIR: int, STEP: int, steps_per_rotation: int, millis_per_angle: float = None):
        """

        :param DIR:
        :param STEP:
        :param steps_per_rotation:
        :param millis_per_angle:
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CCW)

        self._DIR = DIR
        self._STEP = STEP
        self._steps_per_rotation = steps_per_rotation
        self._millis_per_angle = millis_per_angle
        self.angle = 0
        self._speed = 0
        self.wait_per_step = None
        self._running_continues = False

    def _step(self):
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
            self._step()

        self.angle = new_angle

    def get_angle(self):
        return self.angle

    def move_to_x(self, new_x):
        """
        :param new_x: in millis
        """
        if self._millis_per_angle is None:
            raise Exception("millis_per_angle is None")
        self.move_to_angle(((new_x - self.get_x()) / self._millis_per_angle))

    def _set_x(self, new_x):
        if self._millis_per_angle is None:
            raise Exception("millis_per_angle is None")
        self._set_angle(((new_x - self.get_x()) / self._millis_per_angle))

    def _set_angle(self, new_angle):
        self.angle = new_angle

    def get_x(self):
        """

        :return: x in millis
        """
        if self._millis_per_angle is None:
            raise Exception("millis_per_angle is None")
        return self.angle * self._millis_per_angle

    def _dist_to_steps(self, dist):
        return round(dist * self._steps_per_rotation / (self._millis_per_angle * 360))

    def move(self, dist, duration):
        """
        move dist in duration
        :param dist: the distance in millis
        :param duration: the time to move
        """
        if dist == 0:
            return
        if duration == 0:
            self.move_to_x(self.get_x() + dist)
        num_of_steps = self._dist_to_steps(dist)
        wait_time = duration / num_of_steps
        for _ in range(num_of_steps):
            cur_time = time.time()
            self._step()
            sleep(wait_time - (time.time() - cur_time))
        self._set_x(self.get_x()+dist)
