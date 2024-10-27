"""
    Name: Event Model
    Description: Event model class to represent records in Event table of the database
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
        - Base class will have Event_ as a part of its metadata
    Invariants: 
        - The class will always be a sub class of the declarative_base from SQLAlchemy
        - The id attribute will always be an id of an Item
        - ItemType Enum is implemented
        - Many-to-One Relationship with Recurrence
    Known Faults: 
        - None
"""


# Imports
from datetime import datetime
from .item import Item # Superclass model
from .databaseEnums import ItemType # enum for types of item
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship


class Event_(Item):
    """
    Event Model for records in the Event Table

    Attributes:
        __tablename__ (str): the name of the table
        id (int): event id (foreign key to Item.id)
        location_ (str): location of event, max 100 chars
        start_time (datetime): start date and time of event
        e_created (datetime): date and time event was created
        e_last_updated (datetime): date and time event was last updated
        recurrence_id (int): id of associated recurrence, if any
        recurence (Models.Recurrence): object of associated recurrence, if any
    """
    __tablename__ = "Event_"


    # Attributes, all are NOT NULL (required) except location_
    id: Mapped[int] = mapped_column(
        ForeignKey("Item.id"),  # Foreign Key: Item(id)
        primary_key=True # foreign key is primary key
    )

    location_: Mapped[Optional[str]] = mapped_column(String(100))
    
    start_time: Mapped[datetime] = mapped_column(
        default=datetime.now # defaults to inserted date and time
    )
    
    e_created: Mapped[datetime] = mapped_column(
        default=datetime.now # defaults to inserted date and time
    )
    
    e_last_updated: Mapped[datetime] = mapped_column(
        default=datetime.now, # defaults to inserted date and time
        onupdate=datetime.now # auto update this attribute, when record is updated
    )


    # Discriminator, for inheritance: Item(type)
    __mapper_args__ = {
        "polymorphic_identity": ItemType.EVENT
    }


    # Foreign Key to the Recurrence model
    recurrence_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Recurrence.id"))


    # Many-to-One Relationship with Recurrence
    reccurence: Mapped[Optional["Recurrence"]] = relationship( # type: ignore
        back_populates="events" # attribute
    )