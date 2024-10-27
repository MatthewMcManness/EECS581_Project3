from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from screens.usefulwidgets import DatePicker
from screens.usefulwidgets import TimePicker
from screens.usefulwidgets import RepeatOptionsModal  # Import RepeatOptionsModal
from screens.usefulwidgets import CategoryModal  # Import CategoryModal
#
# Import necessary modules from Kivy and Python standard libraries
from kivy.lang import Builder  # To load .kv files for UI definitions
from kivy.uix.boxlayout import BoxLayout  # Layout class to organize widgets horizontally or vertically
from kivy.uix.modalview import ModalView  # For pop-up windows (modals)
from kivy.uix.popup import Popup  # Another kind of popup (used for the date picker)
from kivy.uix.label import Label  # Display text on the UI
from kivy.uix.gridlayout import GridLayout  # Arrange widgets in a grid layout
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen  # Manage switching between screens
from kivy.uix.textinput import TextInput  # Input field for entering text
from kivy.uix.button import Button  # Standard button widget
from kivy.uix.spinner import Spinner  # Dropdown-style component to select from options
from kivy.uix.relativelayout import RelativeLayout  # Used in populate_calendar
from kivy.metrics import dp  # For density-independent pixels
from kivy.properties import StringProperty  # Reactive property to update the label
from kivy.app import App  # Main class for running the Kivy app
from kivy.clock import Clock
from calendar import monthcalendar  # To generate the month's calendar layout
from datetime import datetime, timedelta  # For working with dates and times

class AddTaskModal(ModalView):
    #A modal for adding a new task.
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the modal
        self.size_hint = (0.9, 0.9)  # Set the size of the modal
        self.auto_dismiss = False  # Prevent automatic dismissal when clicking outside

        # Predefined categories and selected categories list
        self.categories = ["Work", "Personal", "School"]
        self.selected_categories = []

        # Create the main layout for the modal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for task title
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

        # Input field for notes
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner to select or add new categories
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

        # Layout to display selected categories
        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        # Action buttons to cancel or save the task
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        # Add the layout to the modal
        self.add_widget(layout)

    def open_date_picker(self, instance):
        #Open the DatePicker popup.
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        #Open the Repeat Options modal.#
        RepeatOptionsModal(self).open()

    def on_category_selected(self, spinner, text):
        #Handle category selection.#
        if text == "Add New Category":
            CategoryModal(self).open()
        elif text not in self.selected_categories:
            self.selected_categories.append(text)
            self.update_applied_categories()

    def update_applied_categories(self):
        #Update the applied categories layout.#
        self.applied_categories_layout.clear_widgets()
        for category in self.selected_categories:
            label = Label(text=category)
            self.applied_categories_layout.add_widget(label)
    
    def update_category_spinner(self):
        #Update the spinner with the current list of categories.#
        self.category_spinner.values = self.categories + ["Add New Category"]

    def save_task(self, *args):
        #Save the task and add it to the To-Do List.#
        task_data = {
            "title": self.title_input.text,
            "deadline": self.deadline_label.text,
            "repeats": self.repeat_button.text,
            "notes": self.notes_input.text,
            "categories": self.selected_categories,
        }

        if not task_data["title"]:
            print("Task Title is required.")
            return

        # Find the ToDoListView screen in the ScreenManager and add the task
        todo_screen = self.app.screen_manager.get_screen('todo')
        todo_screen.add_task(task_data)

        print("Task Saved:", task_data)
        self.dismiss()  # Close the modal
