import mysql.connector as sqlator
import os #operating system
import face_capture
import cv2
import numpy as np
import database_management

def delete_entry(_faceid):

    #Deleting student details whose face ID is the given face ID
    sql = "DELETE FROM primary_details WHERE user_id = {}".format(_faceid)
    database_management.connect_to_database(sql, False)

    path =  "Sample"
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    #Deleting images from 'Sample' folder of the given face ID
    for imagePath in imagePaths:

        #Retrieving face ID from image paths
        id = int(os.path.split(imagePath)[-1].split(".")[-3])

        #Deleting images if their face ID is equal to the given face ID
        if(id == _faceid):
            os.remove(imagePath)

    #Deleting trainer file if it exists
    if(os.path.isfile("Trainer/trainer.yml")):
        os.remove("Trainer/trainer.yml")

    dir = os.listdir(path)

    #Training from the stored images if 'Sample' folder contains images
    if len(dir) != 0:
        face_capture.train_faces()

    #Prints message if 'Sample' folder is empty
    else:
        print("No samples available to train")

