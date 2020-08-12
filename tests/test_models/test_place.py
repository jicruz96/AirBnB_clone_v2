#!/usr/bin/python3
""" """
from sqlalchemy.util.langhelpers import NoneType
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.city_id), NoneType)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), NoneType)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), NoneType)

    def test_description(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.description), NoneType)

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_rooms), NoneType)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), NoneType)

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.max_guest), NoneType)

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.price_by_night), NoneType)

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), NoneType)

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), NoneType)

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)
