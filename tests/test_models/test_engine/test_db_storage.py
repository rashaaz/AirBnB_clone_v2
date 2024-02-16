#!/usr/bin/python3
''' Unit tests for the DBStorage class in the
    context of the User class.'''
import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test not supported')
class TestDBStorage(unittest.TestCase):
    '''Test cases for the DBStorage class in the context of the User class.'''
    def test_new_and_save(self):
        '''Test the new and save methods.'''
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'jack',
                           'last_name': 'bond',
                           'email': 'jack@bond.com',
                           'password': 12345})
        c = db.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        old_count = cu.fetchall()
        c.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        c = db.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        new_count = c.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        c.close()
        db.close()

    def test_creating_new_user(self):
        """  Test creating a new user."""
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cursor.fetchone()
        self.assertTrue(res is not None)
        self.assertIn('john2020@gmail.com', res)
        self.assertIn('password', res)
        self.assertIn('John', res)
        self.assertIn('Zoldyck', res)
        cursor.close()
        dbc.close()

    def test_delete_user(self):
        """  Test deleting a user."""
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        o_k = 'User.{}'.format(new.id)
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cursor.fetchone()
        self.assertTrue(res is not None)
        self.assertIn('john2020@gmail.com', res)
        self.assertIn('password', res)
        self.assertIn('John', res)
        self.assertIn('Zoldyck', res)
        self.assertIn(o_k, storage.all(User).keys())
        new.delete()
        self.assertNotIn(o_k, storage.all(User).keys())
        cursor.close()
        dbc.close()

    def test_reload_data_from_database(self):
        """  Test reloading data from the database."""
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '4447-by-me',
                str(datetime.now()),
                str(datetime.now()),
                'ben_pike@yahoo.com',
                'pass',
                'Benjamin',
                'Pike',
            ]
        )
        self.assertNotIn('User.4447-by-me', storage.all())
        dbc.commit()
        storage.reload()
        self.assertIn('User.4447-by-me', storage.all())
        cursor.close()
        dbc.close()

    def test_saving_a_user(self):
        """  Test saving a user."""
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(res is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        dbc1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur2 = dbc1.cursor()
        cur2.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cur2.fetchone()
        cur2.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cur2.fetchone()[0]
        self.assertFalse(res is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cur2.close()
        dbc1.close()
        cursor.close()
        dbc.close()
