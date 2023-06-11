import time
from time import sleep

import stepper_motor
from Motor import Motor
import RPi.GPIO as GPIO
from Arm import Arm


class Plates:

    def __init__(self, platter_mot: Motor,
                 turn_mot: stepper_motor):
        """

        :param lower_height:
        :param dx:
        :param upper_height:
        :param iner_radi: inner radius of bowl
        :param outer_radi: outer radius of bowl
        :param platter_mot: platter stepper motor obj
        :param turn_mot: turning bowls stepper motor obj
        """

        self.diag = 0
        self.cur_plate = 0  # plates 0,1,2
        self.angle_fed = [(j, [0 for i in range(24)]) for j in range(3)]  # array of angles that where fed
        self.platter_motor = platter_mot
        self.turn_motor = turn_mot
    def change_plate(self):
        """
        change the plate that is eaten from need to change implemntation to use microswitches
        :return:
        """
        self.cur_plate = (self.cur_plate + 1) % 3
        angle_to_move = 120
        if self.cur_plate == 0:
            angle_to_move = -240
        my_array = self.angle_fed[self.cur_plate]
        min_index = my_array.index(min(my_array))

        self.platter_motor.move_to_angle(angle_to_move)  # todo define the direction of the turn
        self.turn_motor.move_to_angle(15 * (min_index - self.diag))
        self.diag = min_index

    def move_changing_servo_to_angle(self, angle):
        """
        move the servo to the angle
        :param angle:
        :return:
        """
        total_time = 5
        #counter = time.pf_counter()
        num_of_steps = int(total_time / 0.02)
        distance_per_step = angle / num_of_steps
        plm = self.platter_motor
        while plm.currAngle != angle:
            plm.move_to_angle(plm.currAngle + distance_per_step)
            sleep(0.02)
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
