from Arm import Arm
from time import sleep

from Plate import Plates


def gather_food(arm: Arm,platter:Plates):
    """

    :param platter:
    :param arm:
    :return:
    """
    arm.enable_shoulder()
    platter.enable_bowl_motor()
    platter.turn_bowl()
    arm.move_hand(0, 0, 0)

    arm.move_hand(-70, -163.40962324069412, -59.99999999999999)

    sleep(0.2)

    sleep(0.2)
    arm.move_hand(-30, -150, -30)
    sleep(0.2)

    arm.move_hand(-29.0646934652067, -162.99954229791467, -26.451612903225804)
    arm.move_hand(x=-15)
    platter.turn_bowl()
    sleep(.2)

    arm.move_hand(-10, -80, 0)
    sleep(0.2)
    arm.move_hand(0, 0, 0)
    platter.disable_bowl_motor()
    arm.disable_shoulder()
