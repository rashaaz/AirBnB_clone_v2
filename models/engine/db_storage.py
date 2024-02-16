#!/usr/bin/python3
'''DBStorage Module for HBNB project'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    '''DBStorage Module for HBNB project'''
    __engine = None
    __session = None

    def __init__(self):
        '''Initializes a new instance of DBStorage.'''
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                                           HBNB_MYSQL_USER,
                                           HBNB_MYSQL_PWD,
                                           HBNB_MYSQL_HOST,
                                           HBNB_MYSQL_DB
                                       ), pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''Retrieves all objects of a specified class or
           all classes if none is specified.

            Args:
                cls (class): Optional - The class to retrieve objects for.

            Returns:
                dict: A dictionary with object IDs as
                      keys and objects as values.'''
        d = {}
        if cls is None:
            for s in classes.values():
                objs = self.__session.query(s).all()
                for obj in objs:
                    k = obj.__class__.__name__ + '.' + obj.id
                    d[k] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                k = obj.__class__.__name__ + '.' + obj.id
                d[k] = obj
        return d

    def new(self, obj):
        '''Adds a new object to the current database session.

            Args:
                obj: The object to be added.

            Raises:
                Exception: If an error occurs during
                           the addition of the object.'''
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        '''Commits changes to the current database session.'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Deletes an object from the current database session.

            Args:
                obj: Optional - The object to be deleted.
        '''
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        '''Creates tables in the database and initializes
           a new database session.'''
        Base.metadata.create_all(self.__engine)
        ses_fac = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(ses_fac)()

    def close(self):
        """Closes the current database session."""
        self.__session.close()
