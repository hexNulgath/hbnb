from app.models.baseModel import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if self.validate_name(first_name) and self.validate_name(last_name):
            self.first_name = first_name
            self.last_name = last_name
        if self.validate_email(email):
            self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []      
    
    @staticmethod
    def validate_name(name):
        if name and len(name) > 50:
            raise ValueError("maximum length of 50 characters")
        return True 
    
    @staticmethod
    def validate_email(email):
        """check if email format is valid format"""
        ## check if email is in db
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            raise ValueError("email not valid")

    def add_review(self, review):
        """Link a review to a user"""
        self.reviews.append(review)

    def add_place(self, place):
        """Add a owned place to a user"""
        self.places.append(place)
