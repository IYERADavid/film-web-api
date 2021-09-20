import jwt
import datetime
from flask_app import app
import flask_app.auth as authatications

class Test_Auth:

    @staticmethod
    def test_generate_login_token(mocker):
        user_id = 'user_login_token'
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        new_token = authatications.Auth.generate_login_token(user_id=user_id, exp_time=exp_time)
        token = bytes(new_token,'utf-8')
        try:
            token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
        except:
            token_data = None       
        assert user_id == token_data['user_id']

    @staticmethod
    def test_generate_passwordreset_token(mocker):
        user_email = "testing@gmal.com"
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        new_token = authatications.Auth.generate_passwordreset_token(email=user_email, exp_time=exp_time)
        token = bytes(new_token,'utf-8')
        try:
            token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
        except:
            token_data = None
        assert user_email == token_data['email']

    @staticmethod
    def test_verify_token():

        def test_with_valid_token():
            user_email = "testingverifier@gmail.com"
            exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
            new_token = authatications.Auth.generate_passwordreset_token(email=user_email, exp_time=exp_time)
            token = bytes(new_token,'utf-8')
            token_value = authatications.Auth.verify_token(token=token)
            assert user_email == token_value['email']

        test_with_valid_token()
        
        def test_with_invalid_token():
            token_value = authatications.Auth.verify_token(token="some wrong token")
            assert None == token_value

        test_with_invalid_token()
    
    @staticmethod
    def test_require_login(mocker):

        def test_with_valid_request_headers():
            user_id = 'vendor videos service center'
            exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
            new_token = authatications.Auth.generate_login_token(user_id=user_id, exp_time=exp_time)
            """
            class Bunch:
                def __init__(self,**kw):
                    self.__dict__.update(kw)
            request = Bunch(headers={'Authorization': new_token})
            """
            request={'headers': {'Authorization': new_token}}
            mocker.patch.object(authatications, 'request', request)
            def sample_func(user_id):
                return user_id
            
            decorated_sample_func = authatications.Auth.require_login(sample_func)
            assert user_id == decorated_sample_func()

        test_with_valid_request_headers()

        def test_with_invalid_request_headers():

            def jsonify(data):
                return data
            request={'headers': {'Authorization': "some wrong token"}}
            mocker.patch.object(authatications, 'jsonify', jsonify)
            mocker.patch.object(authatications, 'request', request)
            def sample_func(user_id):
                # un reachable codes
                return user_id
            
            expected_result = { "status" : "login_required", "body" : "You must login to continue" }
            decorated_sample_func = authatications.Auth.require_login(sample_func)
            assert expected_result == decorated_sample_func()
        
        test_with_invalid_request_headers()
