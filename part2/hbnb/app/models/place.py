from app.models.baseModel import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner_id, amenities, description=""):
        super().__init__()
        if self.validate_title(title):
            self.title = title
        if price >= 0:
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
        self.owner = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = [amenities]  # List to store related amenities

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
