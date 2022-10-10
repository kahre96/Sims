import cv2
import os


path = "/AI/Images/Andreas"

for image in os.listdir(path):
    pic = cv2.imread(f"D:\dokument\skolskit\SIMS\Code\Sims\AI\Images\Andreas\{image}")
    cv2.imwrite(f"Images/Andreas2/{image}",cv2.cvtColor(pic, cv2.COLOR_BGR2RGB))

