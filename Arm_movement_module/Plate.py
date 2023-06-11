import time
from time import sleep

import stepper_motor
from Motor import Motor
import RPi.GPIO as GPIO
from Arm_movement_module.Arm import Arm


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
    def change_plate(self):
        """
        change the plate that is eaten from
        bowls 0 -120, 1 - 0, 2 - 120 -> ang = (curbowl-1)*120-
        :return:
        """
        self.cur_plate = (self.cur_plate + 1) % 3
        angle_to_move = (self.cur_plate-1)*120
        # find angle of bowl
        eaten = self.angle_fed[self.cur_plate]
        min_index = eaten.index(min(eaten))

        time = 5
        stps = 1e4
        self.platter_motor.move_to_angle(angle_to_move, time, stps)
        self.turn_motor.move_to_angle(15 * (min_index - self.diag))
        self.diag = min_index

    def turn_bowl(self):
        """
        turn bowl to the minimum
        :return:
        """
        my_array = self.angle_fed[self.cur_plate]
        min_index = my_array.index(min(my_array))
        self.turn_motor.move_to_angle(15 * (min_index - self.diag))
        self.diag = min_index

    def update_ate(self):
        """
        update the arrray of eaten
        :return:
        """
        self.angle_fed[self.cur_plate][self.diag] += 1

    def gather_food(self, arm: Arm):
        """

        :param arm:
        :return:
        """
        # go inside the bowl
        # move forward
        # go up while turning
        # chang amgle to paralel
        # go back a bit
        # go up
        dx = 30
        # arm.move_hand(self.dx, self.bottom, 90)
        # arm.move_hand(x=arm.get_x()+ self.iner_radi, alpha= 45)
        # arm.move_hand(y= arm.get_y()+self.lip_height,alpha= 20)
        # arm.move_hand(x=arm.get_x()-self.iner_radi,alpha= 0)
        # arm.move_hand(y= arm.get_y()+self.lip_height)
        # arm.move_hand(x=arm.get_x()-self.iner_radi,alpha= -45)
        print(arm.move_hand(0, 0, 0))
        print(arm.move_hand_by_motors_input(0, 30, 45))
        sleep(0.2)

        print(arm.move_hand_by_motors_input(0, -20, 45))
        print(arm.move_hand(-85, -180, -60))
        sleep(0.2)

        print(arm.move_hand(-30, -180, -60))
        sleep(0.2)
        print(arm.move_hand(-30, -180, -30))

        print(arm.move_hand_by_motors_input(0, arm.get_alpha1(), arm.get_alpha2()))
        print(arm.move_hand(-20, -180, -40))
        sleep(2)

        print(arm.move_hand(-10, -80, 0))
        # sleep(0.2)

        print(arm.move_hand(0, 0, 0))
if __name__ == '__main__':
    Plates(Motor(12,lambda x: x/90), None).move_changing_servo_to_angle(90)
