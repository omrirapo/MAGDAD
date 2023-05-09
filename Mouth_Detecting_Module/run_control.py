from Arm import Arm
from Motor import Motor
from stepper_motor import StepperMotor
from pid import PID
from only_mouth import mouthing

import pickle


def orient(name="user", cam_height=0):
    arm_motor = Motor(18, lambda alpha: alpha/90 )
    wrist_motor = Motor(17, lambda alpha: alpha/90)
    shoulder_motor = StepperMotor(20, 200,5)
    arm = Arm(arm_motor, wrist_motor, shoulder_motor, 89.142, 129.5)
    with open('DB', 'rb') as dbfile:
        try:
            db = pickle.load(dbfile)
        except EOFError:
            db = {}
    if name in db:
        arm.move_hand(db[name][0], db[name][1], arm.get_alpha())
    else:
        pid = PID(2, 0.2, 0.2)
        pid.send(None)
        t = 0
        for i in mouthing():
            arm.move_hand(arm.get_x(), arm.get_y()+4*pid.send([t, i, 0]), arm.get_alpha())
            t += 1
            arm.move_hand(arm.get_x(), arm.get_y() - cam_height, arm.get_alpha())
        db[name] = (arm.get_x(), arm.get_y())

    with open('DB', 'ab') as dbfile:

    # source, destination
        pickle.dump(db, dbfile, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    orient()
