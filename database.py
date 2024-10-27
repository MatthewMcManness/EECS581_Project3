"""
    Name: Database Class
    Description: Database class that serves as an interface to interact with the SQLite database
    Author: Magaly Camacho [3072618]

    Date Created: 10/20/2024
    Revisions: 
        - None

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
        - Models and Enums must be implemented
    Postconditions: 
        - None
    Errors/Exceptions: 
        - Operational Error if the database cannot be created or accessed
        - SQLAlchemyError for any SQLAlchemy-related errors
    Side Effects: 
        - None
    Invariants: 
        - Base will contain all database metadata (models/tables)
        - The database schema will be consistent with the defined models
    Known Faults: 
        - None
"""


# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Models.base import Base # base class for database models


class Database:
    """
    Class to interact with the SQLite database
    
    Attributes:
        engine (Engine): database engine created from models
        Session (Session): session class used to instantiate database session to run queries
    """
    def __init__(self, db_path:str, debug:bool=False):
        """
        Initialize database from models

        Attributes:
            db_path (str): the path to the database (or where it should be created)
            debug (bool): whether or not to print SQL emitted by connection, False by default
        """
        # engine to create database connections
        self.engine = create_engine(f"sqlite:///{db_path}", echo=debug)
        
        # create database if it doesn't exist already
        Base.metadata.create_all(self.engine) 

        # save Session class
        self.Session = Session


