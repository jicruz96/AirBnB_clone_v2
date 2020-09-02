#!/usr/bin/python3
"""This module creates the db_storage engine"""
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.state import State
from models.base_model import Base
from os import getenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


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
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all of type cls or all classes if cls=None"""
        from console import HBNBCommand
        objs = []
        if cls is None:
            for classes in HBNBCommand.classes:
                if classes != "BaseModel":
                    objs.extend(self.__session.query(eval(classes)).all())
        else:
            if isinstance(cls, str):
                class_name = eval(cls)
            else:
                class_name = cls
            objs = self.__session.query(class_name).all()
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
        if obj is not None:
            cname = eval(obj.__class__.__name__)
            self.__session.query(cname).filter(cname.id == obj.id).delete()

    def reload(self):
        """Create all tables in the database"""
        from sqlalchemy.orm import scoped_session
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """ closes session object"""
        self.__session.close()
