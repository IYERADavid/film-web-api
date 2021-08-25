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
    def test_new_password(password="testing"):
        errors = Validations.new_password(password="testing")
        assert errors == False
