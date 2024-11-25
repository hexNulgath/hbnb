import re
from flask_bcrypt import bcrypt, Bcrypt
from app import db, bcrypt
from .baseclass import BaseModel
from sqlalchemy.orm import validates, relationship

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique=True) 
    password = db.Column(db.String(128), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False) 
    places = relationship('Place', backref='User', lazy=True)
    reviews = relationship('review', backref='user', lazy=True)


    @staticmethod
    @validates('email')
    def validate_email(email):
        """Check if email format is valid."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return email
        raise ValueError("Invalid email format")

    def serializar_usuario(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    

    def add_review(self, review):
        """Link a review to the user."""
        self.reviews.append(review)
        db.session.add(self)
        db.session.commit()

    def add_place(self, place):
        """Add a place to the user."""
        self.places.append(place)
        db.session.add(self)
        db.session.commit()
