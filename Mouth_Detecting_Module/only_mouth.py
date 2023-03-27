import cv2

# Load the cascade
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
# Read the input image
img = cv2.imread('face5.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
mouthes = mouth_cascade.detectMultiScale(gray, 1.1, 2)
# Draw rectangle around the faces
for (x, y, w, h) in mouthes:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.circle(img,(x +(w//2),y +(3*h//4)),20,(255, 0, 0))
# Display the output
cv2.imshow('img', img)
cv2.waitKey()