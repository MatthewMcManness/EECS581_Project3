from kivy.app import App  # Import the App class from Kivy
from kivy.uix.screenmanager import ScreenManager, NoTransition

from screens.calendarview import CalendarView  # Absolute imports
from screens.todolistview import ToDoListView
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
from screens.addevent import AddEventModal  # Import AddEventModal
from screens.addtask import AddTaskModal  # Import AddTaskModal

class BusyBeeApp(App):
    """Main app class to manage screens and modals."""

    def build(self):
        # Create a ScreenManager to manage the screens
        self.screen_manager = ScreenManager(transition=NoTransition())

        # Add the CalendarView and ToDoListView screens
        self.screen_manager.add_widget(CalendarView(name="calendar"))
        self.screen_manager.add_widget(ToDoListView(name="todo"))

        return self.screen_manager

    def open_add_task_modal(self):
        """Open the Add Task modal."""
        add_task_modal = AddTaskModal()  # Create an instance of AddTaskModal
        add_task_modal.open()

    def open_add_event_modal(self):
        """Open the Add Event modal."""
        add_event_modal = AddEventModal()  # Create an instance of AddEventModal
        add_event_modal.open()

    def switch_to_screen(self, screen_name):
        """Switch between Calendar and To-Do List screens."""
        self.screen_manager.current = screen_name
