MOUTH_FINDER_SCALER = 5  # a constant to scale the distance that the arm moves up when orienting to the mouth

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
EAT_CONTROL = 8
CHANGE_CONTROL = 7
STOP_CONTROL = 5  # NOT USED

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
MIN_ORIENT_HEIGHT = -80
MAX_ORIENT_HEIGHT = float("inf")
# arm lengths
FOREARM = 138.44  # from the wrist to the end of the spoon
BICEP = 129.5  # the length from the elbow to the wrist
MM_PER_ANGLE = 0.367
# travel
MAX_X = 600

# histogram
mouth_height = [0]
mouth_dist = [0]

# logging - wifi and mail
MAGDAD_MAIL = "alinmagdad@outlook.com"
CLIENT_MAIL = "alinmagdad@outlook.com"
WIFI_NAME = ""
WIFI_PASS = ""

# Personal preferences
MOUTH_DEPTH = 20  # the depth of the spoon in the mouth
MOUTH_ANGLE = -7  # the angle of the spoon in the mouth
EATING_TIME = 2
DEG_PER_BOWL_TURN = 330

#FilePaths
relative_path = "/home/pi/FeedingMagdadAlin/"
memory_dir_path = relative_path + "memory_dir/"
height_file_path = memory_dir_path + "prev_height.txt"
initial_plate_path = memory_dir_path + "initial_plate.txt"
