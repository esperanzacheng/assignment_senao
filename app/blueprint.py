from flask import Blueprint, jsonify, make_response
from app.controllers import user_controller

user_blueprint = Blueprint('user_blueprint', __name__)
errors = Blueprint('error', __name__)
User = user_controller()

@user_blueprint.route('/api/user', methods=["POST"])
def user_signup():
    try:
        result = User.post_user()
        if result["success"]:
            return (jsonify(success = True), 201)
        elif ((result["reason"] == "Provided username is not valid") or 
            (result["reason"] == "Provided password is not valid") or 
            (result["reason"] == "Username already exist") or
            (result["reason"] == "Missing username or password input")):
            return (jsonify(success = False, reason = result["reason"]), 400)
        else:
            return (jsonify(success = False, reason = result["reason"]), 500)
    # handle built-in exception error
    except Exception as e:
        return (jsonify(success = False, reason = str(e)), 500)

@user_blueprint.route('/api/user', methods=["GET"])
def user_login():
    try:
        result = User.get_user()
        if result["success"]:
            return (jsonify(success = True), 200)
        elif ((result["reason"] == "Password is wrong") or 
              (result["reason"] == "Username not registered")):
            return (jsonify(success = False, reason = result["reason"]), 403)
        elif (result["reason"] == "Missing username or password input"):
            return (jsonify(success = False, reason = result["reason"]), 400)
        elif (result["reason"] == "Too many failed attempts"):
            response = make_response(jsonify(success = False, reason = "Too many failed attempts"), 429)
            response.headers['Retry-After'] = result["time"]
            return response
        else:
            return (jsonify(success = False, reason = result["reason"]), 500)
    # handle built-in exception error
    except Exception as e:
        return (jsonify(success = False, reason = str(e)), 500)

# handle unexpected server error
@errors.errorhandler(500)
def internal_error(e):
    return (jsonify(success = False, reason = str(e)), 500)