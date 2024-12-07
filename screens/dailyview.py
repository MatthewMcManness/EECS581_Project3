# Prologue Comments:
# Code Artifact: DailyView Class Definition
# Brief Description: This code defines the `DailyView` class for displaying a the events on a given day
# Programmer: Matthew McManness (2210261), Mariam Oraby (3127776), Magaly Camacho (3072618)
# Date Created: October 26, 2024
# Dates Revised:
# - November 18, 2024, created the .py file to implement the Daily View (created by: Mariam Oraby)
# - November 24, 2024, changed the code to make DailyView inherit from Screen (to work with the Screen Manager) (Updated by: Matthew McManness)
# - December 7, 2024, Fixed setting date for dailyview, added prologue comments, made it so calendar view is refreshed when an event is edited - [Magaly Camacho, Mariam Oraby, Manvir Kaur]
# - December 7, 2024: Implemented variables for ease of UI modification (Matthew McManness)

from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.app import App
from database import get_database
from sqlalchemy import select, extract
from Models import Event_
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle  
from screens.calendarview import CalendarView

db = get_database()

class EventBox(BoxLayout):
    """A BoxLayout to hold event details"""
    event_id = ObjectProperty(None)
        
    def __init__(self, **kwargs):
        """Initialize the EventBox"""
        super().__init__(**kwargs)  # Initialize BoxLayout class
        # Initialize size of EventBox and make its background color white
        with self.canvas.before:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # When EventBox is updated, make sure size is correct
        self.bind(size=self.update_rect, pos=self.update_rect)
    def update_rect(self, *args):
        """Update rectangle to match the size and position of the EventBox"""
        self.rect.pos = self.pos
        self.rect.size = self.size

class DailyView(Screen):  # Change inheritance to Screen
    selected_date = ObjectProperty(None)  
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()
        Clock.schedule_once(lambda dt: self.update_date_label())  # Delay update
        Clock.schedule_once(lambda dt: self.populate_events())
        self.app = App.get_running_app()

    def update_date_label(self):
        """Updates the date label to show the current date."""
        self.ids.date_label.text = self.current_date.strftime("%A %B %d, %Y").replace(" ", "\n", 1)
        print(self.current_date.strftime("%A %B %d, %Y"))

    def navigate_previous_day(self):
        """Navigate to the previous day."""
        self.current_date -= timedelta(days=1)
        self.set_date()

    def navigate_next_day(self):
        """Navigate to the next day."""
        self.current_date += timedelta(days=1)
        self.set_date()

    def populate_events(self):
        """Populate the event list for the current date."""
        event_list = self.ids.event_list
        event_list.clear_widgets()

        # Example of loading events
        example_events = [
            {"time": "08:00 AM", "title": "Meeting"},
            {"time": "01:00 PM", "title": "Lunch with Alex"},
            {"time": "05:00 PM", "title": "Gym"},
        ]

        for event in example_events:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
            time_label = Label(text=f"{event['time']} - {event['title']}")
            edit_button = Label(text="Edit", size_hint_x=0.2)
            box.add_widget(time_label)
            box.add_widget(edit_button)
            event_list.add_widget(box)

    def add_event(self):
        """Placeholder function to add a new event."""
        print("Add Event button clicked!")

    def on_kv_post(self, base_widget):
        """Populate events after the KV file is loaded."""
        if self.selected_date:
            self.populate_daily_events()

    def set_date(self, date_obj=None):
        """
        Set the selected date and refresh the events.
        """
        if date_obj is None:
            date_obj = self.current_date
        if isinstance(date_obj, str):
            self.selected_date = datetime.strptime(date_obj, '%Y-%m-%d')
        else:
            self.selected_date = date_obj
        self.ids['date_label'].text = self.selected_date.strftime('%A %B %d, %Y').replace(" ", "\n", 1)
        self.refresh_events()

    def refresh_events(self):
        """
        Fetch and display events for the selected date.
        """
        calendar_view:CalendarView = self.manager.get_screen('calendar')  # Access the CalendarView screen.
        calendar_view.refresh_calendar()
        if not self.selected_date:
            print("Error: No date selected.")
            return

        try:
            # Query events for the selected date
            session = db.get_session()
            start_of_day = datetime.combine(self.selected_date, datetime.min.time())
            end_of_day = datetime.combine(self.selected_date, datetime.max.time())

            stmt = select(Event_).where(
                Event_.start_time >= start_of_day,
                Event_.start_time <= end_of_day
            )

            events = session.scalars(stmt).all()
            self.display_events(events)
            session.close()
        except Exception as e:
            print(e)

    def display_events(self, events):
        """
        Display events in the `event_list`.
        """
        container = self.ids['event_list']
        container.clear_widgets()  # Clear existing widgets

        if not events:
            # Display a "No events" message if there are no events for the day
            container.add_widget(Label(text="No events for this day.", size_hint_y=None, height=dp(40)))
            return

        for event in events:
            self.add_event_to_container(event, container)

    def add_event_to_container(self, event, container):
        """
        Add a single event to the container.
        """
        event_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        # Display event name and time
        time_label = Label(
            text=event.start_time.strftime('%I:%M %p'),
            size_hint=(None, None),
            width=dp(80),
            height=dp(40),
            color=(0, 0, 0, 1)
        )
        event_label = Label(
            text=event.name,
            size_hint_y=None,
            height=dp(40),
            color=(0, 0, 0, 1)
        )
        
        # Add a button to edit the event
        edit_button = Button(
            text="Edit",
            size_hint=(None, None),
            width=dp(60),
            height=dp(40),
            on_press=lambda instance, event_id=event.id: self.open_edit_event_modal(event.id)
        )
        
        # Add widgets to the event box
        event_box.add_widget(time_label)
        event_box.add_widget(event_label)
        event_box.add_widget(edit_button)
        
        # Add the event box to the container
        container.add_widget(event_box)

    def open_edit_event_modal(self, event_id):
        """
        Open the Edit Event modal for the selected event.
        """
        from screens.editEvent import EditEventModal  # Import here to avoid circular imports

        edit_modal = EditEventModal(event_id=event_id, refresh_callback=self.refresh_events)
        edit_modal.open()

    def populate_daily_events(self):
        """Retrieve and display events for the selected day."""
        try:
            session = db.get_session()
            
            # Query events for the selected day
            stmt = select(Event_).where(
                extract("year", Event_.start_time) == self.selected_date.year,
                extract("month", Event_.start_time) == self.selected_date.month,
                extract("day", Event_.start_time) == self.selected_date.day
            )
            events = session.scalars(stmt).all()

            # Sort events by start time
            events.sort(key=lambda event: event.start_time)

            # Clear the current event list
            events_list = self.ids['event_list']
            events_list.clear_widgets()

            # Populate events in the list
            for event in events:
                event_box = EventBox()
                event_box.add_widget(Label(text=f"{event.start_time.strftime('%H:%M')} - {event.name}"))
                events_list.add_widget(event_box)
            
            session.close()
        
        except Exception as e:
            print(e)
