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

##################### Main App Class with ScreenManager #####################
class BusyBeeApp(App):
    """Main app class to manage screens and modals."""
    
    def build(self):
        # Load the UI components defined in the KV file
        Builder.load_file("busybee.kv")

        # Create a ScreenManager to manage the Calendar and To-Do List screens
        self.screen_manager = ScreenManager(transition=NoTransition())

        # Add the CalendarView and ToDoListView screens to the ScreenManager
        self.screen_manager.add_widget(CalendarView(name="calendar"))
        self.screen_manager.add_widget(ToDoListView(name="todo"))

        return self.screen_manager  # Return the screen manager as the main UI

    def switch_to_screen(self, screen_name):
        """Switch between Calendar and To-Do List screens."""
        self.root.current = screen_name

    def open_add_task_modal(self):
        """Open the Add Task modal."""
        AddTaskModal().open()

    def open_add_event_modal(self):
        """Open the Add Event modal."""
        AddEventModal().open()

######################### Calendar View Screen ##########################
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
            """Use Clock to delay the call to ensure everything is loaded."""
            Clock.schedule_once(lambda dt: self.populate_calendar())
        else:
            print("Error: 'calendar_grid' not found in ids.")

    def update_month_year_text(self):
        """Updates the label showing the current month and year."""
        self.month_year_text = datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def change_month(self, increment):
        """Changes the month and repopulates the calendar."""
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
        """Generates the calendar grid."""
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
        """Handles the event when a day is pressed."""
        day_text = instance.parent.children[1].text
        print(f"You selected day: {day_text}")


######################### To-Do List View Screen ##########################
class ToDoListView(Screen):
    """A screen for displaying the To-Do List."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Sorting state to remember the last sort
        self.sort_by = "priority"  # Default sort by priority

    def sort_tasks(self, criterion):
        """Sort the task list based on the chosen criterion (e.g., priority, due date)."""
        self.sort_by = criterion
        print(f"Tasks sorted by {criterion}")
        # Call a function here to sort the task list and refresh the view

    def add_task_item(self, title, due_date, priority_level, category):
        """Add a task item to the list (dummy function for now)."""
        print(f"Added task: {title}, Due: {due_date}, Priority: {priority_level}, Category: {category}")
        # Here you’d add logic to update the list view with the new task

######################### Add Event Modal ##########################
class AddEventModal(ModalView):
    """A modal for adding a new event."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the modal
        self.size_hint = (0.8, 0.5)  # Set the size of the modal
        self.auto_dismiss = False  # Prevent automatic dismissal when clicking outside

        # Create a layout for organizing widgets vertically
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for the event name
        self.event_name_input = TextInput(hint_text="Event Name", multiline=False)
        layout.add_widget(self.event_name_input)

        # Label to display the selected event date and time
        self.event_date_label = Label(text="Pick Event Date & Time")
        layout.add_widget(self.event_date_label)

        # Button to open the date picker
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        layout.add_widget(pick_date_button)

        # Action buttons to cancel or save the event
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_event))
        layout.add_widget(button_layout)

        # Add the layout to the modal
        self.add_widget(layout)

    def open_date_picker(self, instance):
        """Open the DatePicker popup."""
        DatePicker(self).open()

    def save_event(self, *args):
        """Save the event."""
        event_name = self.event_name_input.text.strip()
        event_date = self.event_date_label.text

        # Ensure the event has a name before saving
        if not event_name:
            print("Event Name is required.")
            return

        print(f"Event '{event_name}' scheduled for {event_date}")
        self.dismiss()  # Close the modal

######################### Add Task Modal ##########################
class AddTaskModal(ModalView):
    """A modal for adding a new task."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the modal
        self.size_hint = (0.9, 0.9)  # Set the size of the modal
        self.auto_dismiss = False  # Prevent automatic dismissal when clicking outside

        # Predefined categories and selected categories list
        self.categories = ["Work", "Personal", "School"]
        self.selected_categories = []

        # Create the main layout for the modal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for task title
        self.title_input = TextInput(hint_text="Task Title")
        layout.add_widget(self.title_input)

        # Deadline section with a label and date picker button
        deadline_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.deadline_label = Label(text="Pick a deadline", size_hint_x=0.8)
        deadline_layout.add_widget(self.deadline_label)
        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        deadline_layout.add_widget(pick_date_button)
        layout.add_widget(deadline_layout)

        # Button to open the Repeat Options modal
        self.repeat_button = Button(text="Does not repeat", on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        # Input field for notes
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner to select or add new categories
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

        # Layout to display selected categories
        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        # Action buttons to cancel or save the task
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        # Add the layout to the modal
        self.add_widget(layout)

    def open_date_picker(self, instance):
        """Open the DatePicker popup."""
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        """Open the Repeat Options modal."""
        RepeatOptionsModal(self).open()

    def on_category_selected(self, spinner, text):
        """Handle category selection."""
        if text == "Add New Category":
            CategoryModal(self).open()
        elif text not in self.selected_categories:
            self.selected_categories.append(text)
            self.update_applied_categories()

    def update_applied_categories(self):
        """Update the applied categories layout."""
        self.applied_categories_layout.clear_widgets()
        for category in self.selected_categories:
            label = Label(text=category)
            self.applied_categories_layout.add_widget(label)
    
    def update_category_spinner(self):
        """Update the spinner with the current list of categories."""
        self.category_spinner.values = self.categories + ["Add New Category"]

    def save_task(self, *args):
        """Save the task and add it to the To-Do List."""
        task_data = {
            "title": self.title_input.text,
            "deadline": self.deadline_label.text,
            "repeats": self.repeat_button.text,
            "notes": self.notes_input.text,
            "categories": self.selected_categories,
        }

        if not task_data["title"]:
            print("Task Title is required.")
            return

        # Find the ToDoListView screen in the ScreenManager and add the task
        todo_screen = self.app.screen_manager.get_screen('todo')
        todo_screen.add_task(task_data)

        print("Task Saved:", task_data)
        self.dismiss()  # Close the modal

##################################################################################################################################################################
#################### Usful Widgets and Modals (used by add Task and the Template for add Event) ##################################################################
##################################################################################################################################################################


####################### Custom Date Picker ###########################
class DatePicker(Popup):
    """A custom popup to select a date and time."""

    def __init__(self, modal, **kwargs):
        super().__init__(**kwargs)
        self.modal = modal  # Reference to the task or event modal
        self.title = "Select a Date"  # Title of the popup
        self.size_hint = (0.8, 0.8)  # Size of the popup
        self.selected_button = None  # Track the selected date button

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Grid layout for the days of the month
        grid = GridLayout(cols=7, spacing=5, padding=10)
        days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # Add day headers to the grid
        for day in days_of_week:
            grid.add_widget(Label(text=day))

        today = datetime.today()  # Get today's date
        first_day = today.replace(day=1)  # First day of the month
        start_day = first_day.weekday()  # Which day of the week the month starts on

        # Add empty widgets to align the first day correctly
        for _ in range(start_day + 1):
            grid.add_widget(Label(text=""))

        # Create buttons for each day in the month
        days_in_month = (first_day + timedelta(days=32)).replace(day=1) - first_day
        for day in range(1, days_in_month.days + 1):
            button = Button(text=str(day), on_release=self.select_date)
            button.background_color = (1, 1, 1, 1)  # Default white background
            grid.add_widget(button)

        layout.add_widget(grid)  # Add the grid to the layout

        # Add time selection using spinners
        time_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.hour_spinner = Spinner(text="00", values=[f"{i:02d}" for i in range(24)])
        self.minute_spinner = Spinner(text="00", values=[f"{i:02d}" for i in range(60)])
        time_layout.add_widget(Label(text="Hour:"))
        time_layout.add_widget(self.hour_spinner)
        time_layout.add_widget(Label(text="Minute:"))
        time_layout.add_widget(self.minute_spinner)

        layout.add_widget(time_layout)  # Add the time selection layout

        # Action buttons for the popup
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="OK", on_release=self.confirm_selection))
        layout.add_widget(button_layout)

        self.add_widget(layout)  # Add the main layout to the popup

    def select_date(self, button):
        """Highlight the selected date and store the selection."""
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)  # Reset previous selection to white

        button.background_color = (0, 0.5, 1, 1)  # Highlight selected date
        self.selected_button = button
        self.selected_date = datetime.today().replace(day=int(button.text)).strftime("%Y-%m-%d")

    def confirm_selection(self, instance):
        """Update the appropriate modal with the selected date and time."""
        hour = self.hour_spinner.text
        minute = self.minute_spinner.text
        selected_datetime = f"{self.selected_date} {hour}:{minute}"

        # Check which modal is calling and update the correct label
        if hasattr(self.modal, 'deadline_label'):
            self.modal.deadline_label.text = f"Deadline: {selected_datetime}"
        elif hasattr(self.modal, 'event_date_label'):
            self.modal.event_date_label.text = f"Event Date: {selected_datetime}"
        else:
            print("Error: No valid label to update.")

        self.dismiss()  # Close the popup

####################### Repeat Options Modal ###########################
class RepeatOptionsModal(ModalView):
    """A modal with repeat options: Does not repeat, Daily, Weekly, Monthly."""
    
    def __init__(self, task_modal, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.4)  # Set the size of the modal
        self.auto_dismiss = False  # Prevent automatic dismissal
        self.task_modal = task_modal  # Reference to the task modal

        # Create the main layout for the repeat options
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add buttons for each repeat option
        options = ["Does not repeat", "Daily repeat", "Weekly repeat", "Monthly repeat"]
        for option in options:
            button = Button(text=option, size_hint_y=None, height=50)
            button.bind(on_release=self.set_repeat_option)
            layout.add_widget(button)

        # Add a cancel button to dismiss the modal
        cancel_button = Button(text="CANCEL", size_hint_y=None, height=50, on_release=self.dismiss)
        layout.add_widget(cancel_button)

        self.add_widget(layout)  # Add the layout to the modal

    def set_repeat_option(self, instance):
        """Set the selected repeat option and update the task modal."""
        self.task_modal.repeat_button.text = instance.text  # Update the repeat button text
        self.dismiss()  # Close the modal

####################### Category Modals ###########################
class CategoryModal(ModalView):
    """A modal for adding a new category."""
    
    def __init__(self, task_modal, **kwargs):
        super().__init__(**kwargs)
        self.task_modal = task_modal  # Reference to the task modal
        self.size_hint = (0.8, 0.4)  # Set the size of the modal

        # Create the main layout for the modal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.new_category_input = TextInput(hint_text="Enter new category")
        layout.add_widget(self.new_category_input)

        # Add buttons to cancel or save the new category
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_category))
        layout.add_widget(button_layout)

        self.add_widget(layout)  # Add the layout to the modal

    def save_category(self, *args):
        """Save the new category if it's not a duplicate."""
        new_category = self.new_category_input.text.strip()
        if new_category and new_category not in self.task_modal.categories:
            self.task_modal.categories.append(new_category)
            self.task_modal.update_category_spinner()
            CategoryConfirmationModal(new_category).open()
        else:
            DuplicateCategoryModal().open()
        self.dismiss()

class DuplicateCategoryModal(ModalView):
    """A modal to notify the user of duplicate categories."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.3)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="This category already exists."))
        layout.add_widget(Button(text="OK", on_release=self.dismiss))
        self.add_widget(layout)

class CategoryConfirmationModal(ModalView):
    """A modal to confirm the addition of a new category."""
    
    def __init__(self, category_name, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.3)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=f"Category '{category_name}' added successfully!"))
        layout.add_widget(Button(text="OK", on_release=self.dismiss))
        self.add_widget(layout)

########################### Run the App ###########################
if __name__ == "__main__":
    BusyBeeApp().run()
