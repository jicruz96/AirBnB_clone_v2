#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
from os import getenv
import MySQLdb


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "Not using database")
class test_DBStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """

        args = {
            "user": getenv('HBNB_MYSQL_USER'),
            "passwd": getenv('HBNB_MYSQL_PWD'),
            "db": getenv('HBNB_MYSQL_DB'),
            "host": getenv('HBNB_MYSQL_HOST')
        }

        db_connection = MySQLdb.connect(**args)
        cursor = db_connection.cursor()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            # Clean up
            cursor.close()
            db_connection.close()
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        self.assertIn(new, storage.all().values())

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_all_one(self):
        """ all(cls) returns dict of cls objects only """
        new = BaseModel()
        state_dict = storage.all(State)
        self.assertNotIn(new, state_dict)

    def test_delete(self):
        """ tests delete method"""
        new = BaseModel()
        self.assertIn(new, storage.all().values())
        new.save()
        self.assertNotIn(new, storage.all().values())

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertNotIn(new, storage.all().values())

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        self.assertNotIn(new, storage.all().values())
        storage.save()
        self.assertIn(new, storage.all().values())

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        from models.state import State
        new = State()
        storage.new(new)
        self.assertIn(new, storage.all().values())
        storage.reload()
        self.assertNotIn(new, storage.all().values())

        # for obj in storage.all().values():
        #     loaded = obj
        #     self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        from models.state import State
        new = State()
        new.save()
        _id = new.to_dict()['id']
        self.assertIn('BaseModel' + '.' + _id, storage.all())

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)
