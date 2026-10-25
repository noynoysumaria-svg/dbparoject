import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sumaria@2627",
        database="students_enroll"
    )