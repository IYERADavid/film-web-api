import os
from flask import jsonify,json, url_for, request, redirect, session, \
    send_from_directory
from flask_app import app, mail
from storage.database_access import Userdatabaseclients
from flask_app.validations import Validations
from flask_app.auth import Auth
from flask_mail import Message
from werkzeug.utils import secure_filename


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
    email_value = request.form['email']

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
            password_value = request.form['password']

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
    

@app.route('/home')
@Auth.require_login
def home(user_id):
    user = Userdatabaseclients.get_user(user_id=user_id)
    videos = Userdatabaseclients.uploaded_videos()
    if request.method == "POST":
        video_name = request.form['movie_name']
        videos = Userdatabaseclients.videos_with_name(video_name)
        response = { "status" : "success", "body" : { "uploaded_videos": videos , "user_data": user}}

    response = { "status" : "success", "body" : { "videos_list": videos , "user_data": user}}
    return jsonify(response)

@app.route('/profile', methods=['GET','POST'])
@Auth.require_login
def user_profile(user_id):
    if request.method == "POST":
        allowed_file_ext = ['jpg','jpeg','png','gif','tiff','psd','al','raw']
        profile = request.files["profile_photo"]
        profile_name = secure_filename(profile.filename)
        profile_extension = profile_name.rsplit('.', 1)[1].lower()
        if profile_extension in allowed_file_ext:
            user_data = Userdatabaseclients.update_profile(
                user_id=user_id,profile_name=profile_name,
                profile=profile,upload_path=app.config['UPLOAD_FOLDER']
            )
            response = { "status" : "success","body" : { "user_data" : user_data} }
            return jsonify(response)
        response = { "status" : "invalid_extension",
        "body" : "Your file extension is not allowed" }
        return jsonify(response)
    user_data = Userdatabaseclients.get_user(user_id=user_id)
    response = { "status" : "success", "body" : { "user_data" : user_data} }
    return jsonify(response)

@app.route('/delete/profile')
def remove_profile(user_id):
    user_data = Userdatabaseclients.remove_profile(
        user_id=user_id, upload_path=app.config['UPLOAD_FOLDER']
    )
    if not user_data:
        response = { "status" : "invalid_profile",
        "body" : "You already haven't any profile set" }
        return jsonify(response)
 
    response = { "status" : "success", "body" : { "user_data" : user_data} }
    return jsonify(response)

@app.route('/home/watch-movies-Genre-<genre>')
@Auth.require_login
def videos_genre(genre):
    videos = Userdatabaseclients.videos_with_genre(genre=genre)
    response = { "status" : "success", "body" : { "videos_list": videos}}
    return jsonify(response)

@app.route('/home/watch-movies-Year-<year>')
@Auth.require_login
def videos_year(year):
    videos = Userdatabaseclients.videos_with_year(year=year)
    response = { "status" : "success", "body" : { "videos_list": videos}}
    return jsonify(response)

@app.route('/home/watch-movies-Language-<language>')
@Auth.require_login
def videos_language(language):
    videos = Userdatabaseclients.videos_with_language(language=language)
    response = { "status" : "success", "body" : { "videos_list": videos}}
    return jsonify(response)

@app.route('/view_file/<filename>')
@Auth.require_login
def view_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/recent_movies')
@Auth.require_login
def recent_videos():
    videos = Userdatabaseclients.recent_new_videos()
    response = { "status" : "success", "body" : { "videos_list": videos}}
    return jsonify(response)
