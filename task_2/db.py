#!/usr/bin/env python3
"""
This script contains that class that handles the Database Actions.
DB Module
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

# print(user, password, host)
#

user = ""
password = ""
host = ""
database = ""


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""

        self._engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, password, host, database),
            echo=False,
            pool_pre_ping=True,
        )
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, name: str) -> User:
        """This method adds a new user to the database."""
        try:
            user = User(email=email, name=name)
            #  session = self._session
            self._session.add(user)
            self._session.commit()
        except Exception:
            session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """This method finds the user using the key, value pair."""
        result = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                result.append(
                    self._session.query(User)
                    .filter(getattr(User, key) == value)
                    .first()
                )
            else:
                raise InvalidRequestError
        user = result[0]
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """This method updates a user."""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError()
        self._session.commit()

    def remove_user(self, user_id: int) -> None:
        """This method updates a user."""
        user = self.find_user_by(id=user_id)

        self._session.delete(user)
        self._session.commit()
