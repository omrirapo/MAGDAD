# import RPi.GPIO as GPIO
#
# # GPIO pin number
# pin = 18
#
# # Define interrupt handler function
# def my_callback(channel):
#     print("Interrupt detected on channel:", channel)
#
# # Configure GPIO pin as input
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin, GPIO.IN)
#
# # Set up interrupt on falling edge
# GPIO.add_event_detect(pin, GPIO.FALLING, callback=my_callback, bouncetime=200)
#
# try:
#     print("Waiting for interrupt...")
#     while True:
#         pass
#
# except KeyboardInterrupt:
#     print("Exiting...")
#     GPIO.cleanup()
