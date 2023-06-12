from Arm import Arm
from time import sleep

from Plate import Plates


def gather_food(arm: Arm,platter:Plates):
    """

    :param platter:
    :param arm:
    :return:
    """
    platter.enable_bowl_motor()
    platter.turn_bowl()
    arm.move_hand(0, 0, 0)
    arm.move_hand_by_motors_input(0, 30, 45)
    sleep(0.2)

    arm.move_hand_by_motors_input(0, -20, 45)
    arm.move_hand(-85, -150, -30)
    sleep(0.2)

    arm.move_hand(-30, -150, -60)
    sleep(0.2)
    arm.move_hand(-30, -150, -30)

    #arm.move_hand_by_motors_input(0, arm.get_alpha1(), arm.get_alpha2())
    arm.move_hand(-30, -150, -20)
    #platter.turn_bowl()
    sleep(.2)

    #arm.move_hand(-10, -80, 0)
    # sleep(0.2)
    #arm.move_hand(0, 0, 0)
    platter.disable_bowl_motor()
