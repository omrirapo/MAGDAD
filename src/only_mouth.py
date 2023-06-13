import cv2

DELTA = 0.4


def restrict_to_target(target, obj_arr):
    """
    rstrict search for specific target rect. recieves a rectangle and a list of rectangles and returnes
    a new list of all the rects that intersect it.
    sorted by the size of the intesection
    :param target: (x,y,w,h)
    :param obj_arr: array of rects
    :return: list of rects in obj arr that intersect with target
    """
    if target is None:
        return [(x, 0) for x in obj_arr]
    recs = []
    for rec in obj_arr:
        if rec[2] + target[2] < max(rec[0] + rec[2], target[0] + target[2]) - min(rec[0], target[0]) or rec[3] + target[
            3] < max(rec[1] + rec[3], target[1] + target[3]) - min(rec[1], target[1]):
            recs.append((rec, 0))
        else:
            recs.append((rec, 1))

    return recs


def mouthing():
    """
    a function using image recognition in order to give an approximation to the location of the mouth
    :return: the distance between the mouth and the middle of the image in proportion to the size of the mouth
    """
    MAX_FRAME_OF_LOSS = 5
    # initializes cascades
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    eyes_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    frame_count = 0
    frame_movement = 0
    t = -1
    if mouth_cascade.empty():
        raise IOError('Unable to load the mouth cascade classifier xml file')

    cap = cv2.VideoCapture(0)
    ds_factor = 0.5
    curr = None
    diff = (0, 0)
    frame_loss = 0

    def get_pos():

        while True:
            ret, frame = cap.read()
            height, width, channels = frame.shape
            # gives instructions

            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Find faces
            faces = face_cascade.detectMultiScale(gray, 1.2, 13)
            # Find mouths
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.1, 13)
            # Finds eyes
            eyes_rects = eyes_cascade.detectMultiScale(gray, 1.1, 13)
            # Filter all mouths inside a face
            if len(faces) != 0:
                temp_arr = []
                for i in faces:
                    temp = restrict_to_target(i, mouth_rects)
                    for j, val in temp:
                        if val != 0:
                            temp_arr.append(j)
                mouth_rects = temp_arr

            # deletes all eyes

            for i in eyes_rects:
                temp = restrict_to_target(i, mouth_rects)
                mouth_rects = []
                for j, val in temp:
                    if val == 0:
                        mouth_rects.append(j)

            # paints over the picture
            for (x, y, w, h) in mouth_rects:

                y = int(y - 0.15 * h)

                test_start = True
                _y = y + h // 2
                if abs(height // 4 - _y) / h > DELTA:
                    return float((height // 4 - _y) / h)
                else:
                    return None

            c = cv2.waitKey(1)
            if c == 27:
                break

    return get_pos

