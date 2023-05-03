from mysql.connector import Error
from app.db import pool
connection_pool = pool()

class User():
    def post(username, password):
        try:
            # get cursor from connection pool
            with connection_pool.get_connection() as connection_object, connection_object.cursor() as my_cursor:
                check_username_query = "SELECT user_id FROM Users WHERE username = %s"
                my_cursor.execute(check_username_query, [username])
                check_username_result = my_cursor.fetchone()
                # check if the username exist
                if check_username_result == None: 
                    insert_query = "INSERT INTO Users (username, password) VALUES (%s, %s);"
                    my_cursor.execute(insert_query, (username, password))
                    connection_object.commit()
                    return {"success": True}
                else:
                    return {"success": False, "reason": "Username already exist"}
        except Error as e:
            # handle MySQL error
            return {"success": False, "reason": str(e)}
        
    def get(username):
        try:
            # get cursor from connection pool
            with connection_pool.get_connection() as connection_object, connection_object.cursor() as my_cursor:
                check_query = "SELECT * FROM Users WHERE username = %s"
                my_cursor.execute(check_query, [username])
                check_result = my_cursor.fetchone()
                # check if the username registered before
                if check_result == None: 
                    return {"success": False, "reason": "Username not registered"}
                else:
                    row_headers = [x[0] for x in my_cursor.description]
                    json_result = dict(zip(row_headers, check_result))
                    return {"success": True, "data": json_result}
        except Error as e:
            # handle MySQL error
            return {"success": False, "reason": str(e)}