from app.db import connection_pool

class User():
    def validate(username, password):
        try:
            pass
        except:
            pass
        finally:
            pass

    def get(username, password):
        try:
            pass
        except:
            pass
        finally:
            pass

    def post(username, password):
        try:
            connection_object = connection_pool.get_connection()
            my_cursor = connection_object.cursor()
            check_username_query = "SELECT user_id FROM Users WHERE username = %s"
            my_cursor.execute(check_username_query, [username])
            check_username_result = my_cursor.fetchone()
            if check_username_result == None: 
                insert_query = "INSERT INTO Users (username, password) VALUES (%s, %s);"
                my_cursor.execute(insert_query, (username, password))
                connection_object.commit()
                return {"success": True}
            else:
                return {"success": False, "reason": "Username already exist"}
        except:
            return {"success": False, "reason": "Server internal error"}
        finally:
            my_cursor.close()
            connection_object.close()