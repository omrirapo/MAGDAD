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

# dimensions
CAMHEIGHT = 20


#histogram
mouth_height = []
mouth_dist = []

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


def initialize_buttons(button, direction):
    """

    :param button: pin name to initialise
    :param direction: GPIO.risng\falling
    :return:
    """
    button = pin_mangement[button]
    GPIO.setmode(GPIO.BCM)

    # Set the touch sensor pin as an input with a pull-up resistor
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button, direction, callback=my_callback, bouncetime=200)

def clear_button(button):
    """
    free the gpio pin
    :param button: pinname
    :return:
    """
    GPIO.remove_event_detect(pin_mangement[button])


def orient(arm: Arm, user_height , cam_height=0):
    """

    :param arm: arm Obj
    :param user_height: expected height
    :param cam_height:
    :return: cam height that saw mouth
    """

    print("started orient")

    # arm_motor = Motor(SERVO_ARM, lambda alpha: alpha / 90)
    # wrist_motor = Motor(SERVO_WRIST, lambda alpha: alpha / 90)
    # shoulder_motor = StepperMotor(20, 21, 200, 131.34)
    # arm = Arm(arm_motor, wrist_motor, shoulder_motor, 89.142, 129.5)
    # arm.move_hand_by_motors_input(0, -90, -90)

    # with open('DB', 'rb') as dbfile:
    #   try:
    # db = pickle.load(dbfile)
    # #   except EOFError:
    # db = {}
    # if name in db:
    #     arm.move_hand_by_motors_input(0, arm.get_alpha1(), arm.get_alpha1())

    t = 0
    mouther = mouthing()
    val = mouther() # todo add an explaination
    while val is not None:
        if val>0:
            arm.move_up()
        elif val<0:
            arm.move_backward()
        # arm.move_hand_by_motors_input(0, arm.get_alpha1() + val * 10, arm.get_alpha1() + val * 10) # todo what is 10
        t += 1
        val = mouther()

    sleep(0.5)
    cams = arm.get_y()
    arm.move_hand(arm.get_x(), arm.get_y() + cam_height, 0)

    print("finished orient")
    return cams
    # db[name] = arm.get_alpha1()

    # with open('DB', 'ab') as dbfile:

    # source, destination

#     pickle.dump(db, dbfile, protocol=pickle.HIGHEST_PROTOCOL)

def move_till_touch(arm : Arm):
    """

    :param arm: arm object
    :return:
    """

    while not button_pins["touch"]:
        speed = 0.2+0.8*(mouth_dist[-1]-arm.get_x())/mouth_dist[-1] # poprtional to history
        arm.move_forward(speed)
    mouth_dist.append(arm.get_x())


def start_all_buttons():
    initialize_buttons(button_pins["micro_front"], GPIO.RISING)
    initialize_buttons(button_pins["micro_back"], GPIO.RISING)
    initialize_buttons(button_pins["touch"], GPIO.RISING)
    initialize_buttons(button_pins["ir_turn"], GPIO.RISING)
    initialize_buttons(button_pins["changefood"], GPIO.RISING)
    initialize_buttons(button_pins["emergency"], GPIO.FALLING) # emergerncy needs to make sure it works
    initialize_buttons(button_pins["bring_food"], GPIO.RISING)
    initialize_buttons(button_pins["back"], GPIO.RISING)


def flow():
    """
    manages the program flow
    :return: none
    """
    # define buttons
    start_all_buttons()

    #todo initialise user preferances

    #initialise arm

    arm_motor = Motor(SERVO_ARM, lambda alpha: alpha / 90)
    wrist_motor = Motor(SERVO_WRIST, lambda alpha: alpha / 90)
    shoulder_motor = StepperMotor(20, 21, 200, 131.34)
    arm = Arm(arm_motor, wrist_motor, shoulder_motor, 89.142, 129.5) #todo explain the constants


    # wait for input - set bowl.

    # call gather food

    # call orient

    mouth_height.append(orient(arm,mouth_height[-1], CAMHEIGHT))

    move_till_touch(arm)

    #go back

    # call turn bowls a bit


if __name__ == '__main__':
    orient("")
    move_till_touch(lambda: False)
