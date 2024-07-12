import PIL #pillow
from PIL import Image
import os #operating system
import numpy as np #numpy
import cv2 #opencv
import database_management

#Face model
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def getImage():
    path = "Sample"
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples  = []
    ids = []

    #Looping through image paths and retrieving face samples and its respective ids
    for imagePath in imagePaths:
       PIL_img = PIL.Image.open(imagePath).convert('L')
       img_numpy = np.array(PIL_img)
       id = int(os.path.split(imagePath)[-1].split(".")[-3])
       faces = face_detector.detectMultiScale(img_numpy)
       for (x, y, a, b) in faces:
           faceSamples.append(img_numpy[y:y+a, x:x+b])
           ids.append(id)

    return faceSamples, ids



def train_faces():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids= getImage()

    #Training faces for recognition
    recognizer.train(faces, np.array(ids))
    recognizer.write("Trainer/trainer.yml")
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))


def capture_face(_faceid, _name, _age):

    #Adding a new entry into database(primary_details)
    sql = "INSERT INTO primary_details (user_id, name, age) VALUES ({}, '{}', {})".format(_faceid, _name, _age)
    database_management.connect_to_database(sql, False)

    #camera object
    cam = cv2.VideoCapture(0)

    n = 0
    sample_size = 75
    while(True):

        # Recognizing images and converting into grayscale
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(img, 1.3, 5)

        #Saving images of recognized faces into 'Sample' folder
        for (x, y, a, b) in faces:

            #Drawing a blue rectangle around face
            cv2.rectangle(img, (x, y), (x+a, y+b), (255, 0, 0), 1)
            n += 1
            cv2.imshow("Window", img)
            cv2.imwrite("Sample/."+ str(_faceid) +"."+str(n)+".jpg", gray)

        #Closing when escape is pressed or when number of images stored is equal to 'sample_size'
        k = cv2.waitKey(100)
        if k == 27:
            break
        elif n >= sample_size:
            break

    #Releasing camera and closing opened windows
    cam.release()
    cv2.destroyAllWindows()

    #Training from the stored images
    train_faces()


