"""
    Name: Database Enumerations
    Description: Enumerations for database models, item types, as well as database attributes Task(Priority) and Recurrence(Frequency)
    Authors: Magaly Camacho [3072618]

    Date Created: 10/20/2024
    Revisions: 
        - 11/04/2024 Magaly Camacho
            Added a static method to Priority to get string and color associated with a given priority

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


    @staticmethod
    def get_str_and_color(priority) -> tuple[str, tuple[float, float, float, float]]:
        """
        Returns string and color associated with a given priority

        Parameters:
            priority (Priority): a given priority (LOW, MEDIUM, or HIGH)

        Returns:
            tuple[str, tuple[float, float, float, float]: the string and color associated with the priority (string, color)
        """
        str_list = ["Low", "Medium", "High"]
        colors = [
            (0, 255, 0, 1), # green, low
            (255, 255, 0, 1), # yellow, medium
            (255, 0, 0, 1) # red, high
        ]

        if priority in Priority:
            val = priority.value
            return str_list[val], tuple(c / 255 if i != 3 else c for i, c in enumerate(colors[val]))
        
        raise ValueError("Invalid Priority value")
    

class Frequency(Enum):
    """Enumeration for Recurrence.Frequency"""
    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2
    YEARLY = 3