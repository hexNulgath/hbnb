from app.models.baseclass import BaseModel
from app import db

class Place(BaseModel):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # Added primary_key=True
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)  # Removed default, as coordinates must be specified
    longitude = db.Column(db.Float, nullable=False)  # Same as above
    owner_id = db.Column(db.Integer, nullable=False)  # Added owner_id for ForeignKey (if applicable)

    def __init__(self, title, price, latitude, longitude, owner_id, description=""):
        super().__init__()
        self.title = self.validate_title(title)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id
        self.description = description
        self.amenities = []  # Initialize amenities as an empty list
        self.reviews = []  # Initialize reviews as an empty list

    @staticmethod
    def validate_title(title):
        if not title or len(title) > 100:
            raise ValueError("Title must not be empty and have a maximum length of 100 characters.")
        return title

    @staticmethod
    def validate_price(price):
        if price < 0:
            raise ValueError("Price must be a positive value.")
        return price

    @staticmethod
    def validate_latitude(latitude):
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    @staticmethod
    def validate_longitude(longitude):
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return longitude

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
