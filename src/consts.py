MOUTH_IN_DEGREES = 5

# pins:
MICRO_FRONT = 4
MICRO_BACK = 17
TOUCH = 11
CHANGE_FOOD = 0
EMERGENCY = 0
BRING_FOOD = 0
BACK = 0
SERVO_ARM = 9
SERVO_WRIST = 25
SHOULDER_DIR = 3
SHOULDER_STP = 2
SHOULDER_ENABLE = 27
BOWL_DIR = 23
BOWL_STP = 22
BOWL_ENABLE = 18
SERVO_PLATTER = 12

# servos
wrist_servo_ang = 180
wrist_ratio = 2
arm_servo_ang = 180
arm_ratio = 2
plate_servo_ang = 270

# steppers:
SHOULDER_NUM = 200
BOWL_NUM = 200

STEP_DELAY = 0.00324

# dimensions
CAM_HEIGHT = 35
# arm lengths
FOREARM = 138.44  # from the wrist to the end of the spoon
BICEP = 129.5  # the length from the elbow to the wrist
MM_PER_ANGLE = 0.367
# travel
MAX_X = 600

# histogram
mouth_height = [0]
mouth_dist = [0]

# logger - wifi and mail
MAGDAD_MAIL = "alinmagdad@outlook.com"
CLIENT_MAIL = "alinmagdad@outlook.com"
WIFI_NAME = ""
WIFI_PASS = ""

# Personal preferences
MOUTH_DEPTH = 18  # the depth of the spoon in the mouth
MOUTH_ANGLE = -7
EATING_TIME = 2
DEG_PER_BOWL_TURN = 330