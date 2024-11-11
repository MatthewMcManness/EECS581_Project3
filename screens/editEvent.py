# ----------------------------------------------------------------------------- 
# Name: editEvent.py 
# Description: This module defines the EditEventModal class, which provides a
#              modal interface to edit an event within the BusyBee application.
# Programmer: Shravya Matta
# Date Created: November 8, 2024
# Revision History:
# - November 8, 2024: Initial version created for editing events (Author: Shravya Matta)
#
# Preconditions:
# - Kivy framework must be installed and configured properly.
# - The `DatePicker` and `RepeatOptionsModal` must be accessible within screens/usefulwidgets.
#
# Postconditions:
# - This modal allows updating or deleting events and modifies the Event ListView.
#
# Error Handling:
# - If the event title is missing, the event will not be saved, and an error message will be printed.
#
# Side Effects:
# - Updates the event list and modifies the Event ListView when events are saved or deleted.
#
# Known Faults:
# - None
# -----------------------------------------------------------------------------

# Import necessary Kivy modules and custom widgets
from kivy.uix.modalview import ModalView  # Modal for event editing
from kivy.uix.boxlayout import BoxLayout  # Layout for organizing widgets
from kivy.uix.textinput import TextInput  # Input fields for user text
from kivy.uix.spinner import Spinner  # Dropdown-style component for categories
from kivy.uix.button import Button  # Standard button widget
from kivy.uix.label import Label  # Label widget for displaying text
from kivy.app import App  # Ensure App is imported
from Models import Event, Category  # Event and Category classes
from database import get_database  # To connect to the database
from sqlalchemy import select  # To query the database
from datetime import datetime  # For event date and time

db = get_database()  # Get the database connection

class EditEventModal(ModalView):
    def __init__(self, event_id=None, refresh_callback=None, **kwargs):
        """Initialize the EditEventModal with layout components, loading event data if editing."""
        super().__init__(**kwargs)
        self.event_id = event_id  # Store event ID for editing
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False
        self.refresh_callback = refresh_callback  # Store the refresh callback

        # Load categories from the database
        with db.get_session() as session, session.begin():
            stmt = select(Category).where(True)
            results = session.scalars(stmt).all()
            self.categories = [result.name for result in results]
            self.categories_ids = [result.id for result in results]

        self.selected_categories = []

        # Create layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title input for event name
        self.title_input = TextInput(hint_text="Event Title")
        layout.add_widget(self.title_input)

        # Date and time section
        date_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.date_label = Label(text="Pick a date & time", size_hint_x=0.8)
        date_layout.add_widget(self.date_label)
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        date_layout.add_widget(pick_date_button)
        layout.add_widget(date_layout)

        # Notes input for event description
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner for selecting event categories
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

        # Action buttons (Save, Delete, Cancel)
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="DELETE", on_release=self.delete_event))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_event))
        layout.add_widget(button_layout)

        self.add_widget(layout)

        # Load existing event data if editing
        if event_id:
            self.load_event(event_id)

    def load_event(self, event_id):
        """Load event data into fields for editing."""
        with db.get_session() as session, session.begin():
            event = session.query(Event).filter_by(id=event_id).first()
            if event:
                self.title_input.text = event.name
                self.notes_input.text = event.notes
                self.date_label.text = f"Event on: {event.event_time.strftime('%Y-%m-%d %H:%M')}" if event.event_time else "Pick a date & time"
                self.selected_categories = [category.name for category in event.categories]
                self.update_applied_categories()

    def save_event(self, *args):
        """Save the event, updating if it exists or creating a new one."""
        if not self.title_input.text:
            print("Event Title is required.")
            return

        # Collect data from the modal
        name = self.title_input.text
        notes = self.notes_input.text
        event_time = self.date_label.text.split(" ", 1)[1] if "Event on:" in self.date_label.text else None
        event_time = datetime.strptime(event_time, "%Y-%m-%d %H:%M") if event_time else None

        # Retrieve category instances
        selected_category_ids = [cat_id for cat_id, cat in zip(self.categories_ids, self.categories) if cat in self.selected_categories]

        with db.get_session() as session:
            if self.event_id:
                # Update existing event
                event = session.query(Event).filter_by(id=self.event_id).first()
                event.name = name
                event.notes = notes
                event.event_time = event_time
                event.categories = session.query(Category).filter(Category.id.in_(selected_category_ids)).all()
            else:
                # Create new event
                event = Event(name=name, notes=notes, event_time=event_time)
                event.categories = session.query(Category).filter(Category.id.in_(selected_category_ids)).all()
                session.add(event)

            # Commit the session and capture the event ID
            session.commit()
            event_id = event.id  # Capture the ID before the session closes

        if self.refresh_callback:
            self.refresh_callback()

        print(f"Event {'updated' if self.event_id else 'saved'} with ID: {event_id}")
        self.dismiss()

    def delete_event(self, *args):
        """Delete the event from the database."""
        if self.event_id:
            with db.get_session() as session, session.begin():
                event = session.query(Event).filter_by(id=self.event_id).first()
                if event:
                    session.delete(event)
            print(f"Event with ID {self.event_id} deleted.")

            # Call the refresh callback to update the event list after deletion
            if self.refresh_callback:
                self.refresh_callback()

            self.dismiss()

    def open_date_picker(self, instance):
        """Open the DatePicker modal to select a date and time."""
        DatePicker(self).open()

    def on_category_selected(self, spinner, text):
        """Handle category selection from the spinner."""
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
