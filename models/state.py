#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel, Column, String
from models.city import City
from os import environ


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan",
                          backref="state", passive_deletes=True)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':

        @property
        def cities(self):
            """ Cities getter """
            return self.cities
    else:
        @property
        def cities(self):
            """ Cities getter """
            from models import storage
            from models.city import City
            my_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    my_cities.append(city)
            return my_cities
