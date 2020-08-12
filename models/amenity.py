#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from models.base_model import BaseModel


class Amenity(BaseModel):
    pass
    # __tablename__ = 'amenities'
    # name = Column(String(128), nullable=False)
    # place_amenities = relationship("")
