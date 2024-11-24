# -----------------------------------------------------------------------------
# Name: busybee.py
# Description: This module contains the main application logic for the BusyBee 
#              app. It manages the screens and provides functionality to open 
#              task/event modals.
# Programmer: Matthew McManness (2210261), Magaly Camacho (3072618), Manvir Kaur (3064194)
# Date Created: October 26, 2024
# Revision History:
# - October 26, 2024: Initial version created. (Author: Matthew McManness)
# - October 27, 2024: Current version created (added comments). (Updated by: Matthew McManness)
# - November 4, 2024: Added call to To Do list view so that tasks already in the database are populated (Updated by: Magaly Camacho)
# - November 11, 2024: Added open_edit_task_modal(self, task_id) (Updated by: Matthew McManness)
#
# Preconditions:
# - Kivy must be installed and properly configured in the Python environment.
# - The `screens` directory must contain the required screen classes 
#   (CalendarView, ToDoListView, AddEventModal, AddTaskModal).
#
# Acceptable Input:
# - Screen names such as "calendar" and "todo" for switching screens.
#
# Unacceptable Input:
# - Inputting an invalid screen name will raise an error in screen switching.
#
# Postconditions:
# - If all modules are loaded properly, the application will open the main window 
#   with a screen manager to switch between screens.
#
# Return Values:
# - None. This class initializes and runs the Kivy application.
#
# Error and Exception Conditions:
# - ImportError: Raised if the screen classes or modals are not found.
# - RuntimeError: Raised if the Kivy environment is not properly initialized.
#
# Side Effects:
# - Adds multiple screens to the screen manager.
#
# Invariants:
# - ScreenManager should always contain at least two screens: CalendarView and 
#   ToDoListView.
#
# Known Faults:
# - None identified at the time of writing.
# -----------------------------------------------------------------------------

# Import necessary modules
from kivy.app import App  # Main class for running Kivy applications
from kivy.uix.screenmanager import ScreenManager, NoTransition  # Manage screens and transitions

# Import screen classes from the screens directory
from screens.calendarview import CalendarView
from screens.todolistview import ToDoListView
from screens.addevent import AddEventModal
from screens.addtask import AddTaskModal
from screens.edittask import EditTaskModal  # Import the edit modal
from screens.editEvent import EditEventModal # Import the edit event modal
from kivy.uix.screenmanager import ScreenManager


# -----------------------------------------------------------------------------
# Main Application Class: BusyBeeApp
# This class manages the screens and provides functionality to open modals.
# -----------------------------------------------------------------------------
class BusyBeeApp(App):
    """Main app class to manage screens and modals."""

    def build(self):
        """
        Initialize the screen manager and add the CalendarView and ToDoListView screens.

        Preconditions:
        - ScreenManager must be correctly initialized.

        Postconditions:
        - CalendarView and ToDoListView screens are added to the screen manager.

        Return:
        - Returns the initialized ScreenManager instance.
        """
        self.screen_manager = ScreenManager(transition=NoTransition())  # Initialize ScreenManager

        # Initialize To Do list view
        todo = ToDoListView(name="todo")
        todo.populate() # add existing tasks 

        # Add the CalendarView and ToDoListView screens to the manager
        self.screen_manager.add_widget(CalendarView(name="calendar"))
        self.screen_manager.add_widget(todo)

        return self.screen_manager  # Return the configured ScreenManager

    def open_add_task_modal(self):
        """
        Opens the AddTaskModal for creating a new task.

        Preconditions:
            - The ToDoListView screen must be accessible from the ScreenManager.

        Postconditions:
            - Displays the AddTaskModal for user input.
            - Passes the refresh_tasks callback from ToDoListView to the AddTaskModal.
        """
        # Use the correct screen name ('todo' as defined in build)
        todo_list_view = self.root.get_screen('todo')

        if hasattr(todo_list_view, 'refresh_tasks'):  # Ensure the callback exists
            # Pass refresh_tasks to the AddTaskModal
            add_task_modal = AddTaskModal(refresh_callback=todo_list_view.refresh_tasks)
            add_task_modal.open()
        else:
            print("Error: ToDoListView does not have a refresh_tasks method.")

    def open_add_event_modal(self):
        """
        Open the Add Event modal.

        Preconditions:
        - AddEventModal must be properly imported.

        Postconditions:
        - The Add Event modal will open.

        Side Effects:
        - Opens the Add Event modal view.

        Errors:
        - ImportError: If AddEventModal is not found.

        Return:
        - None.
        """
        add_event_modal = AddEventModal()  # Create an instance of AddEventModal
        add_event_modal.open()  # Open the modal

    def switch_to_screen(self, screen_name):
        """
        Switch between Calendar and To-Do List screens.

        Preconditions:
        - `screen_name` must be a valid screen name (either "calendar" or "todo").

        Postconditions:
        - The specified screen will become active.

        Side Effects:
        - Changes the active screen.

        Errors:
        - ValueError: If the provided screen name is not valid.

        Parameters:
        - screen_name (str): The name of the screen to switch to.

        Return:
        - None.
        """
        self.screen_manager.current = screen_name  # Change the active screen

    def open_edit_task_modal(self, task_id):
        """
        Open the Edit Task modal for a specific task.

        Args:
        - task_id (int): ID of the task to edit.

        Postconditions:
        - The Edit Task modal will open with the task data preloaded.
        """
        """Open the Edit Task modal for a specific task."""
        # Get the ToDoListView instance to access its refresh_tasks method
        todo_screen = self.screen_manager.get_screen("todo")
        
        # Create the EditTaskModal and pass the task ID and refresh callback
        edit_task_modal = EditTaskModal(task_id=task_id, refresh_callback=todo_screen.refresh_tasks)
        edit_task_modal.open()

def open_edit_event_modal(self, event_id):
    edit_event_modal = EditEventModal(event_id=event_id, refresh_callback=self.populate)
    edit_event_modal.open()
