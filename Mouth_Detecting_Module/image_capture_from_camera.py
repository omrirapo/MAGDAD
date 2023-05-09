import cv2
from combined_mouth_selection import get_mouth_inside_face,select_in_relation_to_face
import sys

cascPath ="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Draw rectangle around the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(frame, (x + (w // 2), y + (3 * h // 4)), 20, (255, 0, 0))
    possibilities = get_mouth_inside_face(frame)
    sorted_faces_mouths = select_in_relation_to_face(possibilities)
    for face, mouths in sorted_faces_mouths:
        if not len(mouths) == 0:
            (_x, _y, _w, _h) = mouths[0]
            cv2.rectangle(frame, (_x, _y), (_x + _w, _y + _h), (255, 0, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()