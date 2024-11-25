from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app import db

# Association Table for Many-to-Many Relationship
place_amenity = Table('place_amenity',
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
)

class UserRepository(db.Model):
    __tablename__ = 'user_repository'
    id = Column(Integer, primary_key=True)
    places = relationship('PlaceRepository', backref='user', lazy='select')
    reviews = relationship('ReviewRepository', backref='user', lazy='select')

class PlaceRepository(db.Model):
    __tablename__ = 'place_repository'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_repository.id'), nullable=False)
    reviews = relationship('ReviewRepository', backref='place', lazy='select')
    amenities = relationship('AmenityRepository', secondary=place_amenity, lazy='subquery',
                              backref=db.backref('places', lazy='select'))

class ReviewRepository(db.Model):
    __tablename__ = 'review_repository'
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('place_repository.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user_repository.id'), nullable=False)

    # Add relationships
    place = relationship('PlaceRepository', backref='reviews', lazy='select')
    user = relationship('UserRepository', backref='reviews', lazy='select')

class AmenityRepository(db.Model):
    __tablename__ = 'amenities_repository'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
