from flask import Blueprint, jsonify
from app.controllers import post_user

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/api/user', methods=["POST"])
def user_signup():
    result = post_user()
    if result["success"]:
        return (jsonify(success = True), 201)
    elif (result["reason"] == "Provided username is not valid") or (result["reason"] == "Provided password is not valid") or (result["reason"] == "Username already exist"):
        return (jsonify(success = False, reason = result["reason"]), 400)
    else:
        return (jsonify(success = False, reason = result["reason"]), 500)
    