# Prologue Comments:
# Code Artifact: CalendarView Class Definition
# Brief Description: This code defines the `CalendarView` class for displaying a monthly calendar
# with functionality to navigate months and select days. It also updates the display with the 
# current month and year and populates the calendar dynamically using a grid layout.
# Programmer: Matthew McManness (2210261), Manvir Kaur (3064194), Mariam Oraby (3127776)
# Date Created: October 26, 2024
# Dates Revised:
#   - October 26, 2024: Initial creation of calendar view structure (just a placeholder for navigation) - [Matthew McManness]
#   - November 9, 2024: Added EventBox, connection to the database to add all events to the database and show up on the calendar - [Manvir Kaur]
#   - November 9, 2024: Updated the populate(), get_cell_widgets(), and populate_calendar() functions - [Mariam Oraby]
#   - November 10, 2024: Updated what Manvir and Mariam added to make it stack events correctly - [Matthew McManness]
#   - November 10, 2024: updated the calendar view so that the week starts on a Sunday - Matthew McManness
#   - November 10, 2024: Group modified to ensure event button clicks open the edit modal - [Whole Group]
#   - November 18, 2024: Implemented recurring events - [Magaly Camacho]
#   - December 5, 2024: Redid the add_event() to truncate names that were too long and added a hover feature to display the full name and time of events [Matthew McManness]
#
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
from screens.editEvent import EditEventModal  # Adjust the path if the file is located elsewhere
from kivy.core.window import Window


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




    def add_event(self, event_id, name, start_time, frequency=None, times=None, place=None):
        """
        Add a new event to the calendar with a styled hoverable modal for details.

        Parameters:
            event_id (int): The ID of the event.
            name (str): The name of the event.
            start_time (datetime or str): The start date and time of the event.
            place (Optional[str]): The location of the event (if available).
        """
        # Define a character limit for truncation
        char_limit = 15  # Adjust this value as needed

        # Truncate the event name if it exceeds the character limit
        display_name = name if len(name) <= char_limit else f"{name[:char_limit]}..."

        # Ensure start_time is a datetime object
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')

        # Create the event button
        event_button = Button(
            text=display_name,
            size_hint_y=None,
            height=dp(15),
            background_normal="",
            background_color=(0.7, 0.3, 0.3, 1),
            on_press=lambda instance, event_id=event_id: self.open_edit_event_modal(event_id)  # Pass event ID to the method
        )

        # Create a styled hover modal
        modal = ModalView(size_hint=(None, None), size=(200, 100), auto_dismiss=True)

        # Remove the default modal background
        modal.background = ""
        modal.background_color = (0, 0, 0, 0)
        
        # Add a custom background to the modal
        with modal.canvas.before:
            Color(0.7, 0.3, 0.3, 1)  # Match the event box color
            modal.rect = RoundedRectangle(size=modal.size, pos=modal.pos, radius=[dp(10), dp(10)])
        modal.bind(size=lambda instance, value: setattr(modal.rect, 'size', value))
        modal.bind(pos=lambda instance, value: setattr(modal.rect, 'pos', value))

        # Add a Label to display the full name and time, centered
        modal_layout = BoxLayout(orientation="vertical", padding=10, spacing=5)
        event_details = Label(
            text=f"{name}\n{start_time.strftime('%H:%M')}",
            color=(1, 1, 1, 1),  # White text
            halign="center",  # Center text horizontally
            valign="middle",  # Center text vertically
            size_hint=(1, 1)
        )
        event_details.bind(size=event_details.setter('text_size'))  # Make text wrap inside the box
        modal_layout.add_widget(event_details)
        modal.add_widget(modal_layout)

        # Add hover detection
        def on_mouse_move(window, pos):
            """Check if the mouse is over the button."""
            if event_button.collide_point(*event_button.to_widget(*pos)):
                if not modal.parent:
                    modal.open()
            else:
                if modal.parent:
                    modal.dismiss()

        # Bind mouse motion to hover detection
        Window.bind(mouse_pos=on_mouse_move)

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

            print(f"Added event: {event_id} - {display_name} on {start_time}")


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
    
    def refresh_calendar(self):
        grid = self.ids['calendar_grid']  # Get the calendar grid from the KV file.
        grid.clear_widgets()  # Clear any existing widgets from the grid.
        self.populate_calendar()
        #self.populate()


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

    def open_edit_event_modal(self, event_id):
        """Open the Edit Event modal for a specific event ID and refresh calendar upon save."""
        edit_event_modal = EditEventModal(event_id=event_id, refresh_callback=self.refresh_calendar)
        edit_event_modal.open()
