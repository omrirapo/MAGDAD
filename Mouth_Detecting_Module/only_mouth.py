import cv2
import yogevs_functions
import combined_mouth_selection
def mouthing():
    """
    a function using image recognition in order to give an approximation to the location of the mouth
    :return: the distance between the mouth and the middle of the image in proportion to the size of the mouth
    """
    MAX_FRAME_OF_LOSS = 5
    test_start = False
    # initializes cascades
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    eyes_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    frame_count = 0
    frame_movement = 0
    t=-1
    if mouth_cascade.empty():
        raise IOError('Unable to load the mouth cascade classifier xml file')

    cap = cv2.VideoCapture(0)
    ds_factor = 0.5
    curr = None
    diff = (0, 0)
    frame_loss = 0
    while True:
        t+=1
        frame_count += 1
        if frame_count != 10:
            continue
        else:
            frame_count = 0

        ret, frame = cap.read()
        height, width, channels = frame.shape
        # gives instructions
        if test_start:
            if curr[1] < height // 4:
                frame = cv2.putText(frame, 'go up ' + str((height // 4 - curr[1]) / curr[3]), (100, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

                yield (height // 4 - curr[1]) / curr[3]


            if curr[1] > height // 4:
                frame = cv2.putText(frame, 'go down' + str(-(height // 4 - curr[1]) / curr[3]), (100, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                yield (height // 4 - curr[1]) / curr[3]

        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 2)
        # Find mouths
        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.3, 13)
        # Finds eyes
        eyes_rects = eyes_cascade.detectMultiScale(gray, 1.3, 13)
        # Filter all mouths inside a face
        if len(faces) != 0:
            temp_arr = []
            for i in faces:
                temp = yogevs_functions.restrict_to_target(i, mouth_rects)
                for j, val in temp:
                    if val != 0:
                        temp_arr.append(j)
            mouth_rects = temp_arr


        # deletes all eyes

        for i in eyes_rects:
            temp = yogevs_functions.restrict_to_target(i, mouth_rects)
            mouth_rects = []
            for j, val in temp:
                if val == 0:
                    mouth_rects.append(j)


        temp_arr = []
        temp = yogevs_functions.restrict_to_target(curr, mouth_rects)
        for j, val in temp:
            if val != 0:
                temp_arr.append(j)

        if len(temp_arr)!= 0:
            mouth_rects = temp_arr
            frame_movement = 0

        elif frame_movement <=5:
            mouth_rects = []
            frame_movement+=1
        else:
            frame_movement = 0

        # paints over the picture
        for (x, y, w, h) in mouth_rects:

            y = int(y - 0.15 * h)
            cv2.circle(frame, (x + (w // 2), y + (h // 2)), 5, (255, 0, 0))
            cv2.circle(frame, (width//4,height//4), 5, (0, 255, 0))


            # finds the approximate movement
            if curr is not None:
                diff = (x - curr[0] + (w - curr[2]) // 2, y - curr[1] + (h - curr[3]) // 2)

            test_start = True
            curr = (x, y, w, h)
            frame_loss = 0
            break
        else:
            frame_loss += 1
            if frame_loss >= MAX_FRAME_OF_LOSS and test_start:
                cv2.circle(frame, (x + (w // 2), y + (h // 2)), 5, (255, 0, 0))

                print("mouth was lost")
            elif curr is not None:
                # draws over approximate location if a current one was not find+

                (x, y, w, h) = curr
                curr = (x + diff[0], y + diff[1], w, h)
                (x, y, w, h) = curr

                cv2.circle(frame, (x + (w // 2), y + (h // 2)), 5, (255, 0, 0))

        cv2.imshow('Mouth Detector', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
