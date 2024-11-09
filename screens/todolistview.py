# Prologue Comments:
# Code Artifact: ToDoListView Class Definition
# Brief Description: This code defines the `ToDoListView` class, a screen used to display and manage 
# tasks in a to-do list. It provides a method to add tasks dynamically based on input data.
# Programmer: Matthew McManness (2210261), Magaly Camacho (3072618)
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of ToDoListView structure  (placeholder for navigation) - [Matthew McManness]
#   - November 4, 2024: Updated add_task to connect to database, and added a method populate() that adds all tasks in the database - [Magaly Camacho]
#   - November 11, 2024: Added def on_task_click(self, task_id), refresh_tasks(self), toggle_complete(self, checkbox, task_id, task_box), grey_out_task(self, task_box), reset_task_appearance(self, task_box)  - [Matthew McManness]
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
#   - If the `task_id` isn't valid, the method will not function correctly.
# Side Effects:
#   - Logs task addition messages to the console for debugging.
# Invariants:
#   - The `ToDoListView` must be part of the screen management system for correct rendering.
# Known Faults:
#   - When a new task is added, it's always added at the bottom instead of sorted in

# Imports
from kivy.uix.screenmanager import Screen  # to manage screen
from kivy.uix.boxlayout import BoxLayout  # base class for a task's box
from kivy.uix.checkbox import CheckBox  # checkbox widget (to mark complete/incomplete)
from kivy.uix.label import Label  # label widget to display text
from kivy.graphics import Color, Rectangle  # to control color and size of task background
from kivy.properties import ObjectProperty
from database import get_database  # to connect to database
from sqlalchemy import select  # to query database
from Models import Task  # task model class
from Models.databaseEnums import Priority  # for Task.priority
from kivy.app import App

db = get_database()  # get database

class TaskBox(BoxLayout):
    """A BoxLayout to hold task details"""
    task_id = ObjectProperty(None)
    categories = ObjectProperty(None)

    def __init__(self, on_click_callback, **kwargs):
        """Initialize the TaskBox with a callback for clicks."""
        super().__init__(**kwargs)
        self.on_click_callback = on_click_callback  # Set the callback attribute
        self.check_box = None  # Placeholder for checkbox reference

        # Initialize the size and background color of the TaskBox
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Update the rectangle size and position when TaskBox is resized
        self.bind(size=self.update_rect, pos=self.update_rect)

    def add_checkbox(self, callback):
        """Add a checkbox to the task box and bind it to a callback."""
        self.check_box = CheckBox(size_hint_x=0.1)
        self.check_box.bind(on_release=callback)
        self.add_widget(self.check_box)

    def update_rect(self, *args):
        """Update rectangle to match the size and position of the TaskBox."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        """Detect if the TaskBox was clicked but ignore if the checkbox was clicked."""
        if self.check_box and self.check_box.collide_point(*touch.pos):
            # If clicking on the checkbox, do not trigger the task click callback
            return super().on_touch_down(touch)

        # Otherwise, proceed with the task box click event
        if self.collide_point(*touch.pos):
            if self.on_click_callback:
                self.on_click_callback(self.task_id)
            return True
        return super().on_touch_down(touch)

class ToDoListView(Screen):
    """A screen for displaying the To-Do List."""

    def __init__(self, **kwargs):
        """Initialize the ToDoListView screen."""
        super().__init__(**kwargs)  # Initialize the superclass with provided arguments.

    def add_task(self, task_id, name, priority, due_date=None, categories=None, complete=False):
        """Add a new task to the to-do list."""
        # Create a TaskBox and pass `on_task_click` as the click callback
        task_box = TaskBox(on_click_callback=self.on_task_click, padding="5dp", spacing="5dp", size_hint_y=None, height="60dp", size_hint_x=1)
        task_box.task_id = task_id

        # Add checkbox for Task.complete and bind it to toggle_complete
        # Add checkbox with binding to toggle_complete
        task_box.add_checkbox(lambda instance: self.toggle_complete(instance, task_id, task_box))
        task_box.check_box.active = complete  # Set initial checkbox state

        # Check/update info to display None if needed
        if due_date is None:
            due_date = "-" 
        if categories is None:
            categories = "-" 

        # Get priority text and color
        priority, priority_color = Priority.get_str_and_color(priority)

        # Add widgets to display task info
        task_box.add_widget(Label(text=name, size_hint_x=0.5, color=(0,0,0,1)))
        task_box.add_widget(Label(text=due_date, size_hint_x=0.3, color=(0,0,0,1)))
        task_box.add_widget(Label(text=priority, size_hint_x=0.1, color=priority_color))
        task_box.add_widget(Label(text=categories, size_hint_x=0.5, color=(0,0,0,1)))

        # Grey out task if already complete
        if complete:
            self.grey_out_task(task_box)

        # Add task box to task list layout
        self.ids.task_list.add_widget(task_box)

        print(f"Added task: {task_id}")  # Log the task addition

    def populate(self):
        """Adds all tasks in the database to the view, ordered by due date."""
        with db.get_session() as session:  # connect to database through a session
            stmt = select(Task).where(True).order_by(Task.due_date)  # SQL statement
            tasks = session.scalars(stmt).all()  # Query database to get the tasks

            for task in tasks:
                # Stringify due_date and categories
                due_date = task.due_date.strftime("%Y-%m-%d %H:%M") 
                categories = ", ".join([cat.name for cat in task.categories])

                # Add task 
                self.add_task(task.id, task.name, task.priority, due_date, categories, complete=task.complete)

    def on_task_click(self, task_id):
        """Open the EditTaskModal for the clicked task."""
        print(f"Clicked task with ID: {task_id}")  # Debugging output
        app = App.get_running_app()
        app.open_edit_task_modal(task_id)
    
    def refresh_tasks(self):
        """Refresh the list of tasks by reloading from the database."""
        self.ids.task_list.clear_widgets()  # Clear the current list
        self.populate()  # Re-populate with updated data from the database

    def toggle_complete(self, checkbox, task_id, task_box):
        """Toggle the completion status of a task."""
        complete = checkbox.active  # True if checked, False if unchecked

        # Update the task in the database
        with db.get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                task.complete = complete  # Assume `complete` is a field in the Task model
                session.commit()

        # Update the visual appearance of the task
        if complete:
            # Set text and background color to greyed-out
            self.grey_out_task(task_box)
        else:
            # Set text and background color back to normal
            self.reset_task_appearance(task_box)

    def grey_out_task(self, task_box):
        """Grey out the task's appearance."""
        # Change text color to grey
        for widget in task_box.children:
            if isinstance(widget, Label):
                widget.color = (0.5, 0.5, 0.5, 1)  # Grey color

        # Change background color to a lighter grey
        with task_box.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            task_box.rect = Rectangle(size=task_box.size, pos=task_box.pos)

        # Bind update_rect on task_box to keep the grey background consistent
        task_box.bind(size=task_box.update_rect, pos=task_box.update_rect)


    def reset_task_appearance(self, task_box):
        """Reset the task's appearance to its original color."""
        # Reset text color to black
        for widget in task_box.children:
            if isinstance(widget, Label):
                widget.color = (0, 0, 0, 1)  # Original black color

        # Reset background color to white
        with task_box.canvas.before:
            Color(1, 1, 1, 1)
            task_box.rect = Rectangle(size=task_box.size, pos=task_box.pos)

        # Bind update_rect on task_box to maintain the white background
        task_box.bind(size=task_box.update_rect, pos=task_box.update_rect)