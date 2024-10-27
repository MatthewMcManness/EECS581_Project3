# Prologue Comments:
# Code Artifact: AddEventModal Class Definition
# Brief Description: This code defines the `AddEventModal` class, which provides a pop-up modal for creating 
# new events. Users can input an event name and select a date and time using a date picker widget.
# Programmer: Matthew McManness (2210261), and 
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of event modal structure (placeholder for navigation) - [Matthew McManness]
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
from screens.usefulwidgets import DatePicker  # Custom date picker modal.
from screens.usefulwidgets import TimePicker  # Custom time picker modal.

class AddEventModal(ModalView):
    """A modal for adding a new event with name, date, and time selection."""

    def __init__(self, **kwargs):
        """Initialize the event modal with input fields and buttons."""
        super().__init__(**kwargs)  # Initialize the superclass.

        self.size_hint = (0.8, 0.5)  # Set modal size relative to the screen size.
        self.auto_dismiss = False  # Prevent the modal from closing when clicked outside.

        # Create a vertical layout to hold the widgets.
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for the event name (non-multiline).
        self.event_name_input = TextInput(hint_text="Event Name", multiline=False)
        layout.add_widget(self.event_name_input)  # Add input field to the layout.

        # Label to display the selected event date and time.
        self.event_date_label = Label(text="Pick Event Date & Time")
        layout.add_widget(self.event_date_label)  # Add label to the layout.

        # Button to open the date picker modal.
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        layout.add_widget(pick_date_button)  # Add the button to the layout.

        # Layout for the action buttons (Cancel and Save).
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))  # Cancel button.
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_event))  # Save button.
        layout.add_widget(button_layout)  # Add the button layout to the main layout.

        # Add the complete layout to the modal.
        self.add_widget(layout)

    def open_date_picker(self, instance):
        """Open the DatePicker modal to select the event date and time."""
        DatePicker(self).open()  # Open the date picker modal.

    def save_event(self, *args):
        """Save the event details and validate input."""
        event_name = self.event_name_input.text.strip()  # Get the trimmed event name.
        event_date = self.event_date_label.text  # Get the selected event date from the label.

        # Ensure the event name is not empty before saving.
        if not event_name:
            print("Event Name is required.")  # Print error if the name is empty.
            return  # Stop execution to prevent saving.

        # Print the saved event details to the console.
        print(f"Event '{event_name}' scheduled for {event_date}")
        self.dismiss()  # Close the modal after saving.
