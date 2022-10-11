import cv2
import os

#no longer gives andreas color, now resizes images

path = "D:/dokument/skolskit/SIMS/Code/Sims/AI/testfolder/extra_pics_10_10/kahre2"

for image in os.listdir(path):
    pic = cv2.imread(f"{path}/{image}")
    pic2 = cv2.resize(pic, (224, 224))
    cv2.imwrite(f"D:/dokument/skolskit/SIMS/Code/Sims/AI/testfolder/extra_pics_10_10_resize/kahre2/{image}", pic2)

