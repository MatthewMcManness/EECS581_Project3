"""
    Name: Task Model
    Description: Task model class to represent records in Task table of the database
    Author: Magaly Camacho [3072618]

    Date Created: 10/24/2024
    Revisions: 
        - None

    Preconditions: 
        - SQLAlchemy must be installed and configured in the environment
    Postconditions: 
        - None
    Errors/Exceptions: 
        - Validation errors if the attribute constraints (e.g. type, string length, etc.) are not met
    Side Effects: 
        - Base class will have Task as a part of its metadata
    Invariants: 
        - The class will always be a sub class of the Item model class
        - The id attribute will always be an id of an Item
        - Item model, ItemType Enum, Complete Enum, and Priority Enum are implemented
    Known Faults: 
        - None
"""


# Imports
import datetime
from .item import Item # Superclass model
from .databaseEnums import ItemType, Complete, Priority # enums for types of item, and complete and priority attributes 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column 


class Task(Item):
    """
    Item Model for records in the Item Table

    Attributes:
        __tablename__ (str): the name of the table
        id (int): task id (foreign key to Item.id)
        complete (bool): whether task is complete or not, defaults to False
        priority (Models.databaseEnums.Priority): task priority (low, medium, high)
        t_created (datetime): date and time task was created
        t_last_updated (datetime): date and time task was last updated
    """
    __tablename__ = "Task"


    # Attributes, all are NOT NULL (required)
    id: Mapped[int] = mapped_column(
        ForeignKey("Item.id"), # Foreign Key: Item(id)
        primary_key=True # foreign key is primary key
    ) 
    
    complete: Mapped[bool] = mapped_column(
        default=False # defaults to not complete
    )
    
    priority: Mapped[Priority] = mapped_column(
        default=Priority.LOW # defaults to low priority
    )
    
    t_created: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now # defaults to inserted date and time
    )
    
    t_last_updated: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, # defaults to inserted date and time
        onupdate=datetime.datetime.now # aut update this attribute when record is updated
    )


    # Discriminator for inheritance: Item(type)
    __mapper_args__ = {
        "polymorphic_identity": ItemType.TASK
    }