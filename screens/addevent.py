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
from database import get_database # to connect to database
from datetime import datetime # for date
from sqlalchemy import select # to query database
from Models.databaseEnums import Frequency # for event frequency
from Models import Event_, Recurrence # event model

db = get_database()

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
        date_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.event_date_label = Label(text="Pick Event Date & Time")
        date_layout.add_widget(self.event_date_label)  # Add label to the layout.

        # Button to open the date picker modal.
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        date_layout.add_widget(pick_date_button)  # Add the button to the layout.
        layout.add_widget(date_layout)

        # Button to open the Repeat Options modal
        self.repeat_button = Button(text=Frequency.frequency_options()[0], on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        # Input field for additional task notes
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)
        
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

    def open_repeat_window(self, instance):
        """Open the RepeatOptionsModal to choose a repeat option."""
        RepeatOptionsModal(self).open()

    def save_event(self, *args):
        """Save the event details and validate input."""
        event_name = self.event_name_input.text.strip()  # Get the trimmed event name.
        event_date = self.event_date_label.text  # Get the selected event date from the label.

        # Ensure the event name is not empty before saving.
        if not self.event_name_input.text or self.event_date_label.text == "Pick Event Date & Time":
            print("Event Name and Datetime are required.")  # Print error if the name is empty.
            return  # Stop execution to prevent saving.
        
        # gets info from inputs
        name = self.event_name_input.text
        notes = self.notes_input.text
        date = self.event_date_label.text
        repeat_info = self.repeat_button.text.split(" ")
        frequency = None if len(repeat_info) == 2 else Frequency.str2enum(repeat_info[0])
        times = None if len(repeat_info) == 2 else int(repeat_info[1].split(" ")[0].replace("(", ""))

        #connection to the database
        with db.get_session() as session:
            with session.begin(): # transaction started that will auto commit before exiting
                # collecting event data
                new_event = Event_(name = name, notes = notes)
                
                # Add the date of the event
                date = (" ").join(self.event_date_label.text.split(" ")[2:])
                new_event.start_time = datetime.strptime(date, "%Y-%m-%d %H:%M") # adding date and time to the event
                
                # Add the event to the session
                session.add(new_event)
                
                # Add recurrence and create other events, if needed
                if times and frequency:
                    recurrence_id = self.save_recurrence(frequency, times) # save recurrence
                    new_event.recurrence_id = recurrence_id # add recurrence to event

                    # create other events
                    current_date = new_event.start_time
                    for _ in range(times - 1):
                        new_date = frequency.get_next_date(current_date, new_event.start_time)

                        # create event with same info as new_event but update the date
                        event_i = Event_( 
                            name=new_event.name,
                            notes=new_event.notes,
                            start_time=new_date,
                            recurrence_id=recurrence_id
                        )
                        current_date = new_date # save date to calculate next one
                        session.add(event_i)

                # Log message
                print(f"Saving event: {new_event}")

            event_id = new_event.id # get new_event id
            
        # Access the running app
        app = App.get_running_app()
        calendar_screen = app.screen_manager.get_screen('calendar')

        # If repeating events, add them all to the Calendar screen
        if times and frequency:
            with db.get_session() as session: # start session to get all events
                stmt = select(Event_).where(Event_.recurrence_id == recurrence_id) # sql statement
                events = session.scalars(stmt) # query database

                for event in events:
                    calendar_screen.add_event(event.id, event.name, event.start_time, frequency=frequency, times=times)
        
        # Otherwise, add the single event to the Calendar screen
        else:
            calendar_screen.add_event(event_id, name, date)

        # Print the saved event details to the console.
        print(f"Event '{event_name}' scheduled for {event_date}")
        self.dismiss()  # Close the modal after saving.

    def save_recurrence(self, frequency:Frequency, times:int) -> int:
        """Saves the given recurrence and returns its id"""
        with db.get_session() as session: # start session 
            with session.begin(): # begin transaction, create and save event
                recurrence = Recurrence(times=times, frequency=frequency)
                session.add(recurrence)
            id = recurrence.id # store event id to return 
        
        return id