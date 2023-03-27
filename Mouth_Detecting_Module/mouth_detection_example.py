import cv2

# Load the cascade
mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
# Read the input image
img = cv2.imread('pedri_img.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
mouthes = mouth_cascade.detectMultiScale(gray, 1.1, 500)
# Draw rectangle around the faces
for (x, y, w, h) in mouthes:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
# Display the output
cv2.imshow('img', img)
cv2.waitKey()