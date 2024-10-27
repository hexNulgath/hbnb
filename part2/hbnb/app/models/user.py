from app.models.baseModel import BaseModel
import re

MAX_NAME_LENGTH = 50

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []
    
    @staticmethod
    def validate_name(name):
        if not name or len(name) > MAX_NAME_LENGTH or len(name) < 1:
            raise ValueError(f"Name must be between 1 and {MAX_NAME_LENGTH} characters")
        return name
    
    @staticmethod
    def validate_email(email):
        """Check if email format is valid."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return email
        raise ValueError("Email is not valid")

    def add_review(self, review):
        """Link a review to a user."""
        self.reviews.append(review)

    def add_place(self, place):
        """Add an owned place to a user."""
        self.places.append(place)
