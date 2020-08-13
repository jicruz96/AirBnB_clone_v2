#!/usr/bin/python3
""" """
from models.place import Place
from models.city import City
from models.amenity import Amenity
from os import getenv
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "Not a database")
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                                                       i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertIn('Name', new.__dict__)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    # @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "Not a database")
    # def test_delete(self):
    #     from models import storage
    #     inst_dict = {}
    #     if self.value != BaseModel:
    #         if self.value == Amenity:
    #             inst_dict = {'name': 'WiFi'}
    #         elif self.value == City:
    #             inst_dict = {'state_id': 1, 'name': 'California', 'id': '2'}
    #         elif self.value == Place:
    #             inst_dict = {'city_id': 2, 'user_id': 42,
    #                          'name': 'Super Rad Place', 'number_rooms': 6,
    #                          'number_bathrooms': 4, 'max_guest': 20,
    #                          'price_by_night': 500}
    #         new = self.value(**inst_dict)
    #         new = self.value()
    #         new.save()
    #         self.assertIn(new, storage.all().values())
    #         new.delete()
    #         self.assertNotIn(new, storage.all().values())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "Not a database")
    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        new.id = "new_id"
        new.save()
        new.id = "newer_id"
        new.save()
        new.id = "newest_id"
        new.save()
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertNotEqual(new.created_at, new.updated_at)
