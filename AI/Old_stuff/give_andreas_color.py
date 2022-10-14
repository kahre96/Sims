import cv2
import os

#no longer gives andreas color, now resizes images

path = "D:/dokument/skolskit/SIMS/Code/Sims/AI/Images/Guest"

for image in os.listdir(path):
    pic = cv2.imread(f"{path}/{image}")
    pic2 = cv2.resize(pic, (224, 224))

    if(image[-8:] == ".jpg.jpg"):
        image2 = image[:-4]

        cv2.imwrite(f"D:/dokument/skolskit/SIMS/Code/Sims/AI/testfolder/hej/{image2}", pic2)


