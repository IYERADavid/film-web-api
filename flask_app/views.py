import os
from flask import jsonify,json, url_for, request, redirect, session
from flask_app import app, mail
from storage.database_access import Userdatabaseclients
from flask_app.validations import Validations
from flask_app.auth import Auth
from flask_mail import Message


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
    
    user_email = Userdatabaseclients.check_if_email_exists(email=email_value)
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

    user_email = Userdatabaseclients.check_if_email_exists(email=email_value)
    if user_email:
        user = Userdatabaseclients.login_user(
            email=email_value, password=password_value)
        if user:
            token = Auth.generate_login_token(user_id=user['user_id'])
            response = { "status" : "success", "body" : {"user" : user , "access_token" : token} }
            return jsonify(response)

    response = { "status" : "invalid_credentials", "body" : "The email or password you entered is invalid"}
    return jsonify(response)

@app.route("/reset_password", methods=['POST'])
def reset_password():
    password_reset_url = request.headers['password_reset_url']
    user_data = request.form
    email_value = user_data['email']

    error = Validations.reset_password(email=email_value)
    if error:
        response = { "status" : "input_errors",
        "body" : "Inputs not validating (invalid values that database can't except)"}
        return jsonify(response)

    user = Userdatabaseclients.check_if_email_exists(email=email_value)
    if user:
        token = Auth.generate_passwordreset_token(email=email_value)
        route_url_with_token = password_reset_url + token
        basedir = os.path.abspath(os.path.dirname(__file__))
        with open(basedir+'/email.html', 'r') as f:
            file_data = f.read().format(route_url_with_token)
        msg = Message(subject="Change password", recipients=[email_value])
        msg.html = file_data
        mail.send(msg)
        response = { "status" : "success", "body": "Check your email inbox to confirm password reset"}
        return jsonify(response)

    response = { "status" : "invalid_email", "body" : "The email you entered is invalid"}
    return jsonify(response)


@app.route("/new_password/<token>", methods=['GET', 'POST'])
def new_password(token):
    token = bytes(token,'utf-8')
    token_value = Auth.verify_token(token=token)
    if token_value:
        if request.method == "POST":
            user_data = request.form
            password_value = user_data['password']

            error = Validations.new_password(password=password_value)
            if error:
                response = { "status" : "input_errors",
                "body" : "Inputs not validating (invalid values that database can't except)"}
                return jsonify(response)
            user = Userdatabaseclients.change_password(email=token_value["email"], password=password_value)
            response = { "status" : "success", "body" : "You have successful changed your password" }
            return jsonify(response)

        response = { "status" : "success", "body" : "Now you are allowed to reset your password" }
        return jsonify(response)

    response = { "status" : "invalid_token", "body" : "The token you send is invalid" }
    return jsonify(response)
    

@app.route('/home', methods=['GET'])
@Auth.require_login
def home(user_id):
    user = Userdatabaseclients.get_user(user_id=user_id)
    response = { "status" : "success", "body" : user}
    return jsonify(response)
