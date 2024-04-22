#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            The method should save the user to the database.
            No validations are required at this stage.
            Arguments:
                email (str): The user's email address
                hashed_password (str): The user's hashed password
            Returns:
                User: The user
        """
        adduser = User(email=email, hashed_password=hashed_password)
        self._session.add(adduser)
        self._session.commit()
        return User

    def find_user_by(self, **kwargs) -> User:
        """
            This method takes in arbitrary keyword arguments and returns
            the first row found in the users table as filtered by
            the method’s input arguments.

            Arguments:
                **kwargs: The arbitrary keyword arguments
            Returns:
                User: The user
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("Not found")
        return user
