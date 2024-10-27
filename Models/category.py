"""
    Name: Category Model
    Description: Category model class to represent records in Category table of the database
    Authors: Magaly Camacho [3072618]

    Date Created: 10/26/2024
    Revisions: 
        - None

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
    Postconditions:
        - None
    Errors/Exceptions: 
        - Validation errors if the attribute constraints (e.g. type, string length, etc.) are not met 
    Side Effects: 
        - Base class will have Category as a part of its metadata
    Invariants: 
        - The class will always be a sub class of the declarative_base from SQLAlchemy
        - The id attribute will always be unique and automatically generated
        - Item-category association are implemented
    Known Faults: 
        - None
"""


# Imports
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base # base model
from .itemCategory import item_category_association # association table


class Category(Base):
    """
    Category Model for records in the Category Table

    Attributes:
        __tablename__ (str): the name of the table
        id (int): category id (primary key, automatically generated by database)
        name (str): category name, max 50 chars
        color_hex (str): category's color hex value, defaults to white
        c_created (datetime): date and time category was created
        c_last_updated (datetime): date and time category was last updated
    """
    __tablename__ = "Category"


    # Attributes, all are NOT NULL (required)
    id: Mapped[int] = mapped_column(
        primary_key=True # primary key, automatically generated by database
    )

    name: Mapped[str] = mapped_column(String(50))
    
    color_hex: Mapped[str] = mapped_column(
        String(6),
        default="FFFFFF" # defaults to white
    )
    
    
    c_created: Mapped[datetime] = mapped_column(
        default=datetime.now # defaults to inserted date and time
    )

    c_last_updated: Mapped[datetime] = mapped_column(
        default=datetime.now, # defaults to inserted date and time
        onupdate=datetime.now # auto update this attribute, when record is updated
    )


    # Many-to-Many relationship with Item
    items: Mapped[Optional[List["Item"]]] = relationship( # type: ignore
        secondary=item_category_association, # association table
        back_populates="categories" # attribute in Item
    )