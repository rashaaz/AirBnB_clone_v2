#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from models import storage_type

Base = declarative_base()


class BaseModel:
    """Base class for HBNB project ORM models.

        Attributes:
            id (str): Unique identifier for the instance.
            created_at (datetime): Timestamp of instance creation.
            updated_at (datetime): Timestamp of instance last update.
    """
    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of the BaseModel class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for h in kwargs:
                if h in ['created_at', 'updated_at']:
                    setattr(self, h, datetime.fromisoformat(kwargs[k]))
                elif h != '__class__':
                    setattr(self, h, kwargs[h])
            if storage_type == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the BaseModel instance"""
        return '[{}] ({}) {}'.format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Saves the current instance to the storage system."""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the BaseModel instance."""
        d = self.__dict__.copy()
        d['__class__'] = self.__class__.__name__
        for h in d:
            if type(d[h]) is datetime:
                d[h] = d[h].isoformat()
        if '_sa_instance_state' in d.keys():
            del(d['_sa_instance_state'])
        return d

    def delete(self):
        '''Deletes the current instance from the storage system.'''
        from models import storage
        storage.delete(self)
