from Arm import Arm
from Motor import Motor
from stepper_motor import StepperMotor
from only_mouth import mouthing
from time import sleep
from Plate import Plates
import pickle
import RPi.GPIO as GPIO
from consts import *


pin_mangement = {
    SHOULDER_STP: "stpshoulder",
    SHOULDER_DIR: "dirshoulder",
    MICRO_FRONT: "micro_front",
    SERVO_ARM: "servo_arm",
    TOUCH: "touch",
    BOWL_STP: "stpbowl",
    MICRO_BACK: "micro_back",
    PLATTER_STP: "stpplatter",
    PLATTER_DIR: "dirplatter",
    SERVO_WRIST: "servo_wrist",
    BOWL_DIR: "dirbowl",

    # 24: "changefood",
    # 25: "emergency",
    # 5: "bring_food",
    # 6: "back",
}

button_pins = {
    "micro_front": False,
    "micro_back": False,
    "touch": False,
    "plates_micro_switch": False,
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


def orient(arm: Arm, user_height=0, cam_height=0):
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
    val = mouther()  # todo add an explaination
    while val is not None:
        try:
            arm.move_up_deg(val * MOUTH_IN_DEGREES)
        except Exception as e:
            print(e)


        # arm.move_hand_by_motors_input(0, arm.get_alpha1() + val * 10, arm.get_alpha1() + val * 10) # todo what is 10
        t += 1
        val = mouther()
        sleep(0.1)

    sleep(0.5)
    cams = arm.get_y()
    arm.move_up(cam_height)

    print("finished orient")
    return cams
    # db[name] = arm.get_alpha1()

    # with open('DB', 'ab') as dbfile:

    # source, destination


#     pickle.dump(db, dbfile, protocol=pickle.HIGHEST_PROTOCOL)

def move_till_touch(arm: Arm, dist, time):
    """

    :param arm: arm object
    :return:
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while not GPIO.input(TOUCH):
        arm.move_forward(dist)
    mouth_dist.append(arm.get_x())


def start_all_buttons():
    """
    initialize static buttons
    :return:
    """
    initialize_buttons(button_pins["micro_front"], GPIO.RISING)
    initialize_buttons(button_pins["micro_back"], GPIO.RISING)
    initialize_buttons(button_pins["plates_micro_switch"], GPIO.RISING)
    initialize_buttons(button_pins["changefood"], GPIO.RISING)
    initialize_buttons(button_pins["emergency"], GPIO.FALLING)  # emergerncy needs to make sure it works
    initialize_buttons(button_pins["bring_food"], GPIO.RISING)
    initialize_buttons(button_pins["back"], GPIO.RISING)


def init_platter():
    """

    :return:
    """

    plat_mot = StepperMotor(27, 18, 200)  # todo fill in the constants for the motors
    turn_mot = StepperMotor(23, 22, 200)  # todo fill in the constants for the motors
    return Plates(plat_mot, turn_mot)


def flow():
    """
    manages the program flow
    :return: none
    """
    # define buttons

    # todo initialise user preferances
    # initialise plate:

    # initialise arm
    arm_motor = Motor(SERVO_ARM, lambda alpha: alpha / 45)
    wrist_motor = Motor(SERVO_WRIST, lambda alpha: alpha / 45)
    shoulder_motor = StepperMotor(3, 2, 200,
                                  0.367)  # todo change the constants, and move them into variables with names
    arm = Arm(arm_motor, wrist_motor, shoulder_motor, d, r)
    platter = init_platter()
    platter.gather_food(arm)
    orient(arm, 0, CAM_HEIGHT)

    mouth_height.append(orient(arm, 0, CAM_HEIGHT))

    move_till_touch(arm, 10, 0.5)
    arm.move_hand(0, 0, 0)
    # go back

    # call turn bowls a bit


def alpha_feeding(arm):
    """
    lifts food, and feeds the user, this the first method we use and  hence the alpha version of feeding
    """
    arm.move_hand(-40, -120, -45)
    sleep(2)
    arm.move_hand(-40, -140, -50)
    sleep(2)
    arm.move_hand(-55, -160, -60)
    sleep(2)
    arm.move_hand(-70, -160, -60)
    sleep(2)
    arm.move_hand(-50, -180, -60)
    sleep(2)
    arm.move_hand(-30, -180, -60)
    sleep(2)
    arm.move_hand(0, -160, -40)
    sleep(2)
    arm.move_hand(0, -60, 0)
    sleep(2)
    arm.move_hand(0, 0, 0)
    sleep(2)
    arm.move_hand(450, 0, 0)
    sleep(2)


def beta_feeding(arm): pass


if __name__ == '__main__':
    flow()
