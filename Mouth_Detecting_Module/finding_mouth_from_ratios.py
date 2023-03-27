min_mouth_width_factor = 0.3
max_mouth_width_factor = 0.45
min_mouth_height_factor = 0.15
max_mouth_height_factor = 0.25

def assert_mouth_with_ratios(face, mouthes):
    """
    :param face: (x,y,w,h) - starting x starting y' width and height of face
    :param mouthes: arr of mouth = (x,y,w,h) - starting x starting y' width and height of face
    :return: mouthes that their ratios are good in comperison to face
    """
    valid_mouthes = []
    (x, y, w, h) = face
    for mouth in mouthes:
        (x_mouth, y_mouth, width_mouth, height_mouth) = mouth
        if (w * min_mouth_width_factor <= width_mouth <= w* max_mouth_width_factor):
            if (w * min_mouth_height_factor <= height_mouth <= w* max_mouth_height_factor):
                valid_mouthes.append(mouth)
    return valid_mouthes


import cv2
import math
Ratio_from_face = 1 / 4



# Load the cascade
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Read the input image
img = cv2.imread('face.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
face = face_cascade.detectMultiScale(gray, 1.1, 2)[0]
mouthes = mouth_cascade.detectMultiScale(gray, 1.25, minNeighbors=3)
valid_mouthes = assert_mouth_with_ratios(face,mouthes)
# Draw rectangle around the faces
for mouth in valid_mouthes:
    (x,y,w,h) = mouth
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
# Display the output
cv2.imshow('img', img)
cv2.waitKey()
