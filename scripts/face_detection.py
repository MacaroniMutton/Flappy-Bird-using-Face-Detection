import numpy as np
import cv2

class FaceDetectionWindow:
    def __init__(self, width, height, video_type=0):
        self.width = width
        self.height = height
        self.capture = cv2.VideoCapture(video_type)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def update(self):
        fy = None
        ret, frame = self.capture.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
            cv2.circle(frame, ((2*x+w)//2, ((2*y+h)//2)), 3, (0, 0, 255), 3)
            fy = int((2*y+h)//2)

        cv2.imshow("Webcam", cv2.flip(frame[:, frame.shape[1]//2-self.width//2:frame.shape[1]//2+self.width//2], 1))
        cv2.waitKey(1)
        return fy

    def destroy(self):
        self.capture.release()
        cv2.destroyAllWindows()

