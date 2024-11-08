import cv2
import numpy as np


def detect_faces(image):
    # Load the pre-trained face detection model

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Read the image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    return len(faces) == 1, len(faces)
