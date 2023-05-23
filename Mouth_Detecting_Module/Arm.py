import math

from Motor import Motor
from stepper_motor import StepperMotor
from time import sleep
from math import cos, sin

MOVE_TIME = 0.01


class Arm:

    def __init__(self, wrist_motor: Motor, arm_motor: Motor, shoulder_motor: StepperMotor, d: float, r: float):
        """

        :param wrist_motor:
        :param arm_motor:
        :param shoulder_motor:
        :param d:
        :param r:
        """
        self._WristMotor = wrist_motor
        self._ArmMotor = arm_motor
        self._ShoulderMotor = shoulder_motor
        self.d = d
        self.r = r

    def _coordinates_to_motor_input(self, x: float, y: float, alpha: float):
        """

        :param x:
        :param y:
        :param alpha:
        :return:
        """
        alpha1 = math.asin((y - self.d * math.sin(alpha)) / self.r)
        alpha2 = alpha1 - alpha
        l = x - self.r * math.cos(alpha1) - self.d * math.sin(alpha)
        return l, alpha1, alpha2

    def _motor_input_to_coordinates(self, l: float, alpha1: float, alpha2: float):
        """

        :param l:
        :param alpha1:
        :param alpha2:
        :return:
        """
        x = l + self.r * math.cos(alpha1) + self.d * math.cos(alpha1 - alpha2)
        y = self.r * math.sin(alpha1) + self.d * math.sin(alpha1 - alpha2)
        alpha = alpha1 - alpha2
        return x, y, alpha

    def move_hand_by_motors_input(self, l: float, alpha1: float, alpha2: float):
        """
        meni you need to documebt the code
        :param l:
        :param alpha1:
        :param alpha2:
        :return:
        """
        curr_arm_angle = self._ArmMotor.currAngle
        curr_wrist_angle = self._WristMotor.currAngle
        curr_shoulder_position = self._ShoulderMotor.get_x()
        num_of_steps = int(abs((alpha1 - curr_arm_angle) * (alpha2 - curr_wrist_angle)))
        for i in range(num_of_steps):
            new_arm_angle = curr_arm_angle + i * (alpha1 - curr_arm_angle) / num_of_steps
            new_wrist_angle = curr_wrist_angle + i * (alpha2 - curr_wrist_angle) / num_of_steps
            new_shoulder_position = curr_shoulder_position + i * (l - curr_shoulder_position) / num_of_steps
            self._ArmMotor.move_to_angle(new_arm_angle)
            self._WristMotor.move_to_angle(new_wrist_angle)
            self._ShoulderMotor.move_to_x(new_shoulder_position)
            sleep(MOVE_TIME)

    def move_hand(self, x: float, y: float, alpha: float):
        """

        :param x:
        :param y:
        :param alpha:
        :return:
        """
        self.move_hand_by_motors_input(*self._coordinates_to_motor_input(x, y, alpha))

    def get_coordinates(self):
        """

        :return:
        """
        return self._motor_input_to_coordinates(self._ArmMotor.currAngle, self._WristMotor.currAngle,
                                                self._ShoulderMotor.get_x())

    def get_mouth_distance(self):
        """

        :return:
        """
        pass
    def get_x(self):
        """

        :return:
        """
        return self.get_coordinates()[0]

    def get_y(self):
        """

        :return:
        """
        return self.get_coordinates()[1]

    def get_alpha(self):
        """

        :return:
        """
        return self.get_coordinates()[2]
    def move_forward(self, speed):
        """

        :param self:
        :param: speed : fastest at 1
        :return:
        """
        pass

    def move_backward(self):
        """

        :param self:
        :return:
        """
        pass

    def move_up(self):
        """

        :param self:
        :return:
        """
        pass

    def move_down(self):
        """

        :param self:
        :return:
        """
        pass





