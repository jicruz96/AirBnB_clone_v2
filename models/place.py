#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from models.review import Review
from models.amenity import Amenity


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship(
        "Review", cascade="all, delete-orphan", backref="place")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False, backref="place_amenities")

    @property
    def amenities(self):
        """ Gets amenities attribute """
        return self.amenity_ids

    @amenities.setter
    def amenities(self, obj):
        if obj.__class__.__name__ is "Amenity":
            self.amenity_ids.append(obj)
            # self.amenity_ids.append(obj.__dict__)

    @property
    def reviews(self):
        """ Gets reviews attribute """
        return self.reviews
