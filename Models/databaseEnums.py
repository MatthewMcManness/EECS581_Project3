"""
    Name: Database Enumerations
    Description: Enumerations for database models, item types, as well as database attributes Task(Priority) and Recurrence(Frequency)
    Authors: Magaly Camacho [3072618]

    Date Created: 10/20/2024
    Revisions: 
        - None

    Preconditions: 
        - None
    Postconditions: 
        - None
    Errors/Exceptions: 
        - None
    Side Effects: 
        - None
    Invariants: 
        - The classes will be subclasses of Enum
    Known Faults: 
        - None
"""


from enum import Enum


class ItemType(Enum):
    """Enumeration for types of items"""
    EVENT = 0
    TASK = 1


class Priority(Enum):
    """Enumeration for Task.Priority"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class Frequency(Enum):
    """Enumeration for Recurrence.Frequency"""
    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2
    YEARLY = 3