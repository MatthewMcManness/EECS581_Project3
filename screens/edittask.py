# -----------------------------------------------------------------------------
# Name: edittask.py
# Description: This module defines the AddTaskModal class, which provides a 
#              modal interface to create and save tasks within the BusyBee 
#              application.
# Programmer: Matthew McManness (2210261)
# Date Created: November 9, 2024
# Revision History:
# - November 9, 2024: Initial version copied from addtask.py then added the nessecary functions to update or delete a task (Author: Matthew McManness)
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

class EditTaskModal(ModalView):
    def __init__(self, task_id=None, refresh_callback=None, **kwargs):
        """Initialize the EditTaskModal with layout components, loading task data if editing."""
        super().__init__(**kwargs)
        self.task_id = task_id  # Store task ID for editing
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False
        self.refresh_callback = refresh_callback  # Store the refresh callback

        # Load categories
        with db.get_session() as session, session.begin():
            stmt = select(Category).where(True)
            results = session.scalars(stmt).all()
            self.categories = [result.name for result in results]
            self.categories_ids = [result.id for result in results]

        self.selected_categories = []

        # Create layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title input
        self.title_input = TextInput(hint_text="Task Title")
        layout.add_widget(self.title_input)

        # Deadline section
        deadline_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.deadline_label = Label(text="Pick a deadline", size_hint_x=0.8)
        deadline_layout.add_widget(self.deadline_label)
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        deadline_layout.add_widget(pick_date_button)
        layout.add_widget(deadline_layout)

        # Repeat button
        self.repeat_button = Button(text="Does not repeat", on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        # Notes input
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner
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

        # Display selected categories
        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="DELETE", on_release=self.delete_task))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        self.add_widget(layout)

        # Load existing task data if editing
        if task_id:
            self.load_task(task_id)

    def load_task(self, task_id):
        """Load task data into fields for editing."""
        with db.get_session() as session, session.begin():
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                self.title_input.text = task.name
                self.notes_input.text = task.notes
                self.deadline_label.text = f"Deadline: {task.due_date.strftime('%Y-%m-%d %H:%M')}" if task.due_date else "Pick a deadline"
                self.selected_categories = [category.name for category in task.categories]
                self.update_applied_categories()

    def save_task(self, *args):
        """Save the task, updating if it exists or creating a new one."""

        if not self.title_input.text:
            print("Task Title is required.")
            return

        # Collect data
        name = self.title_input.text
        notes = self.notes_input.text
        due_date = self.deadline_label.text.split(" ", 1)[1] if "Deadline" in self.deadline_label.text else None
        due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M") if due_date else None

        # Retrieve category instances
        selected_categories_ids = [cat_id for cat_id, cat in zip(self.categories_ids, self.categories) if cat in self.selected_categories]

        with db.get_session() as session:
            if self.task_id:
                task = session.query(Task).filter_by(id=self.task_id).first()
                task.name = name
                task.notes = notes
                task.due_date = due_date
                task.categories = session.query(Category).filter(Category.id.in_(selected_categories_ids)).all()
            else:
                task = Task(name=name, notes=notes, due_date=due_date)
                task.categories = session.query(Category).filter(Category.id.in_(selected_categories_ids)).all()
                session.add(task)

            # Commit the session and capture the task ID before the session closes
            session.commit()
            task_id = task.id  # Capture the ID before the session closes

        if self.refresh_callback:
            self.refresh_callback()

        print(f"Task {'updated' if self.task_id else 'saved'} with ID: {task_id}")
        self.dismiss()

    def delete_task(self, *args):
        """Delete the task from the database."""
        if self.task_id:
            with db.get_session() as session, session.begin():
                task = session.query(Task).filter_by(id=self.task_id).first()
                if task:
                    session.delete(task)
            print(f"Task with ID {self.task_id} deleted.")

            # Call the refresh callback to update the ToDoListView after deletion
            if self.refresh_callback:
                self.refresh_callback()

            self.dismiss()

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