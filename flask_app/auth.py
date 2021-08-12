import jwt
import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from flask import request, jsonify
from flask_app import app

class Auth:

    @staticmethod
    def generate_token(user_id):
        token = jwt.encode({"user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)},
        app.config['SECRET_KEY'], algorithm="HS256")
        return token.decode('utf-8')
 
    @staticmethod
    def verify_token(token):
        try:
            token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
            return token_data
        except:
            return None

    @classmethod
    def require_login(self, func):
        @wraps(func)
        def secure_function(*args, **kwargs):
            user_token = request.headers.get('Authorization')
            if user_token:
                token = bytes(user_token,'utf-8')
                token_value = self.verify_token(token=token)
                if token_value:
                    kwargs['user_id'] = token_value["user_id"]
                    return func(*args,**kwargs)
            response = { "status" : "login_required", "body" : "You must login to continue" }
            return jsonify(response)

        return secure_function