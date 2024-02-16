#!/usr/bin/python3
""" """
from models.base_model import BaseModel, Base
from datetime import datetime
import unittest
from uuid import UUID
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'basemodel test not supported')
class test_basemodel(unittest.TestCase):
    """ Test class for the BaseModel class in the HBNB project."""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ Set up method to prepare for each test case."""
        pass

    def tearDown(self):
        """Tear down method to clean up after each test case."""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Test method to ensure proper initialization of instances.
        """
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """ test method to check if instances are of the correct type."""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ check if instances can be created from a dictionary."""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """check if instances handle invalid dictionary values."""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Test method to check if instances are saved correctly."""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ Test method to check the string representation of instances."""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ Test method to check the to_dict() method."""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        self.assertIsInstance(self.value().to_dict(), dict)
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        m = self.value()
        m.firstname = 'Celestine'
        md.lastname = 'Akpanoko'
        self.assertIn('firstname', m.to_dict())
        self.assertIn('lastname', m.to_dict())
        self.assertIn('firstname', self.value(firstname='Celestine').to_dict())
        self.assertIn('lastname', self.value(lastname='Akpanoko').to_dict())
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        datetime_now = datetime.today()
        m = self.value()
        m.id = '012345'
        m.created_at = m.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': m.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(m.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='u-b34', age=13).to_dict(),
                {
                    '__class__': m.__class__.__name__,
                    'id': 'u-b34',
                    'age': 13
                }
            )
            self.assertDictEqual(
                self.value(id='u-b34', age=None).to_dict(),
                {
                    '__class__': m.__class__.__name__,
                    'id': 'u-b34',
                    'age': None
                }
            )
        m_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(m_d.to_dict(), m_d.__dict__)
        self.assertNotEqual(
            m_d.to_dict()['__class__'],
            m_d.__class__
        )
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """ Test method to check handling of None values in kwargs."""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ Test method to check creation with a single key-value pair."""
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """ Test method to check the id attribute."""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ Test method to check the created_at attribute."""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ Test method to check the updated_at attribute."""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
