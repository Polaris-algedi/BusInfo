#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with mysql+mysqldb database
connection.
"""

import os
from models.base_model import Base
from models.user import User
from models.route import Route
from models.feedback import Feedback
from models.bus import Bus
from models.schedule import Schedule
from models.stop import BusStop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
DB_CLASSES = {
    'User': User,
    'Route': Route,
    'Feedback': Feedback,
    'Bus': Bus,
    'Schedule': Schedule,
    'BusStop': BusStop
}


class DBStorage:
    """Database Storage using SQLAlchemy with MySQL database connection."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the object"""
        user = os.getenv('BUS_MYSQL_USER')
        passwd = os.getenv('BUS_MYSQL_PWD')
        host = os.getenv('BUS_MYSQL_HOST')
        database = os.getenv('BUS_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        if os.getenv('BUS_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = DB_CLASSES.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in DB_CLASSES.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        """reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """creates a new object"""
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is not None and type(id) == str:
            if isinstance(cls, str):
                cls = DB_CLASSES.get(cls, None)
            
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if cls is not None:
            if isinstance(cls, str):
                cls = DB_CLASSES.get(cls, None)
            total = self.__session.query(cls).count()
        else:
            for cls in DB_CLASSES.values():
                total += self.__session.query(cls).count()
        return total