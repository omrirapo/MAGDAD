import Arm_movement_module.Arm


def gather_food(arm: Arm):
    """

    :param arm:
    :return:
    """
    arm.move_hand(0, 0, 0)
    arm.move_hand_by_motors_input(0, 30, 45)
    sleep(0.2)

    arm.move_hand_by_motors_input(0, -20, 45)
    arm.move_hand(-85, -180, -60)
    sleep(0.2)

    arm.move_hand(-30, -180, -60)
    sleep(0.2)
    arm.move_hand(-30, -180, -30)

    arm.move_hand_by_motors_input(0, arm.get_alpha1(), arm.get_alpha2())
    arm.move_hand(-20, -180, -40)
    sleep(.2)

    arm.move_hand(-10, -80, 0)
    # sleep(0.2)
    arm.move_hand(0, 0, 0)