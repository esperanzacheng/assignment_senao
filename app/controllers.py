from app.models import User
from flask import request
from datetime import datetime, timedelta
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
failed_times = {} # a dict to store users' login failed total times within 1 min
timeout = timedelta(minutes=1) # set the login deny timeout to 1 min

class user_controller():

    # for username, password input validation, used in post_user() & get_user()
    @staticmethod
    def _input_validation(username, password):
        if username and password:
            username_pattern = r'^\w{3,32}$' # set within 3-32 char
            password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,32}$' # set within 8-32 char, should at least has 1 lower letter, 1 upper letter, 1 digit
            if not re.match(username_pattern, username):
                return {"success": False, "reason": "Provided username is not valid"}
            elif not re.match(password_pattern, password):
                return {"success": False, "reason": "Provided password is not valid"}
            else:
                return {"success": True}
        else:
            return {"success": False, "reason": "Missing username or password input"}

    def post_user(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
            validation = self._input_validation(username, password)
            if validation["success"]:
                hashed_password = bcrypt.generate_password_hash(password) # hash the password before store in the db
                result = User.post(username, hashed_password)
                if result["success"]:
                    return {"success": True}
                else:
                    return {"success": False, "reason": result["reason"]}
            else:
                return {"success": False, "reason": validation["reason"]}
        # handle error if validation or result index goes wrong
        except IndexError as e:
            return {"success": False, "reason": str(e)}

    # for login fail count, used in get_user()
    @staticmethod
    def _failed_counts(username):
        try:
            # check if this username is already in record
            if username in failed_times:
                failed_times[username]['count'] += 1
                # check if the login attempts is over 5 within this min
                if failed_times[username]['count'] >= 5:
                    last_time = failed_times[username]['timestamp'] # get the login attempt timestamp from the last time
                    # check if this user's wait time is longer than the assigned timeout (1 min)
                    if datetime.now() - last_time < timeout:
                        wait_time = (last_time + timeout - datetime.now()).total_seconds() # convert the wait time into sec
                        return {"overload": True, "reason": "Too many failed attempts", "time": wait_time}
                    else:
                        failed_times[username] = {'count': 1, 'timestamp': datetime.now()} # since this user served his/her timeout but failed to login again, reset the count to 1
                        return {"overload": False}
                else:
                    failed_times[username]['timestamp'] = datetime.now() # set the newest fail login timestamp to this time
            else:
                failed_times[username] = {'count': 1, 'timestamp': datetime.now()} # record this username in record, and set the count to 1

            return {"overload": False}
        # handle error if failed_times index goes wrong
        except IndexError as e:
            return {"overload": False}
    
    def put_user(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
            validation = self._input_validation(username, password)
            # check if the input is validated. If not, save the time to select in db
            if validation["success"]:
                result = User.put(username)
                # check if this username exist
                if result["success"]:
                    hashed_password = result["data"]["password"] # un-hash the password
                    check_password = bcrypt.check_password_hash(hashed_password, password) # check if the password match
                    if check_password:
                        failed_times.pop(username, None) # pop the fail record if login successfully
                        return {"success": True}
                    else:
                        failed_count_result = self._failed_counts(username)
                        # check if the fail time is over 5
                        if failed_count_result["overload"]:
                            return {"success": False, "reason": "Too many failed attempts", "time": failed_count_result["time"]}
                        else:
                            return {"success": False, "reason": "Password is wrong"}
                else: 
                    return {"success": False, "reason": result["reason"]}
            else:
                if validation["reason"] == "Provided username is not valid": # username is not validated, which means it is not registered
                    return {"success": False, "reason": "Username not registered"}
                elif validation["reason"] == "Missing username or password input":
                    return {"success": False, "reason": validation["reason"]}
                else: # wrong password input
                    failed_count_result = self._failed_counts(username)
                    if failed_count_result["overload"]:
                        return {"success": False, "reason": "Too many failed attempts", "time": failed_count_result["time"]}
                    else:
                        return {"success": False, "reason": "Password is wrong"}
        # handle error if failed_count_result, validation or result index goes wrong
        except IndexError as e:
            return {"success": False, "reason": str(e)}