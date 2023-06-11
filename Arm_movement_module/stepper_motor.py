import typing
from typing import Callable

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import time
import math
import RPi.GPIO as GPIO
from Control.consts import STEP_DELAY

CW = 1
CCW = 0


class StepperMotor:
    def __init__(self, DIR: int, STEP: int, steps_per_rotation: int, mm_per_angle: float = None):
        """

        :param DIR: a gpio PIN that is connected to the DIR pin of the stepper motor, tells the motor to move CW or CCW
        :param STEP: a gpio PIN that is connected to the STEP pin of the stepper motor, tells the motor to move one step
        :param steps_per_rotation: the number of steps the motor needs to do to make a full rotation
        :param mm_per_angle: the amount of millimeters the motor needs to move to make a 1 degree rotation
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CCW)

        self._DIR = DIR
        self._STEP = STEP
        self._steps_per_rotation = steps_per_rotation
        self._millis_per_angle = mm_per_angle
        self.angle = 0
        self._speed = 0
        self.wait_per_step = None
        self._running_continues = False

    def step(self):
        """

        does one step
        """
        GPIO.output(self._STEP, GPIO.HIGH)
        sleep(STEP_DELAY)
        GPIO.output(self._STEP, GPIO.LOW)
        sleep(STEP_DELAY)

    def move_to_angle(self, new_angle):
        """
        moves the motor to a new angle
        :param new_angle: the new angle to move to in degrees
        """
        rotations = (new_angle - self.angle) / 360
        #print(f"rotations: {rotations}, angle: {self.angle}, new_angle: {new_angle}")
        steps = round(self._steps_per_rotation * rotations)
        self.angle += (steps/self._steps_per_rotation)*360
        if rotations > 0:
            GPIO.output(self._DIR, CW)

        else:
            GPIO.output(self._DIR, CCW)
            steps *= -1
        for i in range(steps):
            self.step()



    def get_angle(self):
        """

        :return: the current angle of the motor in degrees
        """
        return self.angle

    def move_to_x(self, new_x):
        """
        moves the motor to a new x
        :param new_x: in millimeters
        """
        if self._millis_per_angle is None:
            raise Exception("millis_per_angle is None")
        self.move_to_angle((new_x / self._millis_per_angle))

    def reset_location(self):
        """
        resets the location stored to 0. this does not move the motor, only changes the stored location. for reseting the
        motor when is in the wanted 0 position.
        :return:
        """
        self._set_angle(0)

    def _set_x(self, new_x):
        """
        sets the x of the motor without moving it
        :param new_x: the new x in millimeters
        """
        if self._millis_per_angle is None:
            raise Exception("millis_per_angle is None")
        self._set_angle(((new_x - self.get_x()) / self._millis_per_angle))

    def _set_angle(self, new_angle):
        """
        sets the angle of the motor without moving it
        :param new_angle: the new angle in degrees
        """
        self.angle = new_angle

    def get_x(self):
        """
        the current x of the motor in millimeters
        :return: x in millis
        """
        if self._millis_per_angle is None:
            raise Exception("millis_per_angle is None")
        return self.angle * self._millis_per_angle

    def _dist_to_steps(self, dist):
        """
        converts a distance in millimeters to steps
        :param dist: the distance in millimeters
        :return: the number of steps needed to move the distance
        """
        return round(dist * self._steps_per_rotation / (self._millis_per_angle * 360))

    def move(self, dist, duration):
        """
        move dist in duration
        :param dist: the distance in millis
        :param duration: the time to move
        """
        if self._dist_to_steps(dist) == 0:
            return
        if duration == 0:
            self.move_to_x(self.get_x() + dist)
        num_of_steps = self._dist_to_steps(dist)
        wait_time = duration / num_of_steps
        for _ in range(num_of_steps):
            cur_time = time.time()
            self.step()
            sleep(wait_time - (time.time() - cur_time))
        self._set_x(self.get_x() + dist)
