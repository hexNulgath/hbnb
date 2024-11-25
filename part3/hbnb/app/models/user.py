import re
from app import db, bcrypt
from .baseclass import BaseModel
from sqlalchemy.orm import validates, relationship

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique=True) 
    _password = db.Column("password", db.String(128), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False) 

    @validates('email')
    def validate_email(self, key, email):
        """Check if email format is valid."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return email
        raise ValueError("Invalid email format")

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, raw_password):
        self._password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self._password, password)

    def serialize_user(self):
        """Serialize the user object."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def add_review(self, review):
        """Link a review to the user."""
        try:
            self.reviews.append(review)
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to add review: {e}")

    def add_place(self, place):
        """Add a place to the user."""
        try:
            self.places.append(place)
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to add place: {e}")
