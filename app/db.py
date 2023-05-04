import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

def pool():
    try:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name = os.getenv("pool_name"),
            pool_size = 5,
            pool_reset_session = True,
            host = os.getenv("db_host"),
            user = os.getenv("db_user"),
            password = os.getenv("db_password"),
            database = os.getenv("db_name")
        )
        return connection_pool
    except Error as e:
        print(f"Error connecting to database: {e}")


