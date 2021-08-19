
class Validations:

    @staticmethod
    def signup(first_name, last_name, middle_name, email, password):
        errors = 0
        if first_name == "":
            errors += 1 
        elif len(first_name) > 25:
            errors += 1

        if last_name == "":
            errors += 1
        elif len(last_name) > 25:
            errors += 1

        if len(middle_name) > 15:
            errors += 1

        if email == "":
            errors += 1
        elif len(email) > 321:
            errors += 1

        if password == "":
            errors += 1
        elif len(password) > 80:
            errors += 1
        
        if errors > 0:
            return True
        return False

    @staticmethod
    def signin(email, password):
        errors = 0
        if email == "":
            errors += 1
        elif len(email) > 321:
            errors += 1

        if password == "":
            errors += 1
        elif len(password) > 80:
            errors += 1

        if errors > 0:
            return True
        return False
    
    @staticmethod
    def reset_password(email):
        error = 0
        if email == "":
            error += 1
        elif len(email) > 321:
            error += 1
        
        if error > 0:
            return True
        return False

    @staticmethod
    def new_password(password):
        error = 0
        if password == "":
            error += 1
        elif len(password) > 80:
            error += 1

        if error > 0:
            return True
        return False
