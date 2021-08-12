import os
from flask import Flask
from flask_app.export_variables import export_envs

export_envs()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('database_url')
app.config['JSON_SORT_KEYS'] = False