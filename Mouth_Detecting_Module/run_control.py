from Arm import Arm
from Motor import Motor
from stepper_motor import StepperMotor
from only_mouth import mouthing
from time import sleep
import pickle
import RPi.GPIO as GPIO

MICRO_FRONT = 0
MICRO_BACK = 0
TOUCH = 0
IR_TURN = 0
CHANGE_FOOD = 0
EMERGENCY = 0
BRING_FOOD = 0
BACK = 0
SERVO_ARM = 17
SERVO_WRIST = 18
SHOULDER_DIR = 0
SHOULDER_STP = 0
BOWL_DIR = 0
BOWL_STP = 0
PLATTER_DIR = 0
PLATTER_STP = 0

pin_mangement = {
    4: "micro_front",
    27: "micro_back",
    22: "touch",
    23: "ir_turn",
    24: "changefood",
    25: "emergency",
    5: "bring_food",
    6: "back",
    17: "servo_arm",
    18: "servo_wrist",
    12: "dirshoulder",
    13: "stpshoulder",
    16: "dirbowl",
    26: "stpbowl",
    20: "dirplatter",
    21: "stpplatter"
}

button_pins = {
    "micro_front": False,
    "micro_back": False,
    "touch": False,
    "ir_turn": False,
    "changefood": False,
    "emergency": False,
    "bring_food": False,
    "back": False,
}


def my_callback(channel):
    button_pins[pin_mangement[channel]] = True


def initialize_buttons():
    GPIO.setmode(GPIO.BCM)

    # Set the touch sensor pin as an input with a pull-up resistor
    GPIO.setup(TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TOUCH, GPIO.FALLING, callback=my_callback, bouncetime=200)



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
    # Initialize the GPIO library

    # Loop forever to detect touch
    shoulder_motor = StepperMotor(16, 21, 200, 131.34)

    while True:

        # Check if the touch sensor pin is grounded, indicating a touch has been detected
        if GPIO.input(button_pins["touch"]):

            break
            # Wait for a short period to prevent multiple touch detections
        for i in range(4):
            shoulder_motor.step()
    print("finished_move")


if __name__ == '__main__':
    orient("")
    move_till_touch(lambda: False)
