from passlib.hash import sha256_crypt
from storage.database_tables import db, User

class Userdatabaseclients:

    @staticmethod
    def check_if_email_exists(email):
        user = User.query.filter_by(email=email).scalar() is not None
        return user

    @staticmethod
    def add_new_user(first_name, last_name, middle_name, email, password):
        hashed_password = sha256_crypt.encrypt(password)
        new_user = User(
            first_name=first_name, last_name=last_name,middle_name=middle_name,
            email=email, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.serializable_json()

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).one()
        if sha256_crypt.verify(password, user.password):
            return user.serializable_json()
        return None

    @staticmethod
    def get_user(user_id):
        user = User.query.filter_by(user_id=user_id).one()
        return user.serializable_json()