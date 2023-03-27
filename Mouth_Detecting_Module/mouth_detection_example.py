import cv2
import math
Ratio_from_face = 1 / 4


def asstimated_center_of_mouth(gray):
    """
    :param img: the face image
    :return: predicted location of mouth, (x,y,h)
    x is the x location
    y is the y location
    h is the face height
    """
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face = face_cascade.detectMultiScale(gray, 1.1, 2)[0]
    # Draw rectangle around the faces
    (x, y, w, h) = face
    return (x + w // 2, y + 3 * h // 4) , h


# Load the cascade
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
# Read the input image
img = cv2.imread('face5.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Find asstimatrd location of mouth
asttimated_center, face_height = asstimated_center_of_mouth(gray)
# Detect faces
mouthes = mouth_cascade.detectMultiScale(gray, 1.25, minNeighbors=3)
# Draw rectangle around the faces
for mouth in mouthes:
    (x,y,w,h) = mouth
    mouth_center = (x + w//2, y + h//2)
    if (math.dist(mouth_center, asttimated_center) <= face_height*Ratio_from_face):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
# Display the output
cv2.imshow('img', img)
cv2.waitKey()


