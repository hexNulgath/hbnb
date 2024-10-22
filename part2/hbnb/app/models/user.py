import part2.hbnb.app.models.baseModel as baseModel
import re


class User(baseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        if self.validate_name(first_name) and self.validate_name(last_name):
            self.first_name = first_name
            self.last_name = last_name
        if self.validate_email(email):
            self.email = email
        self.is_admin = is_admin
        self.places = []

        
    
    @staticmethod
    def validate_name(name):
        if name and len(name) > 50:
            raise ValueError("maximum length of 50 characters")
        return True 
    
    @staticmethod
    def validate_email(email):
        ## check if email is in db
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            raise ValueError("email not valid")