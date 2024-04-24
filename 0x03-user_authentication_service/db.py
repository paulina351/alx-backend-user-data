#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
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
        return adduser

    def find_user_by(self, **kwargs) -> users:
        """
        """
        adduser = self.session.query(User).filter_by(**kwargs).first())
        if not user:
            raise NoResultFound("No user found")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """"""
        try:
            adduser = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                if hasattr(adduser, k):
                    setattr(adduser, k, v)
                else:
                    raise InvalidRequestError
            self._session.commit()
        except (NoResultFound, InvalidRequestError, ValueError):
            raise ValueError
