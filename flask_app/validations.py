from werkzeug.utils import secure_filename

class Validations:

    @staticmethod
    def signup(first_name, last_name, middle_name, email, password):
        if (   
                first_name == "" or 
                len(first_name) > 25 or 
                last_name == "" or 
                len(last_name) > 25 or 
                len(middle_name) > 15 or 
                email == "" or 
                len(email) > 321 or 
                password == "" or 
                len(password) > 80
            ):
            return True
        return False

    @staticmethod
    def signin(email, password):
        if (
                email == "" or 
                len(email) > 321 or 
                password == "" or 
                len(password) > 80
            ):
            return True
        return False

    @staticmethod
    def reset_password(email):
        if email == "" or len(email) > 321:
            return True
        return False

    @staticmethod
    def new_password(password):
        if password == "" or len(password) > 80:
            return True
        return False

    @staticmethod
    def user_profile(profile):
        if not profile.filename == '':
            allowed_file_ext = ['jpg','jpeg','png','gif','tiff','psd','al','raw']
            profile_name = secure_filename(profile.filename)
            profile_extension = profile_name.rsplit('.', 1)[1].lower()
            if profile_extension in allowed_file_ext:
                return False
        return True
