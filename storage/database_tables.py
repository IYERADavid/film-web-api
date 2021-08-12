import datetime
from flask_app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(321), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def serializable_json(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'email': self.email
        }
