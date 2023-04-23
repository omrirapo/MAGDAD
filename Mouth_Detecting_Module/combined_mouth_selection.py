import math
import yogevs_functions
import cv2
import numpy as np


def get_mouth_inside_face(img):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Read the input image
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)
    # Draw rectangle around the faces
    possibilities = []
    for (x, y, w, h) in faces:
        # Read the input image
        # Convert into grayscale
        # Detect faces
        mouthes = mouth_cascade.detectMultiScale(gray[y:y + h, x:x + w], 1.1, 11)
        # adds all possible mouths to list
        oriented_mouths = []
        for _x, _y, _w, _h in mouthes:
            oriented_mouths.append((_x + x, y + _y, _w, _h))
        possibilities.append(((x, y, w, h), oriented_mouths))
    return possibilities


def asstimated_center_of_mouth(face, factor):
    """
    :param img: the face image
    :return: predicted location of mouth, (x,y,h)
    x is the x location
    y is the y location
    h is the face height
    """
    # Draw rectangle around the faces
    (x, y, w, h) = face
    return (x + w // 2, y + round(h * factor))


def select_in_relation_to_face(possibilities):
    sorted_faces_mouths = []
    for face, mouths in possibilities:
        asstimation = asstimated_center_of_mouth(face, 0.75)
        sorted_faces_mouths.append(
            (face, sorted(mouths, key=lambda x: math.dist(asstimated_center_of_mouth(x, 0.75), asstimation))))
    return sorted_faces_mouths


def detect_in_frame(img, previous: any, face_cascade):
    # Draw rectangle around the faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    possibilities = get_mouth_inside_face(img)
    sorted_faces_mouths = select_in_relation_to_face(possibilities)
    in_relation_to_previous = []
    if len(sorted_faces_mouths) == 0:
        return img, None


    for face, mouths in in_relation_to_previous:
        (_x, _y, _w, _h) = mouths
        cv2.rectangle(img, (_x, _y), (_x + _w, _y + _h), (255, 0, 0), 2)
    sorted_by_fit = sorted(in_relation_to_previous, key=lambda x: x[1][0] - len(img[0]) // 2)
    if len(sorted_by_fit) !=0:
        return img, sorted_by_fit[0][0]
    return img



# Display the output
if __name__ == '__main__':
    previous = None

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    ds_factor = 0.5

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame, previous = detect_in_frame(frame, previous, face_cascade)
        cv2.imshow('Mouth Detector', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
