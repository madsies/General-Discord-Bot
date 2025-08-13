import json
import mysql.connector
from mysql.connector import Error
from pathlib import Path

with open(Path(__file__).parent / "resources/data.json", "r", encoding="utf-8") as f:
    CONFIG_DATA = json.load(f)

def create_connection(host_name : str, user_name : str, user_password : str, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

con = create_connection("localhost", "root", "","disc_yukari")

create_database(con, "CREATE DATABASE YukariDatabase")