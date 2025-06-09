import mysql.connector # type: ignore

def get_connection():
    return mysql.connector.connect(
        host="l****",
        user="****",       
        password="****",   
        database="****"
    )
