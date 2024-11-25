#
#
#
# - November 24, 2024, changed the code to make DailyView inherit from Screen (to work with the Screen Manager) (Updated by: Matthew McManness)
#
#
from kivy.uix.screenmanager import Screen  # Change inheritance from BoxLayout to Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.uix.label import Label

class DailyView(Screen):  # Change inheritance to Screen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()
        Clock.schedule_once(lambda dt: self.update_date_label())  # Delay update
        Clock.schedule_once(lambda dt: self.populate_events())

    def update_date_label(self):
        """Updates the date label to show the current date."""
        self.ids.date_label.text = self.current_date.strftime("%B %d, %Y")

    def navigate_previous_day(self):
        """Navigate to the previous day."""
        self.current_date -= timedelta(days=1)
        self.update_date_label()
        self.populate_events()

    def navigate_next_day(self):
        """Navigate to the next day."""
        self.current_date += timedelta(days=1)
        self.update_date_label()
        self.populate_events()

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
