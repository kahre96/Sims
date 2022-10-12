import cv2
from facenet_pytorch import MTCNN
import os
import time

now = int(time.time())


class picTaker():

    def __init__(self, label, p_amount=1000):
        self.pic_amount = p_amount
        self.label = label
        self.dir_path = f"testfolder/{label}"
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 3840)
        self.cam.set(4, 2160)
        self.detector = MTCNN()
        self.counter = 0
        self.frame = None
        self.check_folder()
        self.take_pics()

    def take_pics(self):
        while True:
            check, self.frame = self.cam.read()
            if not check:
                print("Cant recive a frame from camera. exiting...")
                break

            faces, probability = self.detector.detect(self.frame)

            if faces is not None:
                for face in faces:
                    if any(cord < 0 for cord in face):
                        break

                    x, y, x2, y2 = face.astype(int)
                    if x2 - x < 180:
                        break
                    if y2 - y < 180:
                        break

                    self.save_image(x, y, x2, y2)


            cv2.namedWindow('video', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('video', 1280, 720)
            cv2.imshow('video', self.frame)

            key = cv2.waitKey(1)
            if key == 27:
                break
        self.cam.release()
        cv2.destroyAllWindows()

    # look if folder already exists otherwise creates it
    def check_folder(self):
        if os.path.exists(self.dir_path):
            return
        else:
            os.mkdir(self.dir_path)

    def save_image(self, x, y, x2, y2):
        cropped_img = self.frame[y:y2, x:x2]

        reimage = cv2.resize(cropped_img, (224, 224))
        cv2.imwrite(f"{self.dir_path}/{self.label}_{now}_{self.counter}.jpg", reimage)
        self.counter += 1
        print(f"Pictures taken: {self.counter}")
        if self.counter >= self.pic_amount:
            quit()





