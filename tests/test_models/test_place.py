#!/usr/bin/python3
""" """
from os import getenv
import unittest
from models import storage
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.state import State
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

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "Not using database")
    @unittest.skip("Maybe invalid")
    def test_place_amenity_ids(self):
        """ Tests a place amenity_ids list """
        # creation of a State
        state = State(name="California")
        state.save()

        # creation of a City
        city = City(state_id=state.id, name="San Francisco")
        city.save()

        # creation of a User
        user = User(email="john@snow.com", password="johnpwd")
        user.save()

        # creation of 2 Places
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_1.save()
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_2.save()

        # creation of 3 various Amenity
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()

        # link place_1 with 2 amenities
        place_1.amenities.append(amenity_1)
        place_1.amenities.append(amenity_2)

        # link place_2 with 3 amenities
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)

        self.assertEqual(len(place_1.amenities), 2)
        for objs in place_1.amenities:
            self.assertIsInstance(objs, Amenity)
        self.assertEqual(len(place_2.amenities), 3)
        for objs in place_2.amenities:
            self.assertIsInstance(objs, Amenity)
        self.assertEqual(place_1.user_id, user.id)
        self.assertEqual(place_2.city_id, city.id)
        self.assertIn(place_1, amenity_1.place_amenities)
        self.assertIn(place_2, amenity_2.place_amenities)
