from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app import db

# Association Table for Many-to-Many Relationship
place_amenity = db.Table('place_amenity',
    Column('place_id', Integer, ForeignKey('place_repository.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities_repository.id'), primary_key=True)
)

class UserRepository(db.Model):
    __tablename__ = 'user_repository'  # Table for users
    id = Column(Integer, primary_key=True)
    places = relationship('PlaceRepository', backref='user', lazy=True)  # Relationship to PlaceRepository
    reviews = relationship('ReviewRepository', backref='user', lazy=True)  # Relationship to ReviewRepository

class PlaceRepository(db.Model):
    __tablename__ = 'place_repository'  # Table for places
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_repository.id'), nullable=False)  # ForeignKey to UserRepository
    reviews = relationship('ReviewRepository', backref='place', lazy=True)  # Relationship to ReviewRepository
    amenities = relationship('Amenity', secondary=place_amenity, lazy='subquery',
                              backref=db.backref('places', lazy=True))  # Many-to-Many with Amenity

class ReviewRepository(db.Model):
    __tablename__ = 'review_repository'  # Table for reviews
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('place_repository.id'), nullable=False)  # ForeignKey to PlaceRepository
    user_id = Column(Integer, ForeignKey('user_repository.id'), nullable=False)  # ForeignKey to UserRepository

class Amenity(db.Model):
    __tablename__ = 'amenities_repository'  # Corrected Table Name
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
