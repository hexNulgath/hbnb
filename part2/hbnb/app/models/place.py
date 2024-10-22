import part2.hbnb.app.models.baseModel as baseModel
import part2.hbnb.app.models.user as User


class Place(baseModel):
    def __init__(self, title, price, latitude, longitude, owner, amenities, description=""):
        super().__init__()
        if self.validate_title(title):
            self.title = title
        if price > 0:
            self.price = price
        else:
            raise ValueError("price must be a positive value")
        if longitude > -180 and longitude < 180:
            self.longitude = longitude
        else:
            raise ValueError("longitude invalid")
        if latitude > -90 and latitude < 90:
            self.latitude = latitude
        else:
            raise ValueError("latitude invalid")
        self.description = description
        ## chack if user is in db
        if isinstance(owner, User):
            self.owner = owner
        else:
            raise ValueError("invalid user")
        self.amenities = []
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        owner.add_place(self)

    @staticmethod
    def validate_title(title):
        if title and len(title) > 100:
            raise ValueError("maximum length of 100 characters")
        return True 
    
    def add_amenities(self, amenity):
        self.amenity.append(amenity)

    def add_review(self, review):
    """Add a review to the place."""
        self.reviews.append(review)

