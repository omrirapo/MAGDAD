import typing
from typing import Callable

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


class Motor:
    def __init__(self, GPIO: int, Anlge2ValConverter: Callable, MinSignal=0.5 / 1000, MaxSignal=2.5 / 1000):
        factory = PiGPIOFactory()
        self._servo = Servo(GPIO, min_pulse_width=MinSignal, max_pulse_width=MaxSignal, pin_factory=factory)
        self._Anlge2ValConverter = Anlge2ValConverter
        self._x = 0
        self.move(self._x)

    @property
    def Anlge2ValConverter(self):
        return self._Anlge2ValConverter

    @Anlge2ValConverter.setter
    def Anlge2ValConverter(self, value):
        self._Anlge2ValConverter = value

    @property
    def servo(self):
        return self._servo

    @servo.setter
    def servo(self, value):
        self._servo = value

    def move(self, new_x):
        pass

    def get_x(self):
        return self._x