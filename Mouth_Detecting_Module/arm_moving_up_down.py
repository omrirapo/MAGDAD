# from gpiozero import Servo
# import math
# from time import sleep
#
# from gpiozero.pins.pigpio import PiGPIOFactory
#
# UNITS_PER_ANGLE = 1 / 580
# MOVE_TIME = 0.01
#
#
# def move_to_angle(angle, servo: Servo):
#     curr_angle = servo.value / UNITS_PER_ANGLE
#     servo.value = UNITS_PER_ANGLE * angle
#
#
# def move_synchronize(arm_servo: Servo, wrist_servo: Servo, arm_angle, wrist_angle):
#     curr_arm_angle = arm_servo.value / UNITS_PER_ANGLE
#     curr_wrist_angle = wrist_servo.value / UNITS_PER_ANGLE
#     num_of_steps = math.sqrt(abs((arm_angle - curr_arm_angle) * (wrist_angle - curr_wrist_angle)))
#     for i in range(num_of_steps):
#         new_arm_angle = curr_arm_angle + i * (arm_angle - curr_arm_angle) / num_of_steps
#         new_wrist_angle = curr_wrist_angle + i * (wrist_angle - curr_wrist_angle) / num_of_steps
#
#         move_to_angle(new_arm_angle, arm_servo)
#         move_to_angle(get_wrist_angle(new_wrist_angle), wrist_servo)
#         sleep(MOVE_TIME)
#
#
# def get_wrist_angle(angle):
#     return angle * 0.85 if angle >= 0 else angle * 1.15
#
#
# if __name__ == '__main__':
#     factory = PiGPIOFactory()
#
#     arm_servo = Servo(3, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000, pin_factory=factory)
#     wrist_servo = Servo(2, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000, pin_factory=factory)
#     move_to_angle(-80, arm_servo)
#     move_to_angle(-60, wrist_servo)
#     sleep(2)
#     for i in range(-80, 101):
#         move_to_angle(i, arm_servo)
#         move_to_angle(get_wrist_angle(i), wrist_servo)
#         sleep(0.01)