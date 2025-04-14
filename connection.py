import mysql.connector
import os
from dotenv import load_dotenv

class DatabaseConnection: 
    def __init__ (self):
        self.db = None
        self.cursor = None

        try: 
            self.db = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = os.getenv("DB_NAME")
            )
            
            if self.db.is_connected():
                print("Database connected successfully!")
            else:
                print("Connection failed")

        except mysql.connector.Error as err:
            print(f"Connection failed: {err}")

        self.cursor = self.db.cursor()

    def get_connection(self):
        return self.db, self.cursor

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
            print("Database connection closed.")