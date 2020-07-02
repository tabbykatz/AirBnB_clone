#!/usr/bin/python3
"""unit tests module for our BaseModel Class"""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import uuid
import unittest
import json
import time
import os
import re


class TestBaseModel(unittest.TestCase):

    """tests for the BaseModel class"""

    def setUp(self):
        """to set it up"""
        pass

    def tearDown(self):
        """to tear it all down"""
        self.resetStorage()
        pass

    def resetStorage(self):
        """start fresh with storage"""
        FileStorage._Filestorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    """Tests for instantiation"""
    def test_instance(self):
        """making a lab rat"""

        rat = BaseModel()
        string = "<class 'models.base_model.BaseModel'>"
        self.assertEqual(str(type(rat)), string)
        self.assertIsInstance(rat, BaseModel)
        self.assertTrue(issubclass(type(rat), BaseModel))

    def test_init_no_args(self):
        """init no args please"""
        with self.assertRaises(TypeError) as e:
            BaseModel.__init__()
        msg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_datetime_creation(self):
        """checking for datetime function"""
        rat = BaseModel()
        date = datetime.now()
        difference = rat.updated_at - rat.created_at
        self.assertTrue(abs(difference.total_seconds()) < 0.01)
        difference = rat.created_at - date
        self.assertTrue(abs(difference.total_seconds()) < 0.1)

    def test_ids_special(self):
        """test for unique ids"""
        rat = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(rat)), len(rat))

    def test_save(self):
        """save yourselves!"""
        rat = BaseModel()
        time.sleep(0.5)
        date = datetime.now()
        rat.save()
        self.assertTrue(abs(rat.updated_at > rat.created_at))

    def test_save_time(self):
        """save updates time"""
        rat = BaseModel()
        the_time = rat.updated_at
        time.sleep(0.001)
        rat.save()

        self.assertNotEqual(the_time, rat.updated_at)

        with open("file.json", "r") as f:
            self.assertIn(rat.to_dict(), json.loads(f.read()).values())

    def test_str_method(self):
        """test the str method"""
        rat = BaseModel()
        ratstr = "[{}] ({}) {}".format("BaseModel",
                                       rat.id, rat.__dict__)
        self.assertEqual(rat.__str__(), ratstr)

    def test_attr(self):
        """do they exist, right data types?"""
        rat = BaseModel()
        self.assertTrue(isinstance(rat.id, str))
        self.assertTrue(isinstance(rat.created_at, datetime))
        self.assertTrue(isinstance(rat.updated_at, datetime))

    def test_to_dict(self):
        """send to dict"""
        rat = BaseModel()
        rat.name = "labrat"
        rat.age = 100
        thing = rat.to_dict()
        self.assertEqual(thing["id"], rat.id)
        self.assertEqual(thing["__class__"], type(rat).__name__)
        self.assertEqual(thing["created_at"], rat.created_at.isoformat())
        self.assertEqual(thing["updated_at"], rat.updated_at.isoformat())
        self.assertEqual(thing["name"], rat.name)
        self.assertEqual(thing["age"], rat.age)

if __name__ == '__main__':
    unittest.main()
