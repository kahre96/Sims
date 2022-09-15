import cv2  # OpenCV
from mtcnn import MTCNN


detector = MTCNN()

#variable for blurring, must be odd integer?
ksize = (101, 101)

video_capture = cv2.VideoCapture(0)  # webcamera capture

if not video_capture.isOpened():
    print("Unable to access the camera")
else:
    print("Access to the camera was successfully obtained")


def find_face_MTCNN(frame,result_list):
    for result in result_list:
        x, y, w, h = result['box']
        roi = frame[y:y + h, x:x + w]
        cv2.rectangle(frame,
                      (x, y), (x + w, y + h),
                      (255, 0, 0),
                      5)

        #uncommet code below to blur face
        detectedFace = cv2.GaussianBlur(roi, ksize, 0)
        frame[y:y + h, x:x + w] = detectedFace
    return frame

print("Streaming started")
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #MTCNN detector detects the face
    faces = detector.detect_faces(frame)

    #use a function to change to frame by adding a box around the face
    detectfaceMTCNN = find_face_MTCNN(frame,faces)




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