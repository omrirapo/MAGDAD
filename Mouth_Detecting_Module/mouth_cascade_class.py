import math

import cv2
import yogevs_functions
import combined_mouth_selection
MAX_FRAME_OF_LOSS =20
DEACCELERATION = 0.2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
start = False

if mouth_cascade.empty():
    raise IOError('Unable to load the mouth cascade classifier xml file')

cap = cv2.VideoCapture(0)
ds_factor = 0.5
curr = None
diff = (0,0)
frame_loss = 0
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)

    # Draw rectangle around the faces



    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.3, 13)

    eyes_rects = eyes_cascade.detectMultiScale(gray, 1.3, 13)

    if len(faces) != 0:
        temp_arr = []
        for i in faces:
            temp = yogevs_functions.restrict_to_target(i, mouth_rects)
            for j, val in temp:
                if val != 0:
                    temp_arr.append(j)
        mouth_rects = temp_arr


    for i in eyes_rects:
        temp = yogevs_functions.restrict_to_target(i, mouth_rects)
        mouth_rects = []
        for j, val in temp:
            if val == 0:
                mouth_rects.append(j)
    for (x, y, w, h) in mouth_rects:
        y = int(y - 0.15 * h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if curr != None:
            diff = (x-curr[0]+(w-curr[2])//2,y - curr[1]+(h-curr[3])//2)
        curr = (x, y, w, h)
        frame_loss = 0
        break
    else:
        frame_loss+=1
        if frame_loss >= MAX_FRAME_OF_LOSS:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            print ("mouth was lost")
        elif curr is not None:
            (x, y, w, h) = curr
            curr = (x+math.floor(diff[0]), y+ math.floor(diff[1]), w, h)
            (x, y, w, h) = curr

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            temp = tuple(DEACCELERATION * elem for elem in diff)
            diff = temp
    cv2.imshow('Mouth Detector', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
