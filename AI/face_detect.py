import mtcnn
print(mtcnn.__version__)


#load one image
import matplotlib.pyplot as plt
filename = "Dataset/kåhre"
pixels = plt.imread(filename)
print("Shape of image/array:",pixels.shape)
imgplot = plt.imshow(pixels)
plt.show()

#detect faces
detector = mtcnn.MTCNN()
faces = detector.detect_faces(pixels)
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
        x2 = x
        x2 += width/2
        y2 = y
        y2 += height/2
        #print("x2:", x2)
        # create the shape
        #rect = plt.Rectangle((x, y), width, height, fill=False, color='red')
        rect = plt.Circle((x2, y2),width, fill=False, color='red')
        #crosshair = plt.Circle((x2, y2), fill=False, color='red')
        ch = plt.plot(x2,y2, marker="+", markersize=width/1.8, markerfacecolor="red",markeredgecolor="red")
        ax.add_patch(rect)
        #ax.add_patch(crosshair)
        #ax.add_patch(ch)

    plt.show()


draw_facebox(filename, faces)