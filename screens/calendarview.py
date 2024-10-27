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
class CalendarView(Screen):
    month_year_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        self.update_month_year_text()
        

    def on_kv_post(self, base_widget):
        # Populate the calendar after KV loading
        if 'calendar_grid' in self.ids:
            #Use Clock to delay the call to ensure everything is loaded.
            Clock.schedule_once(lambda dt: self.populate_calendar())
        else:
            print("Error: 'calendar_grid' not found in ids.")

    def update_month_year_text(self):
        #Updates the label showing the current month and year.
        self.month_year_text = datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def change_month(self, increment):
        #Changes the month and repopulates the calendar.
        self.current_month += increment
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_month_year_text()
        self.populate_calendar()

    def populate_calendar(self):
        #Generates the calendar grid.
        grid = self.ids['calendar_grid']
        grid.clear_widgets()
        #self.current_year= datetime.now().year
        #self.current_month= datetime.now().month 

        # Get days of the month and week
        cal = monthcalendar(self.current_year, self.current_month)

        # Add day numbers to the grid
        for week in cal:
            for day in week:
                if day == 0:
                    grid.add_widget(Label())  # Empty label for blank spaces
                else:
                    cell = RelativeLayout(size_hint=(1, None), height=dp(60))
                    
                    day_label = Label(
                        text=str(day),
                        size_hint=(None, None),
                        size=(dp(20), dp(20)),
                        pos_hint={'right': 1, 'top': 1},
                        color=(0, 0, 0, 1)  # Black text color
                    )
                    
                    day_button = Button(
                        background_normal="",
                        background_color=(0.9, 0.9, 0.9, 1),  # Light gray for day cell
                        on_press=self.on_day_press,
                        size_hint=(1, 1),
                        text=""  # Empty text so only the day label shows
                    )
                    cell.add_widget(day_button)
                    cell.add_widget(day_label)
                    grid.add_widget(cell)

    def on_day_press(self, instance):
        #Handles the event when a day is pressed.
        day_text = instance.parent.children[1].text
        print(f"You selected day: {day_text}")
