import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Read the input image
img = cv2.imread('face.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 2)
# Draw rectangle around the faces
for (x, y, w, h) in faces:
    # Read the input image
    # Convert into grayscale
    # Detect faces
    mouthes = mouth_cascade.detectMultiScale(gray[x:x+w][y:y+h], 1.1, 2)
    # Draw rectangle around the faces
    for (_x, _y, _w, _h) in mouthes:
        cv2.rectangle(img, (x+_x, y+_y), (x+_x + w, y + _y + h), (255, 0, 0), 2)
        cv2.circle(img, (x+_x + (w // 2),  y + _y + (3 * h // 4)), 20, (255, 0, 0))

# Display the output
cv2.imshow('img', img)
cv2.waitKey()