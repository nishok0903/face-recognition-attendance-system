import cv2 #opencv
import os
import mysql.connector as sqlator
import database_management

def recognise_face(is_returning):

    nth_file =  0
    files = os.listdir('Sample')
    current_face = "Not defined"

    #Checks if trainer exists
    if (os.path.isfile("Trainer/trainer.yml")):

        #Reading saved data
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Trainer/trainer.yml")
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        font = cv2.FONT_HERSHEY_COMPLEX
        cam = cv2.VideoCapture(0)

        #Recognising face
        while(True):

            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            #Predicting the face and storing identity and confidence
            for (x, y, a, b) in faces:

                # Drawing a blue rectangle around face
                cv2.rectangle(img, (x, y), (x+a, y+b), (255, 0, 0), 1)
                identity, confidence = recognizer.predict(gray[y:y+a,x:x+b])

                #Checking if the recognised face is similar enough
                if confidence < 55:

                   if current_face != str(identity) or current_face == "Not defined":

                       #Retrieving data of matched face
                       myresult = database_management.fetch_results(identity, "user_id", "primary_details")
                       current_face = str(identity)

                       #Returning data if it has to return
                       if is_returning:
                           return myresult
                       else:
                           pass

                   name = myresult[1]
                   age = myresult[2]

                else:
                    name = "UNKNOWN"
                    age = "UNKNOWN"

                #Displaying retrieved data
                cv2.putText(img, "Name : {} Confidence: {}".format(name, confidence), (x-100,y+b), font, 1, (0,255,0), 2)
                cv2.putText(img, "Age : {}".format(age), (x-100, y + b + 40), font, 1, (0, 255, 0), 2)
            cv2.imshow("Window", img)

            #Closing when escape is pressed
            k = cv2.waitKey(100)
            if k == 27:
                break

        # Releasing camera and closing opened windows
        cam.release()
        cv2.destroyAllWindows()

    else:

        print("No faces trained")

