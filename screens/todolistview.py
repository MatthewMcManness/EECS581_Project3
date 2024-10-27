# Prologue Comments:
# Code Artifact: ToDoListView Class Definition
# Brief Description: This code defines the `ToDoListView` class, a screen used to display and manage 
# tasks in a to-do list. It provides a method to add tasks dynamically based on input data.
# Programmer: Matthew McManness (2210261) and
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of ToDoListView structure  (placeholder for navigation) - [Matthew McManness]
#   - [Insert Further Revisions]: [Brief description of changes] - [Your Name]
# Preconditions:
#   - This class should be part of a ScreenManager in the Kivy application to function correctly.
# Acceptable Input:
#   - Valid task data must be passed to the `add_task` method in dictionary format.
# Unacceptable Input:
#   - Passing `None` or invalid data types to `add_task` will result in incorrect behavior.
# Postconditions:
#   - A new task is added and a message is logged to the console.
# Return Values:
#   - None. The task addition relies on side effects such as console logging.
# Error and Exception Conditions:
#   - If the `task_data` is malformed, the method will not function correctly.
# Side Effects:
#   - Logs task addition messages to the console for debugging.
# Invariants:
#   - The `ToDoListView` must be part of the screen management system for correct rendering.
# Known Faults:
#   - None identified.

# Import the Screen class from Kivy for managing screens.
from kivy.uix.screenmanager import Screen

class ToDoListView(Screen):
    """A screen for displaying the To-Do List."""

    def __init__(self, **kwargs):
        """Initialize the ToDoListView screen."""
        super().__init__(**kwargs)  # Initialize the superclass with provided arguments.

    def add_task(self, task_data):
        """Add a new task to the to-do list.
        
        Preconditions:
            - `task_data` must be a dictionary containing valid task information.
        Postconditions:
            - Logs the task addition to the console.

        Args:
            task_data (dict): A dictionary containing details about the task to be added.

        Side Effects:
            - Prints a message to the console with the task details.

        Example:
            task_data = {
                "title": "Complete Assignment",
                "deadline": "2024-11-01",
                "priority": "High"
            }
            self.add_task(task_data)
        
        Error Conditions:
            - If `task_data` is not provided or is invalid, the function will print 
              an incorrect log message but will not crash.

        """
        print(f"Added task: {task_data}")  # Log the task addition to the console.
