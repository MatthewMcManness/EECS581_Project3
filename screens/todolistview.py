# Prologue Comments:
# Code Artifact: ToDoListView Class Definition
# Brief Description: This code defines the `ToDoListView` class, a screen used to display and manage
# tasks in a to-do list. It provides a method to add tasks dynamically based on input data.
# Programmer: Matthew McManness (2210261), Magaly Camacho (3072618), Manvir Kaur (3064194)
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of ToDoListView structure  (placeholder for navigation) - [Matthew McManness]
#   - November 4, 2024: Updated add_task to connect to database, and added a method populate() that adds all tasks in the database - [Magaly Camacho]
#   - November 10, 2024: Added def on_task_click(self, task_id), refresh_tasks(self), toggle_complete(self, checkbox, task_id, task_box), grey_out_task(self, task_box), reset_task_appearance(self, task_box)  - [Matthew McManness]
#   - November 10, 2024: Fixed bug that crashed app when there's no due date. Added priority picker functionality - [Magaly Camacho]
#   - November 23, 2024: updated the populate function to handle recurrence - [Matthew McManness]
#   - November 23, 2024: tasks are displayed sorted by due date automatically - [Manvir Kaur]
#   - November 23, 2024: choosing a sorting option prints it to terminal instead of crashing - [Manvir Kaur]
#   - November 23, 2024: updating populate function to correctly sort all tasks according to the option selected - [Manvir Kaur]
#   - November 24, 2024: updating code to implement the filters correctly - [Shravya Matta]
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
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from database import get_database
from sqlalchemy import select
from Models import Task
from Models.databaseEnums import Priority
from kivy.app import App
from kivy.uix.dropdown import DropDown
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from Models import Category
from sqlalchemy.sql import case

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
        super().__init__(**kwargs)
        self.sort_by_dropdown = DropDown()
        self.filter_by_dropdown = DropDown()
        self.current_sort = "Due Date"  # Default sorting criterion
        self.current_filters = {}

    def add_task(self, task_id, name, priority=None, due_date=None, categories=None, complete=False):
        """Add a new task to the to-do list."""
        task_box = TaskBox(on_click_callback=self.on_task_click, padding="5dp", spacing="5dp", size_hint_y=None, height="60dp", size_hint_x=1)
        task_box.task_id = task_id

        # Add checkbox for Task.complete and bind it to toggle_complete
        task_box.add_checkbox(lambda instance: self.toggle_complete(instance, task_id, task_box))
        task_box.check_box.active = complete  # Set initial checkbox state

        # Check/update info to display None if needed
        if due_date is None:
            due_date = "-"
        if categories is None:
            categories = "-"
        if priority is None:
            priority = "-"
            priority_color = (0, 0, 0, 1)
        else:
            priority, priority_color = Priority.get_str_and_color(priority)

        # Add widgets to display task info
        task_box.add_widget(Label(text=name, size_hint_x=0.5, color=(0, 0, 0, 1)))
        task_box.add_widget(Label(text=due_date, size_hint_x=0.3, color=(0, 0, 0, 1)))
        task_box.add_widget(Label(text=priority, size_hint_x=0.1, color=priority_color))
        task_box.add_widget(Label(text=categories, size_hint_x=0.5, color=(0, 0, 0, 1)))

        # Grey out task if already complete
        if complete:
            self.grey_out_task(task_box)

        # Add task box to task list layout
        self.ids.task_list.add_widget(task_box)

        print(f"Added task: {task_id}")  # Log the task addition

    def populate(self):
        """
        Populate the ToDoListView with tasks from the database, sorted and filtered based on the current_sort and current_filters attributes.
        """
        with db.get_session() as session:
            stmt = select(Task)  # Base statement for task selection

            # Apply filters
            if 'due_date' in self.current_filters:
                due_date_filter = self.current_filters['due_date']
                stmt = stmt.filter(Task.due_date == due_date_filter)

            if 'priority' in self.current_filters:
                priority_filter = self.current_filters['priority']
                stmt = stmt.filter(Task.priority == priority_filter)

            if 'category' in self.current_filters:
                category_filter = self.current_filters['category']
                stmt = stmt.join(Task.categories).filter(Category.name == category_filter)

            # Apply sorting
            if self.current_sort == "Priority":
                priority_order = case(
                    (Task.priority == 'HIGH', 1),
                    (Task.priority == 'MEDIUM', 2),
                    (Task.priority == 'LOW', 3),
                    else_=4
                )
                stmt = stmt.order_by(priority_order)
            elif self.current_sort == "Due Date":
                stmt = stmt.order_by(Task.due_date.asc())
            elif self.current_sort == "Category":
                stmt = stmt.outerjoin(Task.categories).order_by(func.coalesce(Category.name, "").asc())

            tasks = session.execute(stmt).scalars().all()

            # Clear the current task list before repopulating
            self.ids.task_list.clear_widgets()

            # Populate tasks into the list view
            for task in tasks:
                self.add_task(
                    task.id,
                    task.name,
                    priority=task.priority,
                    due_date=task.due_date,
                    categories=[category.name for category in task.categories],
                    complete=task.complete
                )

    def on_task_click(self, task_id):
        """Handle click event on a task."""
        print(f"Task {task_id} clicked")
        # You can add logic for editing or viewing task details here.

    def toggle_complete(self, checkbox, task_id, task_box):
        """Handle toggling the completion state of a task."""
        with db.get_session() as session:
            task = session.get(Task, task_id)
            task.complete = checkbox.active  # Update the completion status
            session.commit()

            # Update the task box appearance
            if task.complete:
                self.grey_out_task(task_box)
            else:
                self.reset_task_appearance(task_box)

    def grey_out_task(self, task_box):
        """Grey out the task when it is marked complete."""
        task_box.opacity = 0.5  # Reduce opacity to indicate completion
        task_box.check_box.disabled = True  # Disable the checkbox for completed tasks

    def reset_task_appearance(self, task_box):
        """Restore the task's appearance when marked incomplete."""
        task_box.opacity = 1  # Restore full opacity
        task_box.check_box.disabled = False  # Re-enable the checkbox

    def sort_tasks(self, sort_option):
        """Set the sorting option and repopulate the list."""
        self.current_sort = sort_option
        self.populate()  # Re-populate tasks based on the new sorting option
        print(f"Sorted by {sort_option}")  # Log the sorting option used

    def filter_tasks(self, filter_option, value):
        """Set the filter option and value, then repopulate the list."""
        self.current_filters[filter_option] = value
        self.populate()  # Re-populate tasks based on the current filters
        print(f"Filtered by {filter_option} = {value}")  # Log the filter used
