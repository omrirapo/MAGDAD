import math

from Motor import Motor
from stepper_motor import StepperMotor
from time import sleep
from math import cos, sin

MOVE_TIME = 0.001


def _angle_to_radians(*angles):
    if len(angles) == 1:
        return angles[0] * math.pi / 180
    return tuple([angle * math.pi / 180 for angle in angles])


def _radians_to_angle(*radians):
    if len(radians) == 1:
        return radians[0] * 180 / math.pi
    return tuple([radian * 180 / math.pi for radian in radians])


class Arm:

    def __init__(self, wrist_motor: Motor, arm_motor: Motor, shoulder_motor: StepperMotor, d: float, r: float):
        self._WristMotor = wrist_motor
        self._ArmMotor = arm_motor
        self._ShoulderMotor = shoulder_motor
        self.d = d
        self.r = r

    def _coordinates_to_motor_input(self, x: float, y: float, alpha: float):
        x += self.d + self.r
        alpha = _angle_to_radians(alpha)
        alpha1 = math.asin((y - self.d * math.sin(alpha)) / self.r)
        alpha2 = (alpha1 - alpha)
        l = x - self.r * math.cos(alpha1 / 2) - self.d * math.sin(alpha / 2)
        alpha1, alpha2 = _radians_to_angle(alpha1, alpha2)
        return l, alpha1, alpha2

    def _motor_input_to_coordinates(self, l: float, alpha1: float, alpha2: float):
        l -= self.d + self.r
        alpha1, alpha2 = _angle_to_radians(alpha1, alpha2)
        x = l + self.r * math.cos(alpha1) + self.d * math.cos(alpha1 - alpha2)
        y = self.r * math.sin(alpha1) + self.d * math.sin(alpha1 - alpha2)
        alpha = alpha1 - alpha2
        alpha = _radians_to_angle(alpha)
        return x, y, alpha

    def move_hand_by_motors_input(self, l: float, alpha1: float, alpha2: float):

        curr_arm_angle = self._ArmMotor.currAngle
        curr_wrist_angle = self._WristMotor.currAngle
        # curr_shoulder_position = self._ShoulderMotor.get_x()
        num_of_steps = 10
        for i in range(1, num_of_steps + 1):
            new_arm_angle = curr_arm_angle + i * (alpha1 - curr_arm_angle) / num_of_steps
            new_wrist_angle = curr_wrist_angle + i * (alpha2 - curr_wrist_angle) / num_of_steps
            # new_shoulder_position = curr_shoulder_position + i * (l - curr_shoulder_position) / num_of_steps
            if not self._ArmMotor.move_to_angle(new_arm_angle):
                return False
            if not self._WristMotor.move_to_angle(new_wrist_angle):
                return False
            # if not self._ShoulderMotor.move_to_x(new_shoulder_position):
            #   return False
            sleep(MOVE_TIME)
        return True

    def move_hand(self, x: float, y: float, alpha: float):
        return self.move_hand_by_motors_input(*self._coordinates_to_motor_input(x, y, alpha))

    def is_coordinates_possible(self, x: float, y: float, alpha: float):
        l, alpha1, alpha2 = self._coordinates_to_motor_input(x, y, alpha)
        return self._ArmMotor.is_angle_possible(alpha1) and self._WristMotor.is_angle_possible(
            alpha2)  # TODO add shoulder

    def move_hand_in_angle_range(self, x: float, y: float, min_alpha: float, max_alpha: float,
                                 ideal_alpha: float = None):
        if ideal_alpha is None:
            ideal_alpha = (min_alpha+max_alpha)/2
        dist = int(max(abs(ideal_alpha - min_alpha), abs(ideal_alpha - max_alpha)))
        for i in range(dist):
            alpha = ideal_alpha + i * (max_alpha - ideal_alpha) / dist
            if self.is_coordinates_possible(x, y, alpha):
                self.move_hand(x, y, alpha)
                return True
            alpha = ideal_alpha + i * (min_alpha - ideal_alpha) / dist
            if self.is_coordinates_possible(x, y, alpha):
                self.move_hand(x, y, alpha)
                return True
        return False

    def get_coordinates(self):
        return self._motor_input_to_coordinates(self._ArmMotor.currAngle, self._WristMotor.currAngle,
                                                self._ShoulderMotor.get_x())

    def get_mouth_distance(self):
        pass

    def get_x(self):
        return self.get_coordinates()[0]

    def get_y(self):
        return self.get_coordinates()[1]

    def get_alpha(self):
        return self.get_coordinates()[2]

    def get_alpha1(self):
        return self._ArmMotor.currAngle

    def get_alpha2(self):
        return self._WristMotor.currAngle

    def move_forward(self):
        pass

    def move_backward(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass


if __name__ == '__main__':
    arm_motor = Motor(17, lambda alpha: alpha / 90)
    wrist_motor = Motor(18, lambda alpha: alpha / 90)
    shoulder_motor = None
    arm = Arm(arm_motor, wrist_motor, shoulder_motor, 89.142, 129.5)
    print(arm._coordinates_to_motor_input(10, 10, 90))
    #
