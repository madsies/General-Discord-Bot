import json
import mysql.connector
from mysql.connector import Error
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

with open(Path(__file__).parent / "resources/data.json", "r", encoding="utf-8") as f:
    CONFIG_DATA = json.load(f)

class MySQLDatabase():
    def __init__(self, host_name : str, user_name : str, user_password : str):
        self._db_name : str = "YukariDatabase"
        self._host_name : str = host_name
        self._user_name : str = user_name
        self._user_password : str = user_password
        self.create_database()
        self.connection = self.create_connection()

    def create_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self._host_name,
                user=self._user_name,
                passwd=self._user_password,
                database=self._db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def create_database(self):
        
        try:
            connection = mysql.connector.connect(
                host=self._host_name,
                user=self._user_name,
                passwd=self._user_password,
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE YukariDatabase")
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def query(self, query : str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        self.connection.commit()
        return data

    def add_user(self, user):
        ID = user.id
        username = user.name
        sql = """INSERT IGNORE INTO users (id, username, messages) VALUES (%s, %s, 0);"""
        vals = (ID, username)
        self.queryTuple(sql, vals)

    def queryTuple(self, sql, val):
        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        data = cursor.fetchall()
        cursor.close()
        self.connection.commit()
        return data

DATABASE_REF = MySQLDatabase("localhost", "root", os.environ.get('MYSQL_PASS'))