import os
import sys

from Arm import Arm
from Motor import Motor
import logger
from stepper_motor import StepperMotor
from only_mouth import mouthing
from time import sleep
from Plate import Plates
import RPi.GPIO as GPIO
from consts import *
from gatherFood import gather_food
import logging
import logging.handlers

current_action = None


pin_mangement = {
    SHOULDER_STP: "stpshoulder",
    SHOULDER_DIR: "dirshoulder",
    MICRO_FRONT: "micro_front",
    SERVO_ARM: "servo_arm",
    TOUCH: "touch",
    BOWL_STP: "stpbowl",
    MICRO_BACK: "micro_back",
    SERVO_WRIST: "servo_wrist",
    BOWL_DIR: "dirbowl"

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


def orient(arm: Arm, user_height=0):
    """

    :param arm: arm Obj
    :param user_height: expected height
    :return: cam height that saw mouth
    """

    logging.info("started orient")

    try:
        height_file = open(height_file_path, 'r')
        height = float(height_file.read())
        arm.move_up(height)
    except:
        logging.warning("orient didnt succeed to find prev height or go to it")

    t = 0
    mouther = mouthing()
    val = mouther()  # todo add an explaination
    while val is not None:
        if check_stop_buttons():
            return False
        try:
            arm.move_up(val * MOUTH_FINDER_SCALER)
        except Exception as e:
            logging.error(f"error in orient,can't move up, error: {e}")

        t += 1
        val = mouther()
        sleep(0.04)

    sleep(0.5)
    cams = arm.get_y()
    if not arm.move_hand(y=cams + CAM_HEIGHT, alpha=0):
        logging.error("orient failed to finish movement, you're to high up")
        return False
    logging.info("finished orient")

    if MIN_ORIENT_HEIGHT > arm.get_y():
        logging.error("can't continue, you're to low")
        return False
    if arm.get_y() > MAX_ORIENT_HEIGHT:
        logging.error("can't continue, you're to high")
        return False
    height_file = open(height_file_path, 'w')
    height_file.write(str(cams))

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

    while not (GPIO.input(TOUCH)):
        if check_stop_buttons():
            return False
        if not arm.move_forward(dist):
            return False
    mouth_dist.append(arm.get_x())
    return True


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


def init_platter(arm):
    """

    :return:
    """
    try:
        initial_plate_file = open(initial_plate_path, 'r')
        initial_plate = int(initial_plate_file.read())
    except:
        logging.warning("couldn't find last plate")
        initial_plate = 0
    plate_servos = lambda alpha: alpha / (plate_servo_ang / 2)
    plat_mot = Motor(SERVO_PLATTER, plate_servos, initial_angle=(initial_plate - 1) * 120)
    turn_mot = StepperMotor(BOWL_DIR, BOWL_STP, BOWL_ENABLE, BOWL_NUM)
    return Plates(plat_mot, turn_mot, arm, initial_plate)


def init_arm():
    """

    :return:
    """

    wrist_lambda = lambda alpha: alpha * wrist_ratio / (wrist_servo_ang / 2)
    arm_lambda = lambda alpha: alpha * arm_ratio / (arm_servo_ang / 2)
    arm_motor = Motor(SERVO_ARM, arm_lambda)
    wrist_motor = Motor(SERVO_WRIST, wrist_lambda)
    shoulder_motor = StepperMotor(SHOULDER_DIR, SHOULDER_STP, SHOULDER_ENABLE, SHOULDER_NUM, MM_PER_ANGLE,
                                  [(4, 1), (17, 0)])
    return Arm(arm_motor, wrist_motor, shoulder_motor, FOREARM, BICEP)


def on_eat_control_pressed(arm: Arm, platter: Plates):
    """

    :return:
    """
    print("eat control pressed")
    if current_action is None:
        feed(arm, platter)
    elif current_action == "orient" or current_action == "feed to user":
        pass
    elif current_action == "change food":
        pass


def on_change_control_pressed(arm: Arm, platter: Plates):
    """

    :return:
    """
    platter.change_plate()


def init_control_buttons(arm, platter):
    """

    :param arm:
    :param platter:
    :return:
    """
    GPIO.setmode(GPIO.BCM)

    # Set the touch sensor pin as an input with a pull-up resistor
    GPIO.setup(EAT_CONTROL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(EAT_CONTROL, GPIO.FALLING, callback=lambda _: on_eat_control_pressed(arm, platter),
    #                      bouncetime=200)
    GPIO.setup(CHANGE_CONTROL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(CHANGE_CONTROL, GPIO.FALLING, callback=lambda _: on_change_control_pressed(arm, platter),
    #                      bouncetime=200)


def flow():
    """
    manages the program flow
    :return: none
    """
    # define buttons

    # initialise plate:
    arm = init_arm()
    arm.wake_up()

    platter = init_platter(arm)
    init_control_buttons(arm, platter)
    # initialise arm
    while True:
        cmd = get_command(arm, platter)
        if cmd == "exit":
            arm.disable_shoulder()
            platter.disable_bowl_motor()
            platter.go_to_start()
            return
        sleep(0.5)

def check_stop_buttons():
    """
    checks if one of the buttons is pressed and if so returns True
    """
    return not (GPIO.input(CHANGE_CONTROL) and GPIO.input(EAT_CONTROL))
def get_command(arm, platter):
    """
    checks if one of the buttons is pressed and if so runs the corresponding command
    Note: activated only when in (0,0,0) waiting for orders/
    """
    if not GPIO.input(EAT_CONTROL):
        print("eat")
        return feed(arm, platter)
    elif not GPIO.input(CHANGE_CONTROL):
        print("change")
        return platter.change_plate()
    print("nothing")
    # inp = input("E - Eat. C - change, Q - quit")
    # if inp == "E":
    #     return feed(arm, platter)
    # elif inp == "C":
    #     return platter.change_plate()
    # elif inp == "Q":
    #     return "exit"


def feed(arm, platter):
    """
    lifts food, and feeds the user, this the heart
    """
    current_action = "lift"
    arm.enable_shoulder()
    arm.move_to_minimal_x()
    gather_food(arm, platter)
    # find mouth height
    # orient(arm, mouth_height[-1], CAM_HEIGHT)
    arm.disable_shoulder()
    current_action = "orient"
    if orient(arm, 0) is not False:
        arm.enable_shoulder()
        arm.move_to_minimal_x()
        current_action = "feed to user"
        if move_till_touch(arm, 10, 0.5):
            sleep(0.2)
            arm.move_hand(x=arm.get_x() + MOUTH_DEPTH, alpha=MOUTH_ANGLE, wait_between_steps=0.01)
            sleep(0.2)
        arm.disable_shoulder()
        sleep(EATING_TIME)
    arm.enable_shoulder()
    current_action = "return to start"
    arm.move_hand(0, 0, 0)
    arm.move_to_minimal_x()
    #arm.spill_food()
    current_action = None

    sleep(0.5)

    arm.disable_shoulder()
    try:
        logger.sender()
    except Exception as e:
        print(f"send fail {e}")
if __name__ == '__main__':
    logs = open("logs.log", 'w')
    if not logs:
        print("can't open log file")
        exit(1)
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)  # todo change to logs
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    root.addHandler(handler)
    flow()
