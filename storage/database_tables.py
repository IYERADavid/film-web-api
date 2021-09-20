import os
import datetime
from flask_app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
default_pic = os.environ["user_profile"]

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(321), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_picture = db.Column(db.String, default=default_pic, nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def serializable_json(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'email': self.email,
            'profile_picture': self.profile_picture
        }

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    video_photo = db.Column(db.String, unique=True, nullable=False)
    video_filename = db.Column(db.String, unique=True, nullable=False)
    video_name = db.Column(db.String(100), nullable=False)
    video_description = db.Column(db.String(3000), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    video_year = db.Column(db.Integer, nullable=False)
    video_genre = db.Column(db.String(30), nullable=False)
    video_language = db.Column(db.String(30), nullable=False)
    video_time_saved = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def serializable_json(self):
        return {
            'video_id': self.video_id,
            'video_photo': self.video_photo,
            'video_filename': self.video_filename,
            'video_name': self.video_name,
            'video_description': self.video_description,
            'active': self.active,
            'video_year': self.video_year,
            'video_genre': self.video_genre,
            'video_language': self.video_language
        }
