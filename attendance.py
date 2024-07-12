import face_recognise
import database_management
import datetime

def get_address():

    x = datetime.datetime.now()

    #Storing and returning current date, time and respective table name
    current_time = "{} : {} : {}".format(x.hour, x.minute, x.second)
    current_date = "{}_{}_{}".format(x.day, x.month, x.year)
    table_name = 'Attendance_for_' + current_date
    return current_time, current_date, table_name


def record_attendance():

    #Retrieving current date, time and respective table name
    current_time, current_date, table_name = get_address()

    #Recognising face and retrieving data
    myresult = face_recognise.recognise_face(True)

    #Creating table for the current day attendance if it doesn't exist
    try:

        sql = "CREATE TABLE " + table_name +"(uid DECIMAL(2,0)  PRIMARY KEY, name VARCHAR(20) UNIQUE NOT NULL, attendance VARCHAR(30) DEFAULT 'Absent',time VARCHAR(20) DEFAULT 'Not Entered');"

        database_management.connect_to_database(sql, False)

    except:

         print("Table already exists")

    #Retrieving and inserting user id, Name from student details(primary_details)
    ins = "INSERT INTO " + table_name + "(uid, name) SELECT user_id, name FROM primary_details WHERE user_id NOT IN(SELECT uid FROM "+table_name+");"
    database_management.connect_to_database(ins, False)

    #Updating attendance into current day's attendance table
    upd = "UPDATE "+table_name+" SET attendance = 'Present', time = '{}' WHERE uid = {} AND attendance = 'Absent';".format(current_time, myresult[0])
    database_management.connect_to_database(upd, False)

    #Checking if attendance is already recorded and returns text accordingly
    stored_results = database_management.fetch_results(myresult[0],'uid', table_name)

    if(stored_results[3] == current_time):
        text = myresult[1] +", your attendance has been recorded on " + current_date +" at: "+current_time

    else:
        text = myresult[1] + ", your attendance has already been recorded"

    return text




