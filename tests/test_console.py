#!/usr/bin/python3
""" Contains unittests for HBNBCommand class """
from os import getenv
from unittest import TestCase
import unittest
from unittest.mock import patch
from console import HBNBCommand
from io import StringIO
from models import storage


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "Not a database")
class test_HBNBCommandClass(TestCase):
    """ Tests HBNBCommand class """

    def test_do_create_string(self):
        """ Tests do_create method with string params """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State id="1" senator="Joe_Rogan"')
        new_dict = storage.all().get('State.1').__dict__
        self.assertIn('senator', new_dict)
        self.assertIsInstance(new_dict['senator'], str)

    def test_do_create_float(self):
        """ Tests do_create method with float params """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State id="2" latitude=37.773972')
        new_dict = storage.all().get('State.2').__dict__
        self.assertIn('latitude', new_dict)
        self.assertIsInstance(new_dict['latitude'], float)

    def test_do_create_integer(self):
        """ Tests do_create method with integer params """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State id="3" max_guest=42')
        new_dict = storage.all().get('State.3').__dict__
        self.assertIn('max_guest', new_dict)
        self.assertIsInstance(new_dict['max_guest'], int)
