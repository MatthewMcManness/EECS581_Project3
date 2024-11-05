# -----------------------------------------------------------------------------
# Name: addtask.py
# Description: This module defines the AddTaskModal class, which provides a 
#              modal interface to create and save tasks within the BusyBee 
#              application.
# Programmer: Matthew McManness (2210261)
# Date Created: October 26, 2024
# Revision History:
# - October 26, 2024: Initial version created (Author: Matthew McManness)
# - October 27, 2024: Updated to include proper comments (Matthew McManness)
# - November 4, 2024: Added connection to database to save tasks (Magaly Camacho)
#
# Preconditions:
# - Kivy framework must be installed and configured properly.
# - The `DatePicker` and `RepeatOptionsModal` must be accessible within 
#   screens/usefulwidgets.
#
# Postconditions:
# - This modal saves task data and adds it to the To-Do ListView.
#
# Error Handling:
# - If the task title is missing, the task will not be saved, and an error 
#   message will be printed to the console.
#
# Side Effects:
# - Updates the category list and modifies the To-Do ListView when tasks are added.
# Known Faults:
# - Priority picker needs to be implemented
# -----------------------------------------------------------------------------

# Import necessary Kivy modules and custom widgets
from kivy.uix.modalview import ModalView  # Modal for task creation
from kivy.uix.boxlayout import BoxLayout  # Layout for organizing widgets
from kivy.uix.textinput import TextInput  # Input fields for user text
from kivy.uix.spinner import Spinner  # Dropdown-style component
from kivy.uix.button import Button  # Standard button widget
from screens.usefulwidgets import DatePicker # Date picker
from screens.usefulwidgets import RepeatOptionsModal, CategoryModal  # Additional modals
from kivy.uix.label import Label  # Label widget for displaying text
from kivy.app import App  # Ensure App is imported
from Models import Task, Category # Task and Category classes
from Models.databaseEnums import Priority # for tasl priorities
from database import get_database # to connect to database
from sqlalchemy import select # to query database
from datetime import datetime # for Task.due_date

db = get_database() # get database

class AddTaskModal(ModalView):
    """
    A modal for adding a new task to the To-Do List.

    Attributes:
        categories (list): List of predefined task categories.
        selected_categories (list): List of user-selected categories for the task.
    """

    def __init__(self, **kwargs):
        """Initialize the AddTaskModal with layout components."""
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)  # Set modal size
        self.auto_dismiss = False  # Prevent accidental dismissal

        # Initialize categories and the selected category list
        with db.get_session() as session, session.begin():
            stmt = select(Category).where(True) # sql statement
            results = session.scalars(stmt).all() # query the database for all categories
            self.categories = [result.name for result in results] # save the names of all categories in the database
            self.categories_ids = [result.id for result in results] # cache ids
        self.selected_categories = [] # initially none

        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for the task title
        self.title_input = TextInput(hint_text="Task Title")
        layout.add_widget(self.title_input)

        # Deadline section with a label and date picker button
        deadline_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.deadline_label = Label(text="Pick a deadline", size_hint_x=0.8)
        deadline_layout.add_widget(self.deadline_label)
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        deadline_layout.add_widget(pick_date_button)
        layout.add_widget(deadline_layout)

        # Button to open the Repeat Options modal
        self.repeat_button = Button(text="Does not repeat", on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        # Input field for additional task notes
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner for category selection
        category_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.category_spinner = Spinner(
            text="Select Category",
            values=self.categories + ["Add New Category"],
            size_hint=(0.7, None),
            height=44
        )
        self.category_spinner.bind(text=self.on_category_selected)
        category_layout.add_widget(self.category_spinner)
        layout.add_widget(category_layout)

        # Display selected categories dynamically
        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        # Action buttons for canceling or saving the task
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        self.add_widget(layout)  # Add the layout to the modal

    def open_date_picker(self, instance):
        """Open the DatePicker modal to select a deadline."""
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        """Open the RepeatOptionsModal to choose a repeat option."""
        RepeatOptionsModal(self).open()

    def on_category_selected(self, spinner, text):
        """
        Handle category selection from the spinner.

        Args:
            spinner (Spinner): The spinner instance.
            text (str): The selected text from the spinner.
        """
        if text == "Add New Category":
            CategoryModal(self).open()  # Open modal to add a new category
        elif text not in self.selected_categories:
            self.selected_categories.append(text)  # Add the selected category
            self.update_applied_categories()  # Refresh the display

    def update_applied_categories(self):
        """Update the layout displaying selected categories."""
        self.applied_categories_layout.clear_widgets()  # Clear previous widgets
        for category in self.selected_categories:
            label = Label(text=category)
            self.applied_categories_layout.add_widget(label)

    def update_category_spinner(self):
        """Update the category spinner with the latest categories."""
        self.category_spinner.values = self.categories + ["Add New Category"]

    def save_task(self, *args):
        """Save the task and add it to the To-Do List screen.

        Preconditions:
            - The task title must not be empty.

        Postconditions:
            - If valid, the task is added to the To-Do List screen.

        Error Conditions:
            - If the task title is empty, an error message is logged.
        """

        # Check for task title
        if not self.title_input.text:
            print("Task Title is required.")
            return  # Stop execution if title is missing

        # Get task info from inputs
        name=self.title_input.text
        notes=self.notes_input.text
        priority=Priority.LOW # *** need to add priority input/spinner
        due_date = self.deadline_label.text
        categories=None # initially assume no categories
        if len(self.selected_categories) > 0: # if there's categories, make a string
            categories=", ".join(self.selected_categories)

        # connect to database with a session
        with db.get_session() as session:
            with session.begin(): # start a transaction, auto commits before exiting context
                # Get instances for selected categories
                selected_categories_ids = [cat_id for cat_id, cat in zip(self.categories_ids, self.categories) if cat in self.selected_categories]
                selected_categories_instances = session.query(Category).filter(Category.id.in_(selected_categories_ids)).all()

                # Collect task data
                new_task = Task(
                    name=name,
                    notes=notes,
                    priority=priority
                )

                # Add due date, if applicable
                if self.deadline_label.text:
                    due_date = (" ").join(self.deadline_label.text.split(" ")[1:]) # get rid of "Deadline: " in label
                    new_task.due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M") # add due date to task

                # Log message
                print(f"Saving task: {new_task}")

                # Create relationship between task and categories, note this can't be done in the constructor Task()
                new_task.categories = selected_categories_instances 

                # add task to session
                session.add(new_task)

            task_id = new_task.id # get new_task id

        # Access the running app instance
        app = App.get_running_app()  # Correctly fetch the app instance
        todo_screen = app.screen_manager.get_screen('todo')  # Get the To-Do List screen

        # Add the task to the To-Do List screen
        todo_screen.add_task(task_id, name, priority, due_date, categories)

        # Log the task addition and close the modal
        print(f"Task saved with ID: {task_id}")
        self.dismiss()