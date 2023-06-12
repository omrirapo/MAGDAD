from Arm import Arm
from Motor import Motor
from stepper_motor import StepperMotor
from only_mouth import mouthing
from time import sleep
from Plate import Plates
import RPi.GPIO as GPIO
from consts import *
from gatherFood import gather_food

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


def orient(arm: Arm, user_height=0, cam_height=0):
    """

    :param arm: arm Obj
    :param user_height: expected height
    :param cam_height:
    :return: cam height that saw mouth
    """

    print("started orient")

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

    while not (GPIO.input(TOUCH),):
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
    plate_servos = lambda alpha: alpha / (plate_servo_ang / 2)
    plat_mot = Motor(SERVO_PLATTER, plate_servos)
    turn_mot = StepperMotor(BOWL_DIR, BOWL_STP, BOWL_ENABLE, BOWL_NUM)
    return Plates(plat_mot, turn_mot)


def init_arm():
    """

    :return:
    """

    wrist_lambda = lambda alpha: alpha * wrist_ratio / (wrist_servo_ang / 2)
    arm_lambda = lambda alpha: alpha * arm_ratio / (arm_servo_ang / 2)
    arm_motor = Motor(SERVO_ARM, arm_lambda)
    wrist_motor = Motor(SERVO_WRIST, wrist_lambda)
    shoulder_motor = StepperMotor(SHOULDER_DIR, SHOULDER_STP, SHOULDER_ENABLE, SHOULDER_NUM,
                                  MM_PER_ANGLE)
    # todo move the hand here to 000 and initialize the values
    return Arm(arm_motor, wrist_motor, shoulder_motor, FOREARM, BICEP)


def flow():
    """
    manages the program flow
    :return: none
    """
    # define buttons

    # initialise plate:
    platter = init_platter()
    # initialise arm
    arm = init_arm()
    cmd = get_command()

    # call turn bowls a bit
    feed(arm,platter) # todo remove after running feed throw listener


# todo finish get command generic so works also with keyboard.
def get_command():
    pass
    # while True:
    #    if button_pins['']


def feed(arm, platter):
    """
    lifts food, and feeds the user, this the heart
    """
    arm.enable_shoulder()
    gather_food(arm, platter)
    # find mouth height
    orient(arm, mouth_height[-1], CAM_HEIGHT)
    mouth_height.append(orient(arm, 0, CAM_HEIGHT))
    move_till_touch(arm, 10, 0.5)
    arm.move_forward(MOUTH_DEPTH)
    arm.disable_shoulder()
    sleep(EATING_TIME)
    arm.enable_shoulder()
    arm.move_hand(0, 0, 0)
    # todo add a timeout till receive input from microswitch that the arm is back in place before start next round

    arm.disable_shoulder()


if __name__ == '__main__':
    flow()
