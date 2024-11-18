from app.models.baseclass import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenity'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # Added primary_key=True
    name = db.Column(db.String(50), nullable=False)  # Set a maximum length constraint for the name

    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    @staticmethod
    def validate_name(name):
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name exceeds maximum length of 50 characters")
        return name
