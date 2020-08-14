#!/usr/bin/python3
""" Module for testing db storage"""
from models.engine.db_storage import DBStorage
from sqlalchemy.sql.schema import ForeignKeyConstraint
from models.city import City
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
import unittest
from models.base_model import BaseModel
from models import storage
from models.state import State
from os import getenv
import MySQLdb


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "Not using database")
class test_DBStorage(unittest.TestCase):
    """ Class to test the db storage method """
    args = {
        "user": getenv('HBNB_MYSQL_USER'),
        "passwd": getenv('HBNB_MYSQL_PWD'),
        "db": getenv('HBNB_MYSQL_DB'),
        "host": getenv('HBNB_MYSQL_HOST')
    }

    def setUp(self):
        """ Setup Func """
        self.db_connection = MySQLdb.connect(**self.args)
        self.cursor = self.db_connection.cursor()

    def tearDown(self):
        """ Tear down func """
        try:
            self.cursor.close()
            self.db_connection.close()
        except:
            pass

    def test_a(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = State(**{'name': 'California'})
        new.save()
        self.assertIn(new, storage.all().values())
        new.delete()

    def test_all(self):
        """ __objects is properly returned """
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_all_one(self):
        """ all(cls) returns dict of cls objects only """
        new = BaseModel()
        state_dict = storage.all("State")
        self.assertNotIn(new, state_dict)

    def test_delete(self):
        """ tests delete method"""
        new = State(**{'name': 'California'})
        new.save()
        self.assertIn(new, storage.all().values())
        new.delete()
        self.assertNotIn(new, storage.all().values())

    def test_save(self):
        """ DBStorage save method """
        new = State(name="Puerto Rico")
        self.assertNotIn(new, storage.all().values())
        new.save()
        self.assertIn(new, storage.all().values())
        new.delete()

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        from models.state import State
        new = State(**{'name': 'California'})
        # storage.new(new)
        new.save()
        self.assertIn(new, storage.all().values())
        storage.reload()
        self.assertNotIn(new, storage.all().values())
        new.delete()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models import DBStorage
        self.assertEqual(type(storage), DBStorage)

    # def test_creation_1(self):
    #     """ Tests state creation """
    #     self.cursor.execute('SELECT count(*) FROM states;')
    #     length1 = self.cursor.fetchone()[0]
    #     self.cursor.close()
    #     self.db_connection.close()
    #     with patch('sys.stdout', new=StringIO()) as state_id:
    #         HBNBCommand().onecmd('create State id="42" name="California"')
    #     self.db_connection = MySQLdb.connect(**self.args)
    #     self.cursor = self.db_connection.cursor()
    #     self.cursor.execute('SELECT count(*) FROM states;')
    #     length2 = self.cursor.fetchone()[0]
    #     self.assertEqual(length1 + 1, length2)

    def test_creation_2(self):
        """ Tests City creation """
        self.cursor.execute('SELECT count(*) FROM cities;')
        length1 = self.cursor.fetchone()[0]
        self.cursor.close()
        self.db_connection.close()
        state_string = 'create State id="2" name="Oklahoma"'
        city_string = 'create City id="1" state_id="2" name="Tulsa"'
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd(state_string)
            HBNBCommand().onecmd(city_string)
        self.db_connection = MySQLdb.connect(**self.args)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute(
            'SELECT count(*) FROM cities WHERE state_id = 2;')
        length2 = self.cursor.fetchone()[0]
        self.assertEqual(length1 + 1, length2)

    def test_creation_3(self):
        """ Tests Place creation """
        self.cursor.execute('SELECT count(*) FROM places;')
        length1 = self.cursor.fetchone()[0]
        self.cursor.close()
        self.db_connection.close()
        state_string = 'create State id="1" name="California"'
        city_string = 'create City id="2" state_id="1" name="Fremont"'
        user_string = 'create User id="42" email="42@gmail.com" password="pwd"'
        place_string = 'create Place user_id="42" city_id="2" name="Rad_Place"'
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd(state_string)
            HBNBCommand().onecmd(city_string)
            HBNBCommand().onecmd(user_string)
            HBNBCommand().onecmd(place_string)
        self.db_connection = MySQLdb.connect(**self.args)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('SELECT count(*) FROM places;')
        length2 = self.cursor.fetchone()[0]
        # self.cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
        # self.cursor.execute('TRUNCATE TABLE places;')
        # self.cursor.execute('TRUNCATE TABLE users;')
        # self.cursor.execute('TRUNCATE TABLE cities;')
        # self.cursor.execute('TRUNCATE TABLE states;')
        self.assertEqual(length1 + 1, length2)

    def test_key_deletion(self):
        """ Tests _sa_instance_state key is deleted """
        new = State(name="California")
        self.assertIn('_sa_instance_state', new.__dict__.keys())
        new = new.to_dict()
        self.assertNotIn('_sa_instance_state', new.keys())

    def test_state_deletion(self):
        """ Tests deleting a state with delete method """
        new = State(name="New Mexico", id="13")
        new.save()
        self.assertIn(new, storage.all().values())
        new.delete()
        self.assertNotIn(new, storage.all().values())

    def test_city_deletion(self):
        """ Tests deleting a city with delete method """
        new_state = State(name="Colorado", id="5280", cities=[
                          City(name="Denver", id="22", state_id="5280")])
        new_state.save()
        self.assertIn('cities', new_state.to_dict())
        new_state.delete()
        self.assertNotIn('cities', storage.all().values())

    def test_storage_type(self):
        """ Tests if storage type is db """
        self.assertEqual(type(storage), DBStorage)

    # def test_deletion(self):
    #     """ Tests State/city deletion """
    #     print(storage.all())
    #     new_state = State(name="California", id="1",
    #     cities=[City(name="Fremont", id="2", state_id="1")])
    #     storage.__session.add(new_state)
    #     storage.__session.commit()
    #     cities = storage.__session.query(City).all()
    #     cities_count = len(cities)
    #     print(cities_count)
    #     storage.__session.close()

    # def test_deletion_1(self):
    #     """ Tests State/city deletion """
    #     state_string = 'create State id="1" name="California"'
    #     city_string = 'create City id="2" state_id="1" name="Fremont"'
    #     with patch('sys.stdout', new=StringIO()) as output:
    #         HBNBCommand().onecmd(state_string)
    #         HBNBCommand().onecmd(city_string)
    #     self.cursor.execute('SELECT count(*) FROM states;')
    #     length1 = self.cursor.fetchone()[0]
    #     self.cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
    #     self.cursor.execute('DELETE FROM states WHERE id = 1;')
    #     self.cursor.execute('SELECT count(*) FROM cities;')
    #     length2 = self.cursor.fetchone()[0]
    #     self.cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
    #     self.cursor.execute('TRUNCATE TABLE places;')
    #     self.cursor.execute('TRUNCATE TABLE cities;')
    #     self.cursor.execute('TRUNCATE TABLE states;')
    #     self.cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
    #     print(length1)
    #     print(length2)
    #     self.assertEqual(length1 - 1, length2)
