from gpiozero import Servo
import math
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

UNITS_PER_ANGLE = 1 / 580


def move_to_angle(angle, servo: Servo):
    servo.value = UNITS_PER_ANGLE * angle


def get_wrist_angle(angle):
    return angle * 0.85 if angle >= 0 else angle * 1.15


factory = PiGPIOFactory()

arm_servo = Servo(3, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000, pin_factory=factory)
wrist_servo = Servo(2, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000, pin_factory=factory)
move_to_angle(-80, arm_servo)
move_to_angle(-60, wrist_servo)
sleep(2)
for i in range(-80, 101):
    move_to_angle(i, arm_servo)
    move_to_angle(get_wrist_angle(i), wrist_servo)
    sleep(0.01)

