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
from kivy.properties import StringProperty  # Property to update UI reactively.
from kivy.app import App  # Main class to run the Kivy app.
from kivy.clock import Clock  # Schedule functions after a delay.
from calendar import monthcalendar  # Generate calendar layout for a given month.
from datetime import datetime, timedelta  # Work with dates and times.
from database import get_database # to connect to database
from sqlalchemy import select, extract # to query database
from Models import Event_ # task model class

db = get_database() # get database
        

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
                    cell = RelativeLayout(size_hint=(1, None), height=dp(60))

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
                    cell.add_widget(day_button)
                    cell.add_widget(day_label)

                    # Add the cell to the calendar grid.
                    grid.add_widget(cell)

    def on_day_press(self, instance):
        """Handle the event when a day button is pressed."""
        day_text = instance.parent.children[1].text  # Get the selected day number.
        print(f"You selected day: {day_text}")  # Print the selected day to the console.

    def add_event(self, event_id, name, place = None):
        """Add a new event to the calendar"""
        # Create an EventBox and pass on_event_click as the click callback
        event_box = EventBox(on_click_callback = self.on_event_click, padding = "5dp", spacing = "5dp", size_hint_y = None, height = "60dp", size_hint_x = 1)
        event_box.event_id = event_id
        
        # Add widgets to display event info
        event_box.add_widget(Label(text = name, size_hint_x=0.5, color=(0,0,0,1)))
        event_box.add_widget(Label(text = start_time, size_hint_x=0.3, color=(0,0,0,1)))

        print(f"Added evnet: {event_id}")  # Log the event addition

    
    def get_cell_widget(self, date_str):
        """Retrieve the widget for the specified date."""
        # Parse the date string into a datetime object
        target_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        target_day = target_date.day
        target_month = target_date.month
        target_year = target_date.year

        # Check if the date is in the current calendar view
        if target_month != self.current_month or target_year != self.current_year:
            print("Error: The specified date is not in the current month or year.")
            return None

        # Get the calendar layout for the current month
        cal = monthcalendar(self.current_year, self.current_month)

        (comment)# Locate the widget for the target day in calendar_grid
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
        with db.session() as session:
            stmt = select(Event_).where(
                extract("year",Event_.start_time)== self.current_year,
                extract("month", Event_.start_time) == self.current_month)
            events = session.scalars(stmt).all()

            for event in events:
                start_time = event.start_time.strftime("%Y-%m-%d %H:%M")
                cell_widget = self.get_cell_widget(start_time)
                
                #add event 
                self.add_event(event.id, event.name, event.place, event.start_time)
                
            
        


