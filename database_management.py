import mysql.connector as sqlator

def connect_to_database(sql, is_returning):

    #Connecting to the database
    db_connector = sqlator.connect(host="localhost", user="root", passwd="tiger", database="face_recognition_attendance_system_project")
    if db_connector.is_connected():
        print('Successfully connected to MySQL database')
    cursor = db_connector.cursor()
    cursor.execute(sql)

    #Checking if something has to be returned
    if is_returning:

        #returning the result
        myresult = cursor.fetchone()
        db_connector.commit()
        return myresult
    else:
        db_connector.commit()

def fetch_results(identity, column_to_check, table_name):

    #Fetching the result from the given table where the value of the given column is the given value
    sql = "SELECT * FROM "+table_name+" WHERE "+column_to_check+" = {}".format(identity)
    myresult = connect_to_database(sql, True)
    return myresult




