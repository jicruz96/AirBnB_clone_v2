#!/usr/bin/python3
""" Module for testing file storage"""
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models.engine.db_storage import DBStorage
import unittest
from models.base_model import Base, BaseModel
from models import storage
from models.state import State
import os
from os import getenv
import MySQLdb


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "Not using database")
class test_DBStorage(unittest.TestCase):
    """ Class to test the file storage method """
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
        self.cursor.close()
        self.db_connection.close()

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
        new = BaseModel()
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
        storage.delete(new)
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
        storage.new(new)
        self.assertIn(new, storage.all().values())
        storage.reload()
        self.assertNotIn(new, storage.all().values())

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)

    def test_creation_1(self):
        """ Tests state creation """
        self.cursor.execute('SELECT count(*) FROM states;')
        length1 = self.cursor.fetchone()[0]
        self.cursor.close()
        self.db_connection.close()
        with patch('sys.stdout', new=StringIO()) as state_id:
            HBNBCommand().onecmd('create State id="42" name="California"')
        self.db_connection = MySQLdb.connect(**self.args)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('SELECT count(*) FROM states;')
        length2 = self.cursor.fetchone()[0]
        self.assertEqual(length1 + 1, length2)

    def test_creation_2(self):
        """ Tests City creation """
        self.cursor.execute('SELECT count(*) FROM cities;')
        length1 = self.cursor.fetchone()[0]
        self.cursor.close()
        self.db_connection.close()
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State id="2" name="Oklahoma"')
            HBNBCommand().onecmd('create City id="1" state_id="2" name="Tulsa"')
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
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State id="1" name="California"')
            HBNBCommand().onecmd('create City id="2" state_id="1" name="Fremont"')
            HBNBCommand().onecmd('create User id="42" email="email@gmail.com" password="pwd"')
            HBNBCommand().onecmd('create Place user_id="42" city_id="2" name="Rad_Place"')
        self.db_connection = MySQLdb.connect(**self.args)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute(
            'SELECT count(*) FROM places WHERE city_id = 2 AND user_id = 42 AND name = "Rad Place";')
        length2 = self.cursor.fetchone()[0]
        self.assertEqual(length1 + 1, length2)
