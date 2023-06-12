from time import sleep
from typing import Callable

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


class Motor:

    def __init__(self, GPIO: int, Anlge2ValConverter: Callable, MinSignal=0.5 / 1000, MaxSignal=2.5 / 1000):
        """
        a Class that represents a servo motor
        :param GPIO: the GPIO pin number
        :param Anlge2ValConverter: a function that converts an angle to a value between -1 and 1
        :param MinSignal: the minimum signal the servo can get, you can find it in the servo's datasheet
        :param MaxSignal: the maximum signal the servo can get, you can find it in the servo's datasheet
        """
        factory = PiGPIOFactory()
        self._servo = Servo(GPIO, min_pulse_width=MinSignal, max_pulse_width=MaxSignal, pin_factory=factory)
        self._Anlge2ValConverter = Anlge2ValConverter
        self.currAngle = 0
        self.move_to_angle(0)

    @property
    def Anlge2ValConverter(self):
        """

        :return: the function that converts an angle to a value between -1 and 1
        """
        return self._Anlge2ValConverter

    @Anlge2ValConverter.setter
    def Anlge2ValConverter(self, value):
        """
        change the function that converts an angle to a value between -1 and 1
        :param value: the function that converts an angle to a value between -1 and 1
        """
        self._Anlge2ValConverter = value

    @property
    def servo(self):
        """

        :return: the servo object
        """
        return self._servo

    @servo.setter
    def servo(self, value):
        """
        change the servo object
        :param value: the servo object
        """
        self._servo = value

    def move_to_angle(self, new_angle, time=None, stps=1000):
        """
        move the servo to a new angle, updates curr_angle
        :param new_angle: the new angle to move to in degrees
        :param time : time to turn
        :param stps: stps to turn with
        :return: if the angle is possible to move to
        """
        stps = int(stps)
        if time:
            dest = self._Anlge2ValConverter(new_angle)
            diff = (dest - self._Anlge2ValConverter(self.currAngle)) / stps
            angles = [self._Anlge2ValConverter(self.currAngle) + i * diff for i in range(stps + 1)]
            for ang in angles:
                self._servo.value = ang
                sleep(time / stps)
                self.currAngle = ang
            
            return True
        elif -1 <= self._Anlge2ValConverter(new_angle) <= 1:
            self._servo.value = self._Anlge2ValConverter(new_angle)
            self.currAngle = new_angle
            # print(f"curr angle = {new_angle}, value = {self._servo.value}")
            return True
        else:
            return False

    def is_angle_possible(self, new_angle):
        """
        check if the angle is possible to move to
        :param new_angle: the new angle to move to in degrees
        :return: is the angle possible to move to
        """
        return -1 <= self._Anlge2ValConverter(new_angle) <= 1

    def get_angle(self):
        """

        :return: the current angle of the servo in degrees
        """
        return self.currAngle
