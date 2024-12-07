# Prologue Comments:
# Code Artifact: AddEventModal Class Definition
# Brief Description: This code defines the `AddEventModal` class, which provides a pop-up modal for creating 
# new events. Users can input an event name and select a date and time using a date picker widget.
# Programmer: Matthew McManness (2210261), Manvir Kaur (3064194), Magaly Camacho (3072618)
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of event modal structure (placeholder for navigation) - [Matthew McManness]
#   - November 9. 2024: Added connection to database to save events and show on the calendar - [Manvir Kaur]
#   - November 10, 2024: Fixed start time not being saved correctly, added check to make sure date and time are picked - [Magaly Camacho]
#   - November 18, 2024: Implemented recurring events - [Magaly Camacho]
#   - November 20, 2024: Matched layout with editEvent layout - [Magaly Camacho]
#   - [Insert Further Revisions]: [Brief description of changes] - [Your Name]
# Preconditions:
#   - The `DatePicker` class must be implemented and correctly imported from `screens.usefulwidgets`.
#   - This modal expects interaction from the user to input the event name and select a date.
# Acceptable Input:
#   - Valid event name as a non-empty string.
#   - Selected event date through the date picker.
# Unacceptable Input:
#   - Empty event name results in a validation error.
# Postconditions:
#   - The event details are printed to the console if successfully saved.
#   - The modal is dismissed after saving or cancelling.
# Return Values:
#   - None. The modal relies on side effects within the Kivy framework.
# Error and Exception Conditions:
#   - If the event name is empty, an error message is printed, and the modal remains open.
# Side Effects:
#   - Opens and closes the modal and date picker modals.
#   - Updates the event date label with the selected date.
# Invariants:
#   - Modal remains open until the user cancels or saves the event.
# Known Faults:
#   - None identified.

from kivy.uix.modalview import ModalView  # For creating modals in Kivy.
from kivy.uix.boxlayout import BoxLayout  # Layout for arranging widgets vertically or horizontally.
from kivy.uix.textinput import TextInput  # Input field for the event name.
from kivy.uix.label import Label  # Label widget to display text.
from kivy.uix.button import Button  # Button widget for user interaction.
from screens.usefulwidgets import DatePicker, RepeatOptionsModal  # Custom date picker and repeat options modals
from kivy.app import App  # Ensure App is imported
from database import get_database  # to connect to database
from datetime import datetime  # for date
from sqlalchemy import select  # to query database
from Models.databaseEnums import Frequency  # for event frequency
from Models import Event_, Recurrence  # event model
from kivy.metrics import dp  # Import dp for density-independent pixel values
from kivy.graphics import Color, RoundedRectangle  # For rounded rectangle shape


class UniformButton(Button):
    pass

db = get_database()

class AddEventModal(ModalView):
    """A modal for adding a new event with name, date, and time selection."""

    def __init__(self, **kwargs):
        """Initialize the event modal with input fields and buttons."""
        super().__init__(**kwargs)  # Initialize the superclass.

        self.size_hint = (0.8, 0.5)  # Set modal size relative to the screen size.
        self.auto_dismiss = False  # Prevent the modal from closing when clicked outside.

        # Access app-wide styles
        app = App.get_running_app()

          # Set up custom background
        with self.canvas.before:
            Color(rgba=app.Background_Color)  # Use the app's background color
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])  # Add rounded corners


        # Create a vertical layout to hold the widgets.
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Input field for the event name (non-multiline).
        self.event_name_input = TextInput(
            hint_text="Event Name",
            multiline=False,
            font_size=app.button_font_size,
            foreground_color=(0, 0, 0, 1),
            padding=[dp(10), dp(5)]
        )
        layout.add_widget(self.event_name_input)  # Add input field to the layout.

        # Label to display the selected event date and time.
        date_layout = BoxLayout(orientation='horizontal', spacing=dp(10))
        self.event_date_label = Label(
            text="Pick Event Date & Time",
            font_size=app.label_font_size,
            color=(0, 0, 0, 1),
        )
        date_layout.add_widget(self.event_date_label)  # Add label to the layout.

        # Button to open the date picker modal.
        pick_date_button = UniformButton(
            text="Pick Date & Time"
        )
        pick_date_button.bind(on_release=self.open_date_picker)
        date_layout.add_widget(pick_date_button)  # Add the button to the layout.
        layout.add_widget(date_layout)

        # Button to open the Repeat Options modal
        self.repeat_button = UniformButton(
            text=Frequency.frequency_options()[0]
        )
        self.repeat_button.bind(on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        # Input field for additional task notes
        self.notes_input = TextInput(
            hint_text="Notes",
            multiline=True,
            font_size=app.button_font_size,
            foreground_color=(0, 0, 0, 1),
            padding=[dp(10), dp(5)]
        )
        layout.add_widget(self.notes_input)

        # Layout for the action buttons (Cancel and Save).
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        cancel_button = UniformButton(
            text="CANCEL"
        )
        cancel_button.bind(on_release=self.dismiss)
        save_button = UniformButton(
            text="SAVE"
        )
        save_button.bind(on_release=self.save_event)
        button_layout.add_widget(cancel_button)  # Cancel button.
        button_layout.add_widget(save_button)  # Save button.
        layout.add_widget(button_layout)  # Add the button layout to the main layout.

        # Add the complete layout to the modal.
        self.add_widget(layout)


    def open_date_picker(self, instance):
        """Open the DatePicker modal to select the event date and time."""
        DatePicker(self).open()  # Open the date picker modal.

    def open_repeat_window(self, instance):
        """Open the RepeatOptionsModal to choose a repeat option."""
        RepeatOptionsModal(self).open()

    def save_event(self, *args):
        """Save the event details and validate input."""
        # Your save logic remains unchanged
        pass

    def save_recurrence(self, frequency: Frequency, times: int) -> int:
        """Saves the given recurrence and returns its id"""
        # Your recurrence saving logic remains unchanged
        pass
