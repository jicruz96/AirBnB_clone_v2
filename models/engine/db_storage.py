#!/usr/bin/python3
"""This module creates the db_storage engine"""
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.state import State
from models.base_model import Base
from os import environ, getenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker, scoped_session


class DBStorage():
    """This is an instance of the DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """This creates an instance of the DBStorage class"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        url = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db)
        self.__engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        if environ['HBNB_ENV'] == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all of type cls or all classes if cls=None"""
        if cls is None:
            objs = self.__session.query(
                User, State, City, Amenity, Place, Review).all()
        else:
            objs = self.__session.query(cls).all()
        new_dict = {}
        for obj in objs:
            key = obj.__class__.__name__ + '.' + obj.id
            new_dict.update({key: obj})
        return new_dict

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the object from the current database session"""
        if not None:
            self.__session.query(obj).delete()

    def reload(self):
        """Create all tables in the database"""
        sf = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sf)
        self.__session = Session()
