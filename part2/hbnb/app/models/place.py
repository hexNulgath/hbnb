from app.models.baseModel import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        super().__init__()
        if self.validate_title(title):
            self.title = title
        if price > 0:
            self.price = price
        else:
            raise ValueError("price must be a positive value")
        if -180 < longitude < 180:
            self.longitude = longitude
        else:
            raise ValueError("longitude invalid")
        if -90 < latitude < 90:
            self.latitude = latitude
        else:
            raise ValueError("latitude invalid")
        self.description = description
        # Check if owner is a valid User instance
        if isinstance(owner, User):
            self.owner = owner
        else:
            raise ValueError("invalid user")
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        owner.add_place(self)

    @staticmethod
    def validate_title(title):
        if title and len(title) > 100:
            raise ValueError("maximum length of 100 characters")
        return True 
    
    def add_amenities(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
