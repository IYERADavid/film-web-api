from flask import jsonify,json, url_for, request, redirect, session
from flask_app import app
from storage.database_access import Userdatabaseclients
from flask_app.validations import Validations
from flask_app.auth import Auth


@app.route('/signup', methods=['POST'])
def signup():
    user_datas = request.form
    first_name_value = user_datas['first_name']
    last_name_value = user_datas['last_name']
    middle_name_value = user_datas['middle_name']
    email_value = user_datas['email']
    password_value = user_datas['password']

    errors = Validations.signup(
        first_name=first_name_value,last_name=last_name_value,
        middle_name=middle_name_value, email=email_value, password=password_value
    )
    if errors:
        response = { "status" : "input_errors",
        "body" : "Inputs not validating (invalid values that database can't except)"}
        return jsonify(response)
    
    user_email = Userdatabaseclients.check_if_email_exists(email_value)
    if user_email:
        response = { "status" : "email_exist_error",
        "body" : "The email you entered already exist"}
        return jsonify(response)

    user = Userdatabaseclients.add_new_user(
        first_name=first_name_value,last_name=last_name_value,
        middle_name=middle_name_value, email=email_value, password=password_value
    )
    response = { "status" : "success", "body" : user}
    return jsonify(response)

@app.route('/signin', methods=['POST'])
def signin():
    user_datas = request.form
    email_value = user_datas['email']
    password_value = user_datas['password']

    errors = Validations.signin(email=email_value, password=password_value)
    if errors:
        response = { "status" : "input_errors",
        "body" : "Inputs not validating (invalid values that database can't except)"}
        return jsonify(response)

    user_email = Userdatabaseclients.check_if_email_exists(email_value)
    if user_email:
        user = Userdatabaseclients.login_user(
            email=email_value, password=password_value)
        if user:
            token = Auth.generate_token(user_id=user['user_id'])
            response = { "status" : "success", "body" : {"user" : user , "access_token" : token} }
            return jsonify(response)
    
    response = { "status" : "invalid_credentials", "body" : "The email or password you entered is invalid"}
    return jsonify(response)


@app.route('/home', methods=['GET'])
@Auth.require_login
def home(user_id):
    user = Userdatabaseclients.get_user(user_id=user_id)
    response = { "status" : "success", "body" : user}
    return jsonify(response)
