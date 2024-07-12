from tkinter import *
import face_capture
import face_recognise
import delete_entry
import attendance
import database_management
import mysql.connector as sqlator

root = Tk()
text = ""
root.title("Attendance System")
root.columnconfigure(1, weight=1)
root.columnconfigure(0, weight=3)

try:
    db_connector = sqlator.connect(host="localhost", user="root", passwd="tiger")
    if db_connector.is_connected():
     print('Successfully connected to MySQL database')
    cursor = db_connector.cursor()
    cursor.execute("CREATE DATABASE face_recognition_attendance_system_project")
    cursor.execute("USE face_recognition_attendance_system_project")
    cursor.execute("CREATE TABLE primary_details(user_id decimal(2,0) PRIMARY KEY, Name varchar(20) NOT NULL, Age decimal(2,0))")
    db_connector.close()
except:

    print("Database already exists")

def display_table():

    try:

        # Displaying table
        current_time, current_date, table_name = attendance.get_address()
        given_date = date.get().replace("/","_")
        if given_date != '':
                table = 'Attendance_for_' + given_date
        else:
            table = table_name


        db_connector = sqlator.connect(host="localhost", user="root", passwd="tiger", database="face_recognition_attendance_system_project")
        if db_connector.is_connected():
            print('Successfully connected to MySQL database')
        cursor = db_connector.cursor()

        sql = "SELECT * FROM " + table
        cursor.execute(sql)
        students = cursor.fetchall()
        labels = ["ID", "Name", "Attendance", "Time of Attendance"]

        window = Toplevel(root)
        window.title(table)

        for y in range(4):
            e = Label(window, text=labels[y])
            e.grid(row=0, column=y)

        i = 1
        col = 4
        iteration = 0
        for student in students:
            for j in range(col):

                e = Label(window,width=10, text=student[j])
                e.grid(row=i, column=j)
            i = i + 1

    #Displays "Nobody is present" when no table is created
    except:
        global text
        text = "Nobody is present" if given_date == '' else "No records available regarding the specified value"
        mesLabel.config(text=text)
        return

def details_recorded():

    try:
        i = int(id.get())
        n = name.get()
        a = int(age.get())
        face_capture.capture_face(i,n,a)
        global text
        text = "Your details has been recorded"
        mesLabel.config(text = text)
        name.delete(0,END)
        age.delete(0, END)
        id.delete(0, END)


    except Exception as e:
        print(e)
        # print("Input appropriate values...")

def delete_record():

    i = int(id.get())
    delete_entry.delete_entry(i)

def recognise_face():

    face_recognise.recognise_face(False)

def attendance_text():

    global text
    text = attendance.record_attendance()
    mesLabel.config(text=text)

#label
nameLabel = Label(root, text="Name :", width = 40)
nameLabel.grid(row = 0, column = 0, sticky=NSEW)

name = Entry(root, width=50)
name.grid(row = 0, column = 1, sticky=NSEW)

#label
ageLabel = Label(root, text="Age :")
ageLabel.grid(row = 1, column = 0, sticky=NSEW)

age = Entry(root, width=50)
age.grid(row = 1, column = 1, sticky=NSEW)

#label
idLabel = Label(root, text="User ID:")
idLabel.grid(row = 2, column = 0, sticky=NSEW)

id = Entry(root, width=50)
id.grid(row = 2, column = 1, sticky=NSEW)

# add empty label in row 0 and column 0
l0 = Label(root, text='')
l0.grid(column=0, row=5, columnspan =2)

#label
dateLabel = Label(root, text="Date: (e.g., 24/8/2021)")
dateLabel.grid(row = 6, column = 0, sticky=NSEW)

date = Entry(root, width=50)
date.grid(row = 6, column = 1, sticky=NSEW)

myButton = Button(root, text = "Record Details", command = details_recorded)
myButton.grid(row = 3, column =0, sticky=NSEW)

recogniseButton = Button(root, text = "Recognise", command = recognise_face)
recogniseButton.grid(row = 3, column =1, sticky=NSEW)

recordAttendanceButton = Button(root, text = "Record Attendance", command = attendance_text)
recordAttendanceButton.grid(row = 4, column =0, sticky=NSEW)

deleteRecordButton = Button(root, text = "Delete Record", command = delete_record)
deleteRecordButton.grid(row = 4, column =1, sticky=NSEW)

exitButton = Button(root, text = "Exit", command = root.destroy)
exitButton.grid(row = 8, column =0, sticky=NSEW)

displayButton = Button(root, text = "Display", command = display_table)
displayButton.grid(row = 8, column =1, sticky=NSEW)

mesLabel = Label(root, text = "")
mesLabel.grid(row = 9, column =0, columnspan = 2, sticky=NSEW)

root.mainloop()