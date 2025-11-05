# db_config.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",      # change if needed
        user="root",           # your MySQL username
        password="blue_wings_22",  # your MySQL password
        database="vehicle_rental"  # your DB name
    )
