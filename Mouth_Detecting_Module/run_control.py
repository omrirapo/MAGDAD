from Arm import Arm
from Motor import Motor
from stepper_motor import StepperMotor
from pid import PID
from only_mouth import mouthing
from time import sleep
import pickle


def orient(name="user", cam_height=0):
    arm_motor = Motor(17, lambda alpha: alpha / 90)
    wrist_motor = Motor(18, lambda alpha: alpha / 90)
    shoulder_motor = None
    arm = Arm(arm_motor, wrist_motor, shoulder_motor, 89.142, 129.5)
    arm.move_hand_by_motors_input(0, -90, -90)

    # with open('DB', 'rb') as dbfile:
    #   try:
    # db = pickle.load(dbfile)
    #   except EOFError:
    db = {}
    if name in db:
        arm.move_hand_by_motors_input(0, arm.get_alpha1(), arm.get_alpha1())
    else:
        t = 0
        mouther = mouthing()
        val = mouther()
        while val is not None:
            arm.move_hand_by_motors_input(0, arm.get_alpha1() + val * 10, arm.get_alpha1() + val * 10)
            t += 1
            print(val)
            val = mouther()
    # db[name] = arm.get_alpha1()

    # with open('DB', 'ab') as dbfile:

    # source, destination


#     pickle.dump(db, dbfile, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    orient("eyal")
