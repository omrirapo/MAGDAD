from Arm import Arm
from Motor import Motor
from stepper_motor import StepperMotor
from pid import PID
from only_mouth import mouthing
from time import sleep
import pickle
import RPi.GPIO as GPIO


def orient(name="user", cam_height=0):
    print("started orient")

    arm_motor = Motor(17, lambda alpha: alpha / 90)
    wrist_motor = Motor(18, lambda alpha: alpha / 90)
    shoulder_motor = StepperMotor(20, 21, 200, 131.34)
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
            val = mouther()

    sleep(0.5)
    arm.move_hand(arm.get_x(), arm.get_y() + 35, 0)

    print("finished orient")

    # db[name] = arm.get_alpha1()

    # with open('DB', 'ab') as dbfile:

    # source, destination


#     pickle.dump(db, dbfile, protocol=pickle.HIGHEST_PROTOCOL)
def move_till_touch(should_i_stop):
    print("started move")

    # Define the GPIO pin connected to the touch sensor output
    TOUCH_SENSOR_PIN = 2

    # Initialize the GPIO library
    GPIO.setmode(GPIO.BCM)

    # Set the touch sensor pin as an input with a pull-up resistor
    GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Loop forever to detect touch
    shoulder_motor = StepperMotor(16, 21, 200, 131.34)

    count = 0
    while True:

        # Check if the touch sensor pin is grounded, indicating a touch has been detected
        if GPIO.input(TOUCH_SENSOR_PIN):
            count += 1
            print(f"Touch Detected! :{count}")
            break
            # Wait for a short period to prevent multiple touch detections
        for i in range(4):
            shoulder_motor.step()
    print("finished_move")


if __name__ == '__main__':
    orient("")
    move_till_touch(lambda: False)