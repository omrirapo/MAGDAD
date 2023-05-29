import stepper_motor


class Plates:

    def __init__(self, lower_height, upper_height, iner_radi, outer_radi, platter_mot: stepper_motor,
                 turn_mot: stepper_motor):
        """

        :param lower_height:
        :param upper_height:
        :param iner_radi:
        :param outer_radi:
        :param platter_mot:
        :param turn_mot:
        """
        self.bottom = lower_height
        self.lip_height = upper_height
        self.iner_radi = iner_radi
        self.outer_radi = outer_radi
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

