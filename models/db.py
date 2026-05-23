import mysql.connector
from flask import current_app

def get_db_connection():
    # current_app nos permite leer la configuración desde app.py
    connection = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB']
    )
    return connection
