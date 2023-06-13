import time
from time import sleep

import RPi.GPIO as GPIO

from consts import STEP_DELAY

CW = 1
CCW = 0


class StepperMotor:
    def __init__(self, DIR: int, STEP: int, ENABLE, steps_per_rotation: int, mm_per_angle: float = None,
                 ms_arr=tuple()):
        """

        :param DIR: a gpio PIN that is connected to the DIR pin of the stepper motor, tells the motor to move CW or CCW
        :param STEP: a gpio PIN that is connected to the STEP pin of the stepper motor, tells the motor to move one step
        :param steps_per_rotation: the number of steps the motor needs to do to make a full rotation
        :param mm_per_angle: the amount of millimeters the motor needs to move to make a 1 degree rotation
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(ENABLE, GPIO.OUT)
        GPIO.output(DIR, CCW)

        self._DIR = DIR
        self._STEP = STEP
        self._ENABLE = ENABLE
        self._steps_per_rotation = steps_per_rotation
        self._millis_per_angle = mm_per_angle
        self.angle = 0
        self._speed = 0
        self.wait_per_step = None
        self.micro_switches = ms_arr
        for i, s in ms_arr:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def step(self):
        """

        does one step
        """
        GPIO.output(self._STEP, GPIO.HIGH)
        sleep(STEP_DELAY)
        GPIO.output(self._STEP, GPIO.LOW)
        sleep(STEP_DELAY)

    def enable(self):
        """
        lets the motor be controlled by the step function
        :return:
        """
        GPIO.output(self._ENABLE, GPIO.LOW)

    def disable(self):
        """
        makes the motor unable to be controlled by the step function, if the motor is disabled it can be moved freely as if it was not connected to the pi
        :return:
        """
        GPIO.output(self._ENABLE, GPIO.HIGH)

    def move_to_angle(self, new_angle):
        """
        moves the motor to a new angle
        :param new_angle: the new angle to move to in degrees
        """
        rotations = (new_angle - self.angle) / 360
        # print(f"rotations: {rotations}, angle: {self.angle}, new_angle: {new_angle}")
        steps = round(self._steps_per_rotation * rotations)
        self.angle += (steps / self._steps_per_rotation) * 360
        d = 1
        if rotations > 0:
            GPIO.output(self._DIR, CW)

        else:
            GPIO.output(self._DIR, CCW)
            steps *= -1
            d = 0

        for i in range(steps):
            for ms, direction in self.micro_switches:
                if d != direction and GPIO.input(ms):
                    return False

            self.step()
        return True

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
        return self.move_to_angle((new_x / self._millis_per_angle))

    def reset_location(self):
        """
        resets the location stored to 0. this does not move the motor, only changes the stored location. for reseting the
        motor when is in the wanted 0 position.
        :return:
        """
        self._set_angle(0)

    def set_x(self, new_x):
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
