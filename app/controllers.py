from app.models import User
from flask import request
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

def post_user():
    try:
        username = request.json["username"]
        password = request.json["password"]
        username_pattern = r'^\w{3,32}$'
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,32}$'
        if not re.match(username_pattern, username):
            return {"success": False, "reason": "Provided username is not valid"}
        elif not re.match(password_pattern, password):
            return {"success": False, "reason": "Provided password is not valid"}
        elif username and password:
            hashed_password = bcrypt.generate_password_hash(password)
            result = User.post(username, hashed_password)
            if result["success"]:
                return {"success": True}
            elif result["reason"] == "Username already exist":
                return {"success": False, "reason": result["reason"]}
            else: 
                return {"success": False, "reason": "Server internal error"}
    except:
        return {"success": False, "reason": "Server internal error"}