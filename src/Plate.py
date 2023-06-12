from time import sleep

import stepper_motor
from Arm import Arm
from Motor import Motor
from consts import *

class Plates:

    def __init__(self, platter_mot: Motor,
                 turn_mot: stepper_motor):
        """

        :param platter_mot: servo motor to switch plates
        :param turn_mot: stepper motor to tuen plates
        """

        self.diag = 0
        self.cur_plate = 0  # plates 0,1,2
        self.angle_fed = [(j, [0 for i in range(24)]) for j in range(3)]  # array of angles that where fed
        self.platter_motor = platter_mot
        self.turn_motor = turn_mot
        self.turn_motor.disable()

    def change_plate(self):
        """
        change the plate that is eaten from
        bowls 0 -120, 1 - 0, 2 - 120 -> ang = (curbowl-1)*120-
        :return:
        """
        self.cur_plate = (self.cur_plate + 1) % 3
        angle_to_move = (self.cur_plate-1)*120

        time = 1
        stps = 1000
        if self.cur_plate==0:
            time = 2
            stps = 2000

        self.platter_motor.move_to_angle(angle_to_move, time, stps)

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
