import re
from flask import Blueprint, make_response, jsonify, request

from app.models.model import Users
from werkzeug.exceptions import abort

error_pwd_validation_msg = 'Password must contain at least 6 characters, including Upper/Lowercase, special characters and numbers'

signup_blueprint = Blueprint('signup', __name__)
@signup_blueprint.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.json['username']
        try:
            if Users.objects.get(username=username):
                return make_response(jsonify({"username": username+' username already exists'}), 400)
        except Users.DoesNotExist:
            pass

        email = request.json['email']
        if email_validation(email) == None:
            return make_response(jsonify({"email_validation": email+' is not a valid email address'}), 400)

        password = request.json['password']
        if password_validation(password) == None:
            return make_response(jsonify({"password_validation": error_pwd_validation_msg}), 400)

        users = Users(username=username,
                      password=password,
                      name=request.json['name'],
                      email=email,
                      dob=request.json['dob'])
        users.save()
    except KeyError:
        abort(400)
    return make_response(jsonify({
        "success": 'User Created Successfully'
    }), 201)


# Utility method to validate the password
def password_validation(password):
    pwd_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pwd_pattern = re.compile(pwd_regex)
    password_regex_match = re.search(pwd_pattern, password)
    return password_regex_match

# Utility method to validate the email address
def email_validation(email):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email_pattern = re.compile(email_regex)
    email_regex_match = re.search(email_pattern, email)
    return email_regex_match
