import os
from flask_app.validations import Validations

class Test_validations:

    @staticmethod
    def test_signup():
        errors = Validations.signup(
            first_name="f_nam", last_name="last_name",
            middle_name="m_name", email="test@gmail.com",
            password="testing"
        )
        assert errors == False

    @staticmethod
    def test_signin():
        errors = Validations.signin(
            email="test@gmail.com",password="testing"
        )
        assert errors == False

    @staticmethod
    def test_reset_password():
        errors = Validations.reset_password(email="test@gmail.com")
        assert errors == False

    @staticmethod
    def test_new_password():
        errors = Validations.new_password(password="testing")
        assert errors == False

    @staticmethod
    def test_user_profile():
        basedir = os.path.abspath(os.path.dirname(__file__))
        real_file =  open(basedir+"/media/download.jpeg", "r")
        testing_profile = { "filename" : real_file.name }
        errors = Validations.user_profile(profile=testing_profile)
        assert errors == False 
