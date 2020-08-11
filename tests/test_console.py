#!/usr/bin/python3
""" Contains unittests for HBNBCommand class """
from unittest import TestCase
from unittest.mock import patch
from console import HBNBCommand
from io import StringIO


class TestHBNBCommandClass(TestCase):
    """ Tests HBNBCommand class """

    def test_do_all(self):
        """ Tests all method """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create bad")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")
