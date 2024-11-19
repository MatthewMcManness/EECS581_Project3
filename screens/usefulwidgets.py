# -----------------------------------------------------------------------------
# Name: widgets_and_modals.py
# Description: This module contains custom UI components such as the DatePicker, 
#              TimePicker, RepeatOptionsModal, and category-related modals used 
#              throughout the BusyBee application.
# Programmer: Matthew McManness (2210261), Magaly Camacho (3072618)
# Date Created: October 26, 2024
# Revision History:
# - October 26, 2024: Initial version created (Author: Matthew McManness)
# - October 27, 2024: Updated the datepicker to match calendar and added proper comments. (Matthew McManness)
# - November 4, 2024: Made it so that the CategoryModal pulls from and updates to the database (Magaly Camacho)
# - November 10, 2024: updated the calendar view so that the week starts on a Sunday - Matthew McManness
# - November 10, 2024: Added PriorityOptionsModal (Magaly Camacho)
# - November 18, 2024: Updated RepeatOptionsModal to include how many times to repeat, made it so it pulls info from task modal (Magaly Camacho)
#
# Preconditions:
# - Kivy framework must be installed and functional.
# - All modals and UI components rely on the Kivy App class and are part of a 
#   larger app structure.
#
# Postconditions:
# - The UI components will display modals to handle date, time, and category 
#   selections within the app.
#
# Known Faults:
# - Can't add two categories in a row, must select in between.
# Side Effects:
# - The modals modify the underlying app's properties (e.g., category lists, 
#   selected dates) when used.
# -----------------------------------------------------------------------------

# Import necessary modules from Kivy and Python standard libraries
from kivy.lang import Builder  # Load .kv files for UI definitions
from kivy.uix.boxlayout import BoxLayout  # Organize widgets horizontally or vertically
from kivy.uix.modalview import ModalView  # Pop-up windows (modals)
from kivy.uix.label import Label  # Display text in the UI
from kivy.uix.gridlayout import GridLayout  # Arrange widgets in a grid
from kivy.uix.button import Button  # Standard button widget
from kivy.uix.spinner import Spinner  # Dropdown-style component for selections
from kivy.uix.textinput import TextInput  # Input field for user text
from calendar import monthcalendar  # Generate a month’s calendar layout
from datetime import datetime  # Date and time utilities
from Models import Category # Category model
from Models.databaseEnums import Priority, Frequency # priorities for tasks, frequency for recurrence
from database import get_database # class to interact with database
import calendar  # Import calendar for setting first day of the week

# Set the first day of the week to Sunday
calendar.setfirstweekday(calendar.SUNDAY)

db = get_database() # get database

####################### Custom Date Picker ###########################
class DatePicker(ModalView):
    """A custom modal for selecting a date."""

    def __init__(self, modal, **kwargs):
        """
        Initializes the DatePicker modal.

        Args:
            modal (ModalView): The parent task or event modal.
            **kwargs: Additional keyword arguments passed to the superclass.

        Preconditions:
            - The calling code must provide a valid parent modal.

        Postconditions:
            - A DatePicker modal with navigation, day selection, and cancel/select buttons.
        """
        super().__init__(**kwargs)
        self.modal = modal  # Store reference to the parent modal
        self.size_hint = (0.9, 0.9)  # Define modal size
        self.auto_dismiss = False  # Disable dismissal when clicking outside

        self.selected_button = None  # No button selected initially

        # Layout for the modal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)

        # Set initial year and month to current
        self.current_year = datetime.today().year
        self.current_month = datetime.today().month

        # Create label showing the current month and year
        self.month_year_label = Label(
            text=self.get_month_year_text(),
            font_size='20sp',
            size_hint_y=None,
            height=40
        )

        # Header layout for month navigation
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        header_layout.add_widget(Button(text="<", on_release=lambda _: self.change_month(-1)))
        header_layout.add_widget(self.month_year_label)
        header_layout.add_widget(Button(text=">", on_release=lambda _: self.change_month(1)))
        layout.add_widget(header_layout)

        # Grid layout for calendar days
        self.grid = GridLayout(cols=7, spacing=2, padding=5, size_hint_y=0.8)
        layout.add_widget(self.grid)

        # Footer buttons for Cancel and Select
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SELECT", on_release=self.on_select))
        layout.add_widget(button_layout)

        self.add_widget(layout)  # Add layout to modal
        self.populate_calendar()  # Populate the calendar with current month

    def get_month_year_text(self):
        """Returns the current month and year as a formatted string."""
        return datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def change_month(self, increment):
        """
        Changes the displayed month by the given increment.

        Args:
            increment (int): Positive or negative value to change the month.

        Postconditions:
            - The displayed month and year are updated.
        """
        self.current_month += increment
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        self.month_year_label.text = self.get_month_year_text()
        self.populate_calendar()  # Refresh calendar

    def populate_calendar(self):
        """
        Populates the calendar grid with buttons representing days of the month.

        Postconditions:
            - Calendar grid reflects the days of the selected month.
        """
        self.grid.clear_widgets()  # Remove old widgets

        # Calculate number of weeks in the current month
        cal = monthcalendar(self.current_year, self.current_month)
        num_weeks = len(cal)

        # Define row height
        total_rows = num_weeks + 1  # +1 for header row
        row_height = 1 / total_rows

        # Add headers for days of the week
        days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days_of_week:
            self.grid.add_widget(Label(text=day, size_hint_y=row_height))

        # Add buttons for each day of the month
        for week in cal:
            for day in week:
                if day == 0:
                    self.grid.add_widget(Label(size_hint_y=row_height))  # Empty space
                else:
                    button = Button(
                        text=str(day),
                        size_hint_y=row_height,
                        background_color=(1, 1, 1, 1)  # White background
                    )
                    button.bind(on_release=lambda btn=button: self.select_date(btn))
                    self.grid.add_widget(button)

    def select_date(self, button):
        """
        Stores the selected date.

        Args:
            button (Button): The button representing the selected day.

        Postconditions:
            - The selected date is stored and highlighted.
        """
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)  # Reset color

        button.background_color = (0, 0.5, 1, 1)  # Highlight selected day
        self.selected_button = button
        self.selected_date = datetime(
            self.current_year, self.current_month, int(button.text)
        ).strftime("%Y-%m-%d")

    def on_select(self, instance):
        """
        Opens the TimePicker when the Select button is clicked.

        Preconditions:
            - A date must be selected.
        """
        if not hasattr(self, 'selected_date'):
            print("Please select a date first.")
            return

        TimePicker(self).open()  # Open the TimePicker

####################### Custom Time Picker ###########################
class TimePicker(ModalView):
    """A custom time picker mimicking Material Design style."""

    def __init__(self, date_picker, **kwargs):
        """
        Initializes the TimePicker.

        Args:
            date_picker (DatePicker): Reference to the DatePicker instance.

        Preconditions:
            - The calling code must provide a valid DatePicker reference.
        """
        super().__init__(**kwargs)
        self.date_picker = date_picker  # Store reference
        self.size_hint = (0.8, 0.5)
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Add spinners for hours and minutes
        time_layout = BoxLayout(orientation='horizontal', spacing=30)
        self.hour_spinner = Spinner(text="00", values=[f"{i:02d}" for i in range(24)])
        self.minute_spinner = Spinner(text="00", values=[f"{i:02d}" for i in range(60)])
        time_layout.add_widget(self.hour_spinner)
        time_layout.add_widget(self.minute_spinner)
        layout.add_widget(time_layout)

        # Add Cancel and OK buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=20)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="OK", on_release=self.confirm_selection))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def confirm_selection(self, instance):
        """
        Confirms the selected time and updates the parent modal.

        Postconditions:
            - The selected time is saved and displayed in the parent modal.
        """
        hour = self.hour_spinner.text
        minute = self.minute_spinner.text
        selected_datetime = f"{self.date_picker.selected_date} {hour}:{minute}"

        if hasattr(self.date_picker.modal, 'deadline_label'):
            self.date_picker.modal.deadline_label.text = f"Deadline: {selected_datetime}"
        elif hasattr(self.date_picker.modal, 'event_date_label'):
            self.date_picker.modal.event_date_label.text = f"Event Date: {selected_datetime}"
        else:
            print("Error: No valid label to update.")

        self.dismiss()  # Close the TimePicker
        self.date_picker.dismiss()  # Close the DatePicker

####################### Repeat Options Modal ###########################
class RepeatOptionsModal(ModalView):
    """A modal that provides options for repeating tasks: Does not repeat, Daily, Weekly, Monthly, Yearly."""

    def __init__(self, task_modal, **kwargs):
        """
        Initializes the RepeatOptionsModal.

        Args:
            task_modal (ModalView): The parent task modal to update repeat information.
            **kwargs: Additional keyword arguments passed to the superclass.

        Preconditions:
            - A valid task_modal must be provided.

        Postconditions:
            - A modal with buttons to select repeat options is displayed.
        """
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.4)  # Set modal size
        self.auto_dismiss = False  # Prevent accidental dismissal
        self.task_modal = task_modal  # Store reference to the task modal

        # Create the main layout for repeat options
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add buttons for each repeat option
        options = Frequency.frequency_options()
        for option in options:
            button = Button(text=option, size_hint_y=None, height=50)
            button.bind(on_release=self.set_repeat_frequency)  # Bind selection to handler
            layout.add_widget(button)

        # Get existing inputs
        old_input = self.task_modal.repeat_button.text.split(" ")
        old_frequency = (" ").join(old_input[0:2]) if len(old_input) == 2 else old_input[0]
        old_times = "#" if len(old_input) == 2 else old_input[1].split(" ")[0].replace("(", "")

        # Input for how many times to repeat
        self.repeats_layout = BoxLayout(orientation='horizontal', spacing=10)
        repeats_label_1 = Label(text="Repeats:")
        self.repeats_frequency = Label(text=old_frequency)
        self.repeat_times = TextInput(hint_text=old_times, multiline=False)
        repeats_label_2 = Label(text="times")
        for widget in [repeats_label_1, self.repeats_frequency, self.repeat_times, repeats_label_2]:
            self.repeats_layout.add_widget(widget)
        layout.add_widget(self.repeats_layout)

        # Add a cancel button to dismiss the modal
        cancel_button = Button(text="CANCEL", size_hint_y=None, height=50, on_release=self.dismiss)

        # Add save button
        save_button = Button(text="SAVE", size_hint_y=None, height=50, on_release=self.save)

        # save and cancel layout
        save_cancel_layout = BoxLayout(orientation='horizontal', spacing=10)
        save_cancel_layout.add_widget(cancel_button)
        save_cancel_layout.add_widget(save_button)
        layout.add_widget(save_cancel_layout)

        # Add the layout to the modal
        self.add_widget(layout) 

    def set_repeat_frequency(self, instance):
        """
        Sets the selected repeat option and updates the task modal.

        Args:
            instance (Button): The button representing the selected repeat option.

        Postconditions:
            - The repeat button in the task modal reflects the selected option.
        """
        self.repeats_frequency.text = instance.text # update label in repeat options modal
        
    def save(self, instance):
        """Saves repeats option and dismisses modal"""
        repeat_option_str = self.repeats_frequency.text
        repeat_option = Frequency.str2enum(repeat_option_str)
        repeat_times = self.repeat_times.text.strip()

        # if it doesn't repeat or nothing was chosen, close modal
        if Frequency.is_no_repeat(repeat_option):
            self.task_modal.repeat_button.text = repeat_option_str  # Update the repeat option in the parent modal
            self.dismiss()  # Close the modal

        # save # of times to repeat, then close model
        elif repeat_times.isnumeric():
            self.task_modal.repeat_button.text = f"{repeat_option_str} ({repeat_times} times)"
            self.dismiss()

        
####################### Priority Options Modal ###########################
class PriorityOptionsModal(ModalView):
    """A modal that provides options for task priority: Low, Medium, High."""

    def __init__(self, task_modal, **kwargs):
        """
        Initializes the PriorityOptionsModal.

        Args:
            task_modal (ModalView): The parent task modal to update priority information.
            **kwargs: Additional keyword arguments passed to the superclass.
        """
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.4)  # Set modal size
        self.auto_dismiss = False  # Prevent accidental dismissal
        self.task_modal = task_modal  # Store reference to the task modal

        # Create the main layout for priority options
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add buttons for each priority option
        options = Priority.priority_options() + ["Clear"]
        for option in options:
            button = Button(text=option, size_hint_y=None, height=50)
            button.bind(on_release=self.set_priority_option)  # Bind selection to handler
            layout.add_widget(button)

        # Add a cancel button to dismiss the modal
        cancel_button = Button(text="CANCEL", size_hint_y=None, height=50, on_release=self.dismiss)
        layout.add_widget(cancel_button)

        self.add_widget(layout)  # Add the layout to the modal

    def set_priority_option(self, instance):
        """
        Sets the selected priority option and updates the task modal.

        Args:
            instance (Button): The button representing the selected priority option.
        """
        if instance.text == "Clear":
            self.task_modal.priority_button.text = "Pick Priority" # Clear the priority
        else:
            self.task_modal.priority_button.text = instance.text  # Update the priority option in the parent modal
        self.dismiss()  # Close the modal

####################### Category Modals ###########################
class CategoryModal(ModalView):
    """A modal for adding a new category to tasks."""

    def __init__(self, task_modal, **kwargs):
        """
        Initializes the CategoryModal.

        Args:
            task_modal (ModalView): The parent task modal to update categories.
            **kwargs: Additional keyword arguments passed to the superclass.

        Preconditions:
            - A valid task_modal must be provided.

        Postconditions:
            - A modal to input new categories is displayed.
        """
        super().__init__(**kwargs)
        self.task_modal = task_modal  # Store reference to the task modal
        self.size_hint = (0.8, 0.4)  # Set modal size

        # Create the main layout for the modal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for new category
        self.new_category_input = TextInput(hint_text="Enter new category")
        layout.add_widget(self.new_category_input)

        # Action buttons to cancel or save the category
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_category))
        layout.add_widget(button_layout)

        self.add_widget(layout)  # Add the layout to the modal

    def save_category(self, *args):
        """
        Saves the new category if it is not a duplicate.

        Postconditions:
            - The category is added to the task modal's list, or an error is displayed.
        """
        new_category = self.new_category_input.text.strip()  # Get input text

        if new_category and new_category not in self.task_modal.categories:
            self.task_modal.categories.append(new_category)  # Add category
            self.task_modal.update_category_spinner()  # Update spinner options

            category_object = Category(name=new_category) # make a category object

            # save new category
            with db.get_session() as session: # connect to database with a session
                with session.begin(): # start transaction (auto commits)
                    session.add(category_object) # insert new category
                
                category_id = category_object.id # get generated id
                self.task_modal.categories_ids.append(category_id) # cache id
                
            CategoryConfirmationModal(new_category).open()  # Open confirmation modal
        else:
            DuplicateCategoryModal().open()  # Open duplicate error modal

        self.dismiss()  # Close the modal

class DuplicateCategoryModal(ModalView):
    """A modal to notify the user if a duplicate category is detected."""

    def __init__(self, **kwargs):
        """
        Initializes the DuplicateCategoryModal.

        Postconditions:
            - A notification modal is displayed to indicate duplicate categories.
        """
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.3)  # Set modal size

        # Create the layout with error message and OK button
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="This category already exists."))
        layout.add_widget(Button(text="OK", on_release=self.dismiss))

        self.add_widget(layout)  # Add layout to modal

class CategoryConfirmationModal(ModalView):
    """A modal to confirm the addition of a new category."""

    def __init__(self, category_name, **kwargs):
        """
        Initializes the CategoryConfirmationModal.

        Args:
            category_name (str): The name of the added category.

        Postconditions:
            - A confirmation message is displayed indicating the successful addition.
        """
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.3)  # Set modal size

        # Create layout with confirmation message and OK button
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=f"Category '{category_name}' added successfully!"))
        layout.add_widget(Button(text="OK", on_release=self.dismiss))

        self.add_widget(layout)  # Add layout to modal
