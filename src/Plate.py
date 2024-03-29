import logging
from time import sleep

import stepper_motor
from Arm import Arm
from Motor import Motor
from consts import *
import RPi.GPIO as GPIO

class Plates:

    def __init__(self, platter_mot: Motor,
                 turn_mot: stepper_motor, arm: Arm, initial_plate: int = 0, cb_arr=tuple()):
        """

        :param platter_mot: servo motor to switch plates
        :param turn_mot: stepper motor to tuen plates
        """

        self.diag = 0
        self.cur_plate = initial_plate  # plates 0,1,2
        self.angle_fed = [(j, [0 for i in range(24)]) for j in range(3)]  # array of angles that where fed
        self.platter_motor = platter_mot
        self.turn_motor = turn_mot
        self.turn_motor.disable()
        self.arm = arm
        self.control_buttons = cb_arr
        for i in cb_arr:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def change_plate(self):
        """
        change the plate that is eaten from
        bowls 0 -120, 1 - 0, 2 - 120 -> ang = (curbowl-1)*120-
        :return:
        """
        self.arm.move_hand(0, 0, 0)
        sleep(1)
        self.cur_plate = (self.cur_plate + 1) % 3
        angle_to_move = (self.cur_plate - 1) * 120

        time = 1
        stps = 1000
        if self.cur_plate == 0:
            time = 2
            stps = 2000

        self.platter_motor.move_to_angle(angle_to_move, time, stps)
        initial_plate_file = open(initial_plate_path, 'w')
        initial_plate_file.write(str(self.cur_plate))

    def turn_bowl(self):
        """
        turn bowl to the minimum
        :return:
        """
        self.turn_motor.move_to_angle(self.turn_motor.get_angle() + DEG_PER_BOWL_TURN)

    def update_ate(self):
        """
        update the arrray of eaten
        :return:
        """
        self.angle_fed[self.cur_plate][self.diag] += 1

    def disable_bowl_motor(self):
        """
        disable the bowl motor uses stepper_motor.disable_motor()
        :return:
        """
        self.turn_motor.disable()

    def enable_bowl_motor(self):
        """
        enables the shoulder motor uses stepper_motor.enable
        :return:
        """
        self.turn_motor.enable()

    def go_to_start(self):
        if self.cur_plate == 0:
            return
        time = 1
        stps = 1000
        self.platter_motor.move_to_angle(0, time, stps)
