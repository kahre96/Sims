import mtcnn
import cv2
import PIL
import numpy as np
print(mtcnn.__version__)


#load one image
import matplotlib.pyplot as plt
filename = "dog.jpg"
img = plt.imread(filename)
#print("Shape of image/array:",pixels.shape)
#imgplot = plt.imshow(pixels)
#plt.show()

#detect faces
detector = mtcnn.MTCNN()
faces = detector.detect_faces(img)
for face in faces:
    print(face)



# draw an image with detected objects
def draw_facebox(filename, result_list):

    data = plt.imread(filename)

    plt.imshow(data)

    #get the context from image to use as reference for rectangle?
    ax = plt.gca()

    for result in result_list:
        #grabbign coordinates from the detector
        x, y, width, height = result['box']
        print(result['box'])
        #x2 = x
        #x2 += width/2
        #y2 = y
        #y2 += height/2
        #print("x2:", x2)
        # create the shape
        rect = plt.Rectangle((x, y), width, height, fill=False, color='red')
        #rect = plt.Circle((x2, y2),width, fill=False, color='red')
        #crosshair = plt.Circle((x2, y2), fill=False, color='red')
        #ch = plt.plot(x2,y2, marker="+", markersize=width/1.8, markerfacecolor="red",markeredgecolor="red")
        ax.add_patch(rect)
        plt.show()
        #ax.add_patch(crosshair)
        #ax.add_patch(ch)
        #print("x:  ",x);
        #print("x2: ",x+width);
        #print("y:  ",y);
        #print("y2: ",y+height);
        #cropped_img = img[y:y+height,x:x+width];

        #cv2.imwrite("test.jpg", cropped_img);
        #img2 = cv2.imread("test.jpg");
        #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        #cv2.imwrite("test.jpg", img2);





draw_facebox(filename, faces)