#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from models import storage
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.save()  # <- Added this here?
        else:
            isoformat = "%Y-%m-%dT%H:%M:%S.%f"
            time_func = datetime.strptime
            kwargs['updated_at'] = time_func(kwargs['updated_at'], isoformat)
            kwargs['created_at'] = time_func(kwargs['created_at'], isoformat)
            del kwargs['__class__']  # WHY IS THIS DELETED??
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                           (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        try:
            del dictionary['_sa_instance_state']
        except:
            pass
        return dictionary

    def delete(self):
        """Delete the current instance from storage by calling delete method"""
        storage.delete(self)
