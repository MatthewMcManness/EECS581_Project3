# Prologue Comments:
# Code Artifact: CalendarView Class Definition
# Brief Description: This code defines the `CalendarView` class for displaying a monthly calendar
# with functionality to navigate months and select days. It also updates the display with the 
# current month and year and populates the calendar dynamically using a grid layout.
# Programmer: Matthew McManness (2210261) and
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of calendar view structure (just a placeholder for navigation) - [Matthew McManness]
#   - [Insert Further Revisions]: [Brief description of changes] - [Your Name]
#   - November 10, 2024: Updated what Manvir added to make it stack events correctly - [Matthew McManness]
#   - November 10, 2024: updated the calendar view so that the week starts on a Sunday - Matthew McManness

# Preconditions:
#   - The `.kv` file must define a `calendar_grid` widget ID to correctly render the calendar grid.
#   - The app must have valid Kivy widgets and dependencies available (e.g., Button, Label, etc.).
# Acceptable Input:
#   - Increment values of 1 or -1 to navigate months.
#   - A day button press to select a specific day.
# Unacceptable Input:
#   - Increment values outside expected range result in incorrect month/year changes.
# Postconditions:
#   - The calendar view updates with the current month and day selection.
#   - Displays a console message when a day is selected.
# Return Values:
#   - None. The methods rely on UI updates and side effects.
# Error and Exception Conditions:
#   - If `calendar_grid` ID is not found, it logs an error message.
# Side Effects:
#   - Updates the calendar dynamically on month changes or day selection.
# Invariants:
#   - The view always displays the current month and updates on navigation.
# Known Faults:
#   - None identified.

# Import necessary modules from Kivy and Python standard libraries.
from kivy.graphics import Color, Rectangle # to control color and size of event background
from kivy.lang import Builder  # Load .kv files for UI definitions.
from kivy.uix.boxlayout import BoxLayout  # Organize widgets horizontally/vertically.
from kivy.uix.modalview import ModalView  # Define modals (pop-up windows).
from kivy.uix.popup import Popup  # Create pop-ups (used for date picker).
from kivy.uix.label import Label  # Display text in the UI.
from kivy.uix.gridlayout import GridLayout  # Arrange widgets in a grid layout.
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen  # Manage screens.
from kivy.uix.textinput import TextInput  # Input field for text entry.
from kivy.uix.button import Button  # Standard button widget.
from kivy.uix.spinner import Spinner  # Dropdown for selecting from options.
from kivy.uix.relativelayout import RelativeLayout  # Layout used in calendar population.
from kivy.metrics import dp  # Use density-independent pixels for UI scaling.
from kivy.properties import StringProperty, ObjectProperty  # Property to update UI reactively.
from kivy.app import App  # Main class to run the Kivy app.
from kivy.clock import Clock  # Schedule functions after a delay.
from calendar import monthcalendar  # Generate calendar layout for a given month.
from datetime import datetime, timedelta  # Work with dates and times.
from database import get_database # to connect to database
from sqlalchemy import select, extract # to query database
from Models import Event_ # task model class
from kivy.uix.anchorlayout import AnchorLayout  # Import for anchoring widgets
from kivy.graphics import Color, Rectangle, RoundedRectangle  # Import for rounded rectangle backgrounds
import calendar  # Import calendar for setting first day of the week

# Set the first day of the week to Sunday
calendar.setfirstweekday(calendar.SUNDAY)



db = get_database() # get database

class EventBox(BoxLayout):
    """A BoxLayout to hold event details"""
    event_id = ObjectProperty(None)
        
    def __init__(self, **kwargs):
        """Initialize the Eventkbox"""
        super().__init__(**kwargs) # initialize BoxLayout class
        # initialize sixe of event box and make it's background color white
        with self.canvas.before:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # when eventbox is updated, make sure size is correct
        self.bind(size=self.update_rect, pos=self.update_rect)
    def update_rect(self, *args):
        """Update rectanlge to match the size and position of the EventBox"""
        self.rect.pos = self.pos
        self.rect.size = self.size
        
class CalendarView(Screen):
    """Displays a monthly calendar with navigational buttons and day selection."""

    month_year_text = StringProperty()  # Reactive property for month and year text.

    def __init__(self, **kwargs):
        """Initialize the calendar with the current month and year."""
        super().__init__(**kwargs)  # Initialize the superclass.
        now = datetime.now()  # Get the current date and time.
        self.current_year = now.year  # Store the current year.
        self.current_month = now.month  # Store the current month.
        self.update_month_year_text()  # Update the month-year text display.

    def on_kv_post(self, base_widget):
        """Populate the calendar after the KV file has loaded."""
        if 'calendar_grid' in self.ids:  # Check if the grid is defined in the KV file.
            # Use the Clock to schedule the population to ensure the UI is fully loaded.
            Clock.schedule_once(lambda dt: self.populate_calendar())
        else:
            print("Error: 'calendar_grid' not found in ids.")  # Log error if grid not found.

    def update_month_year_text(self):
        """Update the label to show the current month and year."""
        self.month_year_text = datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def change_month(self, increment):
        """Change the month based on the given increment and repopulate the calendar."""
        self.current_month += increment  # Adjust the month.
        # Handle year change when month goes out of bounds.
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_month_year_text()  # Update the month-year text.
        self.populate_calendar()  # Repopulate the calendar grid.

    def populate_calendar(self):
        """Generate the calendar grid with day buttons."""
        grid = self.ids['calendar_grid']  # Get the calendar grid from the KV file.
        grid.clear_widgets()  # Clear any existing widgets from the grid.

        # Get the calendar layout for the current month.
        cal = monthcalendar(self.current_year, self.current_month)

        # Populate the grid with days of the month.
        for week in cal:
            for day in week:
                if day == 0:
                    # Add an empty label for non-days (blank spaces).
                    grid.add_widget(Label())
                else:
                    # Create a relative layout for each day cell.
                    cell = BoxLayout(orientation = 'vertical', spacing = -20)
                    container = RelativeLayout(size_hint=(1, None), height=dp(60))

                    # Create a label to display the day number.
                    day_label = Label(
                        text=str(day),
                        size_hint=(None, None),
                        size=(dp(20), dp(20)),
                        pos_hint={'right': 1, 'top': 1},
                        color=(0, 0, 0, 1)  # Black text color.
                    )

                    # Create a button for the day, which responds to clicks.
                    day_button = Button(
                        background_normal="",
                        background_color=(0.9, 0.9, 0.9, 1),  # Light gray background.
                        on_press=self.on_day_press,  # Bind to day press event.
                        size_hint=(1, 1),  # Make the button fill the cell.
                        text=""  # No text on the button itself.
                    )

                    # Add the button and label to the cell.
                    container.add_widget(day_button)
                    cell.add_widget(day_label)
                    container.add_widget(cell)

                    # Add the cell to the calendar grid.
                    grid.add_widget(container)
        self.populate()

    def on_day_press(self, instance):
        """Handle the event when a day button is pressed."""
        day_text = instance.parent.children[1].text  # Get the selected day number.
        print(f"You selected day: {day_text}")  # Print the selected day to the console.

    def add_event(self, event_id, name, start_time, place=None):
        """
        Add a new event to the calendar with a colored button for each event.

        Parameters:
            event_id (int): The ID of the event.
            name (str): The name of the event.
            start_time (datetime or str): The start date and time of the event.
            place (Optional[str]): The location of the event (if available).
        """
        # Convert start_time to datetime if it’s a string
        if isinstance(start_time, str):
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            except ValueError:
                print(f"Error: Incorrect date format for event '{name}'. Expected '%Y-%m-%d %H:%M'.")
                return  # Exit the function if date format is incorrect

        # Create a Button for the event with rounded corners and padding
        event_button = Button(
            text=f"{name} ({start_time.strftime('%H:%M')})",  # Display name and formatted time
            size_hint_y=None,
            height=dp(15),  # Set a fixed, smaller height for each event button
            background_normal="",
            background_color=(0.7, 0.3, 0.3, 1),  # Change color as desired
            on_press=lambda instance: self.on_event_click(event_id)
        )

        # Use canvas instructions to round the button's corners
        with event_button.canvas.before:
            Color(0.7, 0.3, 0.3, 1)  # Same color as background_color
            event_button.rect = RoundedRectangle(
                size=event_button.size,
                pos=event_button.pos,
                radius=[(dp(5), dp(5), dp(5), dp(5))]  # Rounded corners
            )

        # Bind button size and position updates to keep the rounded rectangle in sync
        event_button.bind(size=lambda inst, val: setattr(inst.rect, 'size', val))
        event_button.bind(pos=lambda inst, val: setattr(inst.rect, 'pos', val))

        # Retrieve the cell widget for the event's start date
        cell = self.get_cell_widget(start_time)
        if cell:
            # Check if an AnchorLayout exists in the cell; if not, create one
            if not cell.children or not isinstance(cell.children[0], AnchorLayout):
                # Create an AnchorLayout to anchor events to the top
                anchor_layout = AnchorLayout(anchor_y='top', size_hint_y=None, height=dp(60))
                events_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=(2, 2))  # Small padding for spacing
                events_layout.bind(minimum_height=events_layout.setter('height'))
                anchor_layout.add_widget(events_layout)
                cell.add_widget(anchor_layout)
            else:
                events_layout = cell.children[0].children[0]  # Access the BoxLayout inside AnchorLayout

            # Add the new event button to the layout
            events_layout.add_widget(event_button)

            # Sort events within the layout by start time after all events are added
            sorted_events = []
            for btn in events_layout.children:
                time_str = btn.text.split("(")[-1].strip(")")
                try:
                    event_time = datetime.strptime(time_str, '%H:%M')
                    sorted_events.append((event_time, btn))
                except ValueError:
                    print(f"Skipping button with invalid time format: {btn.text}")
                    continue

            # Sort events by time and only keep the first 2
            sorted_events = sorted(sorted_events, key=lambda x: x[0])
            display_events = sorted_events[:2]

            # Clear and re-add only the top 2 events at the top
            events_layout.clear_widgets()
            for _, sorted_event in display_events:
                events_layout.add_widget(sorted_event)

            # If there are more than 2 events, add a "More..." label
            if len(sorted_events) > 2:
                more_label = Label(
                    text="More...",
                    size_hint_y=None,
                    height=dp(15),  # Reduced height for the "More..." label as well
                    color=(0.5, 0.5, 0.5, 1)  # Grey color for the "More..." label
                )
                events_layout.add_widget(more_label)

            print(f"Added event: {event_id} - {name} on {start_time}")
            

    
    def get_cell_widget(self, date_obj):
        """Retrieve the widget for the specified date."""
        # Parse the date string into a datetime object
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M')

        target_day = date_obj.day
        target_month = date_obj.month
        target_year = date_obj.year

        # Check if the date is in the current calendar view
        if target_month != self.current_month or target_year != self.current_year:
            print("Error: The specified date is not in the current month or year.")
            return None

        # Get the calendar layout for the current month
        cal = monthcalendar(self.current_year, self.current_month)

        # Locate the widget for the target day in calendar_grid
        grid = self.ids['calendar_grid']
        widget_index = 0
        for week in cal:
            for day in week:
                if day == target_day:
                    # Found the target day; retrieve the widget
                    return grid.children[len(grid.children) - widget_index - 1]
                widget_index += 1

        print("Error: Day widget not found.")
        return None
    
    def populate(self):
        """Retrieve and display events for the current month."""
        session = db.get_session()
        try:
            stmt = select(Event_).where(
                extract("year", Event_.start_time) == self.current_year,
                extract("month", Event_.start_time) == self.current_month
            )
            events = session.scalars(stmt).all()
            events.sort(key=lambda event: event.start_time)  # Sort events by start time

            for event in events:
                start_time = event.start_time if isinstance(event.start_time, datetime) else datetime.strptime(event.start_time, "%Y-%m-%d %H:%M")
                self.add_event(event.id, event.name, start_time, event.place)
        finally:
            session.close()
