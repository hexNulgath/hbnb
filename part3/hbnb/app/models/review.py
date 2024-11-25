from app.models.baseclass import BaseModel
from app import db



class Review(BaseModel):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  # Primary Key
    text = db.Column(db.String(500), nullable=False)  # Max length constraint for text
    rating = db.Column(db.Integer, nullable=True)  # Fixed typo in db.Integer
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)  # Foreign Key to Place
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign Key to User
    user = db.relationship('users', backref='review', lazy=True)
    place = db.relationship('places', backref='review', lazy=True)
    

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        
        # Validate text
        self.text = self.validate_text(text)
        
        # Validate rating
        self.rating = self.validate_rating(rating)
        
        # Validate place and user existence
        self.place_id = self.validate_place(place_id)
        self.user_id = self.validate_user(user_id)

    @staticmethod
    def validate_text(text):
        """Ensure text is not empty and within the allowed length."""
        if not text or text.strip() == "":
            raise ValueError("Text content is required.")
        if len(text) > 500:
            raise ValueError("Text exceeds maximum length of 500 characters.")
        return text

    @staticmethod
    def validate_rating(rating):
        """Ensure rating is between 1 and 5."""
        if rating is not None and (rating < 1 or rating > 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    def validate_user(self, user_id):
        """Check if the user exists in the database."""
        from app.services.facade import HBnBFacade  # Delayed import to avoid circular dependency
        facade = HBnBFacade()
        user = facade.get_user(user_id)
        if not user or 'error' in user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user_id

    def validate_place(self, place_id):
        """Check if the place exists in the database."""
        from app.services.facade import HBnBFacade  # Delayed import to avoid circular dependency
        facade = HBnBFacade()
        place = facade.get_place(place_id)
        if not place or 'error' in place:
            raise ValueError(f"Place with ID {place_id} not found.")
        return place_id
