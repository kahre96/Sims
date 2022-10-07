import cv2  # OpenCV
import numpy
from facenet_pytorch import MTCNN
from PIL import ImageDraw, Image
import tensorflow as tf

tf.config.set_visible_devices([], 'GPU')

detector = MTCNN()

#variable for blurring, must be odd integer?
ksize = (101, 101)

video_capture = cv2.VideoCapture(0)  # webcamera capture

if not video_capture.isOpened():
    print("Unable to access the camera")
else:
    print("Access to the camera was successfully obtained")


def find_face_MTCNN(frame):

    #faces=[]
    #MTCNN detecting faces
    faces, probabilities = detector.detect(frame)

    #draw = ImageDraw.Draw(frame)

    if faces is not None:

        for face in faces:
            print(face)



            faceList = face.tolist()

            x, y, x2, y2 = faceList


            cv2.rectangle(frame,
                          (int(x), int(y)), (int(x2), int(y2)),
                          (255, 0, 0),
                         5)

            #draw.rectangle(face.tolist(), outline=(255, 0, 0), width=6)

            #uncommet code below to blur face
            #detectedFace = cv2.GaussianBlur(roi, ksize, 0)
            #frame[y:y + h, x:x + w] = detectedFace
    return frame

print("Streaming started")
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #frame2= cv2.imread('testpic.jpg')

    #use a function to change to frame by adding a box around the face
    detectfaceMTCNN = find_face_MTCNN(frame)




    # Display the resulting frame
    cv2.imshow("Face detector - to quit press ESC", detectfaceMTCNN)

    # Exit with ESC
    key = cv2.waitKey(1)
    if key % 256 == 27:  # ESC code
        break

# When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()
print("Streaming ended")