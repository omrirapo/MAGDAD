import RPi.GPIO as GPIO
import time


def check_touch(num=10)->bool:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(18, GPIO.OUT)

    run = True
    last = False
    high = 0
    start_t = time.time()
    thiss = False
    GPIO.output(18, GPIO.HIGH)
    val = 0
    for i in range(num):
        start_t = time.time()
        GPIO.output(18, GPIO.HIGH)
        thiss = GPIO.input(12)
        timer = time.time()

        val += int((not thiss) and last)

        last = not thiss
        time.sleep(0.001)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.001)

    GPIO.output(18, GPIO.LOW)

    GPIO.cleanup()
    return bool((2 * val) // num)
