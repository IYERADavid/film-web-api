import os
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_app.export_variables import export_envs

export_envs()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['database_url']
app.config['JSON_SORT_KEYS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ["email_username"]
app.config['MAIL_PASSWORD'] = os.environ["email_password"]
app.config['MAIL_DEFAULT_SENDER'] = os.environ["email_username"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = basedir + "/../storage/uploads"
app.config['UPLOAD_FOLDER'] = upload_folder

mail = Mail(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})