from app.models.baseclass import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenity'
    id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        super().__init__()
        if self.validate_name(name):
            self.name = name

    @staticmethod
    def validate_name(name):
        if name and len(name) > 50:
            raise ValueError("maximum length of 50 characters")
        return True
