import math

from Motor import Motor
from stepper_motor import StepperMotor
from time import sleep
from consts import MAX_X


def _angle_to_radians(*angles):
    """

    :param angles: a number of angles in degrees
    :return: the same angles in radians in a tuple, if from size 1, returns a number
    """
    if len(angles) == 1:
        return angles[0] * math.pi / 180
    return tuple([angle * math.pi / 180 for angle in angles])


def _radians_to_angle(*radians):
    """

    :param radians: a number of radians
    :return: the same angles in degrees in a tuple, if from size 1, returns a number
    """
    if len(radians) == 1:
        return radians[0] * 180 / math.pi
    return tuple([radian * 180 / math.pi for radian in radians])


class Arm:

    def __init__(self, wrist_motor: Motor, arm_motor: Motor, shoulder_motor: StepperMotor, forearm: float,
                 bicep: float):
        """

        :param wrist_motor: the motor that moves the wrist as a Motor object
        :param arm_motor: the motor that moves the arm as a Motor object
        :param shoulder_motor: the stepper motor that moves the arm forward and backward as a StepperMotor object
        :param forearm: the distance from the wrist to the end of the spoon in millimeters
        :param bicep: the distance from the elbow to the wrist in millimeters
        """
        self._WristMotor = wrist_motor
        self._ArmMotor = arm_motor
        self._ShoulderMotor = shoulder_motor
        self.forearm = forearm
        self.bicep = bicep
        self.disable_shoulder()

    def _coordinates_to_motor_input(self, x: float, y: float, alpha: float):
        """

        :param x: the x coordinate of the spoon in millimeters
        :param y: the y coordinate of the spoon in millimeters
        :param alpha: the angle of the spoon in angles
        :return: the motor input needed to get to the given coordinates
        """
        alpha = _angle_to_radians(alpha)
        alpha1 = math.asin((y - self.forearm * math.sin(alpha)) / self.bicep)
        alpha2 = (alpha1 - alpha)
        l = x + self.forearm + self.bicep - self.bicep * math.cos(alpha1) - self.forearm * math.cos(alpha)
        alpha1, alpha2 = _radians_to_angle(alpha1, alpha2)
        return l, alpha1, alpha2

    def _motor_input_to_coordinates(self, l: float, alpha1: float, alpha2: float):
        """

        :param l: the distance that the arm is extended in millimeters(the distance that the shoulder motor moved)
        :param alpha1: the angle of the arm in angles
        :param alpha2: the angle of the wrist in angles
        :return: the coordinates of the spoon
        """
        l -= self.forearm + self.bicep
        alpha1, alpha2 = _angle_to_radians(alpha1, alpha2)
        x = l + self.bicep * math.cos(alpha1) + self.forearm * math.cos(alpha1 - alpha2)
        y = self.bicep * math.sin(alpha1) + self.forearm * math.sin(alpha1 - alpha2)
        alpha = alpha1 - alpha2
        alpha = _radians_to_angle(alpha)
        return x, y, alpha

    def move_to_minimal_x(self):
        # todo change this so it moves back till it touches the microswitch and then resets the 0. and add a timeout.
        self._ShoulderMotor.move_to_x(0)

    def move_hand_by_motors_input(self, l: float, alpha1: float, alpha2: float, wait_between_steps=0.001):
        """
        moves the hand to the given coordinates, moves all the motors accordingly
        :param l: the distance that the arm is extended(the distance that the shoulder motor moved) in millimeters
        :param alpha1: the angle of the arm motor in angles
        :param alpha2: the angle of the wrist motor in angles
        :param wait_between_steps: the time to wait between each step in seconds
        :return: current coordinates after move
        """
        l = max(min(MAX_X, l), 0)  # make sure l is between 0 and MAX_X

        curr_arm_angle = self._ArmMotor.currAngle
        curr_wrist_angle = self._WristMotor.currAngle
        curr_shoulder_position = self._ShoulderMotor.get_x()
        num_of_steps = int((abs(curr_wrist_angle - alpha1)) + int(abs(curr_wrist_angle - alpha2))) + int(abs(
            curr_shoulder_position - l))
        for i in range(1, num_of_steps):
            new_arm_angle = curr_arm_angle + (alpha1 - curr_arm_angle) * (i / num_of_steps)
            new_wrist_angle = curr_wrist_angle + (alpha2 - curr_wrist_angle) * (i / num_of_steps)
            new_shoulder_position = curr_shoulder_position + (l - curr_shoulder_position) * (i / num_of_steps)
            if not self._ArmMotor.move_to_angle(new_arm_angle):
                return False
            if not self._WristMotor.move_to_angle(new_wrist_angle):
                return False
            if new_shoulder_position < 0:
                return False
            self._ShoulderMotor.move_to_x(new_shoulder_position)
            sleep(wait_between_steps)
        if not self._ArmMotor.move_to_angle(alpha1):
            return False
        if not self._WristMotor.move_to_angle(alpha2):
            return False
        if l < 0:  # not relevant.
            return False
        self._ShoulderMotor.move_to_x(l)
        return self.get_coordinates()

    def move_hand_by_angles(self, alpha1: float, alpha2: float, wait_between_steps=0.001):
        """
        moves the hand to the given angles, the shoulder motor will not move
        :param alpha1: the angle of the arm motor in angles
        :param alpha2: the angle of the wrist motor in angles
        :param wait_between_steps: the time to wait between each step in seconds
        :return: the coordinates at the end with True or False
        """
        curr_arm_angle = self._ArmMotor.currAngle
        curr_wrist_angle = self._WristMotor.currAngle
        num_of_steps = 10
        for i in range(1, num_of_steps + 1):
            new_arm_angle = curr_arm_angle + i * (alpha1 - curr_arm_angle) / num_of_steps
            new_wrist_angle = curr_wrist_angle + i * (alpha2 - curr_wrist_angle) / num_of_steps
            if not self._ArmMotor.move_to_angle(new_arm_angle):
                return self.get_coordinates(), False
            if not self._WristMotor.move_to_angle(new_wrist_angle):
                return self.get_coordinates(), False
            sleep(wait_between_steps)
        return self.get_coordinates(), True

    def move_hand(self, x: float = None, y: float = None, alpha: float = None, wait_between_steps=0.001):
        """
        moves the hand to the given coordinates, moves all the motors accordingly, defines the 0 of the coordinate
         to be the end of the spoon when the arm is straight
        :param wait_between_steps:
        :param x: the x coordinate of the spoon in millimeters
        :param y: the y coordinate of the spoon in millimeters
        :param alpha: the angle of the spoon in angles, positive means pointing up
        :param wait_between_steps: the time to wait between each step in seconds
        :return: True if moved successfully, false otherwise
        """
        if x is None:
            x = self.get_x()
        if y is None:
            y = self.get_y()
        if alpha is None:
            alpha = self.get_alpha()
        # print(
        #     f"l = {self._coordinates_to_motor_input(x, y, alpha)[0]}, alpha1 = {self._coordinates_to_motor_input(x, y, alpha)[1]}, alpha2 = {self._coordinates_to_motor_input(x, y, alpha)[2]}")
        if not self.move_hand_by_motors_input(*self._coordinates_to_motor_input(x, y, alpha), wait_between_steps):
            print(f"failed to move hand while trying to move to coordinates {x,y,alpha}, instead moved to {self.get_coordinates()}")
            return False
        return self.get_coordinates()

    def is_coordinates_possible(self, x: float, y: float, alpha: float):
        """

        :param x: the x coordinate in millimeters
        :param y: the y coordinate in millimeters
        :param alpha: the angle of the spoon in angles
        :return: True if it is possible to move the arm to coordinates without Failing, False otherwise
        """
        l, alpha1, alpha2 = self._coordinates_to_motor_input(x, y, alpha)
        return self._ArmMotor.is_angle_possible(alpha1) and self._WristMotor.is_angle_possible(
            alpha2) and l > 0

    def move_hand_in_angle_range(self, x: float, y: float, min_alpha: float, max_alpha: float,
                                 ideal_alpha: float = None):
        """
        simulates a move to x,y in the range min_alpha to max_alpha. tries to find the angle that is closet to ideal_alpha
        :param x: the x coordinate in millimeters
        :param y: the y coordinate in millimeters
        :param min_alpha: in angles
        :param max_alpha: in angles
        :param ideal_alpha: the angle that would be tried first, would choose the angle that is closest to ideal_alpha
        :return: returns True if found an angle in the range that is possible to move to, False otherwise
        """
        if ideal_alpha is None:
            ideal_alpha = (min_alpha + max_alpha) / 2
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
        """

        :return: a tuple of (x,y, alpha) when x is the x coordinate, y is the y coordinate and alpha is the angle,
        all of the spoon relative to starting pos.
        """
        return self._motor_input_to_coordinates(self._ShoulderMotor.get_x(),self._ArmMotor.currAngle, self._WristMotor.currAngle)

    def get_x(self):
        """

        :return: the x coordinate in millimeters
        """
        return self.get_coordinates()[0]

    def get_y(self):
        """

        :return: the y coordinate in millimeters
        """
        return self.get_coordinates()[1]

    def get_alpha(self):
        """

        :return: the angle of the spoon in angles
        """
        return self.get_coordinates()[2]

    def get_l(self):
        """

        :return: the length of the arm in millimeters
        """
        return self._ShoulderMotor.get_x()

    def get_alpha1(self):
        """

        :return: the angle of the arm motor in angles
        """
        return self._ArmMotor.currAngle

    def get_alpha2(self):
        """

        :return:  the angle of the wrist motor in angles
        """
        return self._WristMotor.currAngle

    def move_forward(self, dist):
        """

        :param dist: distance to travel
        :param time: time to travel it
        """
        self._ShoulderMotor.move_to_x(dist + self._ShoulderMotor.get_x())

    def move_backward(self, dist):
        """

        :param dist: distance to travel
        :param time: time to travel it
        """
        self.move_forward(-dist)

    def move_up_deg(self, dist):
        """

        :param dist: distance to travel
        :param time: time to travel it
        """
        self.move_hand_by_motors_input(self._ShoulderMotor.get_x(), self.get_alpha1() + dist, self.get_alpha1() + dist)

    def move_up(self, dist):
        """

        :param dist: distance to travel
        :param time: time to travel it
        """
        x, y, alpha = self.get_coordinates()
        _, alpha1, alpha2 = self._coordinates_to_motor_input(x, y + dist, alpha)
        self.move_hand_by_motors_input(self._ShoulderMotor.get_x(), alpha1, alpha2)

    def move_down(self, dist):
        """

        :param dist: distance to travel
        :param time: time to travel it
        """
        self.move_up(-dist)

    def hover_angle(self, angle):
        """
        changes the angle of the spoon without changing the x and y coordinates
        :param angle: angle to get to
        """
        self.move_hand(self.get_x(), self.get_y(), angle)

    def disable_shoulder(self):
        """
        disables the shoulder motor uses stepper_motor.disable
        :return:
        """
        self._ShoulderMotor.disable()

    def enable_shoulder(self):
        """
        enables the shoulder motor uses stepper_motor.enable
        :return:
        """
        self._ShoulderMotor.enable()
