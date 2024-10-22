from app.models.baseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()  # Call the BaseModel constructor
        if self.validate_name(name):
            self.name = name

    @staticmethod
    def validate_name(name):
        if name and len(name) > 50:
            raise ValueError("maximum length of 50 characters")
        return True
