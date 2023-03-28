import math

import cv2


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
        mouthes = mouth_cascade.detectMultiScale(gray[y:y + h, x:x + w], 1.1, 2)

        # adds all possible mouths to list
        oriented_mouths = []
        for _x, _y, _w, _h in mouthes:
            oriented_mouths.append((_x+x, y+_y, _w, _h))
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
    return (x + w // 2, y + round(h*factor))


def select_in_relation_to_face(possibilities):
    sorted_faces_mouths = []
    for face, mouths in possibilities:
        asstimation = asstimated_center_of_mouth(face, 0.75)
        sorted_faces_mouths.append((face, sorted(mouths, key = lambda x: math.dist(asstimated_center_of_mouth(x, 0.75), asstimation))))
    return sorted_faces_mouths


# Display the output
if __name__ == '__main__':
    img = cv2.imread('faces.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Draw rectangle around the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(img, (x + (w // 2), y + (3 * h // 4)), 20, (255, 0, 0))
    possibilities = get_mouth_inside_face(img)
    sorted_faces_mouths = select_in_relation_to_face(possibilities)
    for face, mouths in sorted_faces_mouths:
        if not len(mouths) == 0:
            (_x, _y, _w, _h) = mouths[0]
            cv2.rectangle(img, (_x, _y), (_x + _w, _y + _h), (255, 0, 0), 2)


cv2.imshow('img', img)

cv2.waitKey()
