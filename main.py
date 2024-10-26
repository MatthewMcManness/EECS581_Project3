"""
Authors: Matthew McManness [2210261], Manvir Kaur [3064194], Magaly Camacho [3072618], Mariam Oraby [3127776], Shravya Matta [3154808]
Date Created: 10/26/2024
Last Updated: 10/26/2024

Program Title: BusyBee
Program Description: 
    The app will feature a modern and clean design, similar to popular productivity apps, with a bottom navigation bar to easily switch between the calendar 
and to-do list views. The Calendar section will display a grid for the current month, allowing users to view and interact with each day, while the To-Do List section will
 provide a scrollable list of tasks with the ability to add, check, and remove tasks. The user interface is built with KivyMD's material design components, providing a sleek 
 and responsive look that fits perfectly on mobile devices.

	Utilizing Kivy and KivyMD ensures cross-platform compatibility and a professional, mobile-optimized experience. Kivy’s layout flexibility makes it ideal for creating responsive
designs that adapt to different screen sizes, while KivyMD’s material design elements provide a polished and user-friendly interface. The bottom navigation bar and scrollable 
layouts for both calendar and to-do list views will offer an intuitive experience for users. This approach allows for easy expansion with future features, such as adding events
 or task notifications, ensuring the app is scalable and future-ready.

Sources: YouTube, ChatGPT
Inputs: User mouse/key inputs
Output: App Window

"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.app import App
from datetime import datetime, timedelta

# Calendar View Screen
class CalendarView(Screen):
    pass

# To-Do List View Screen
class ToDoListView(Screen):
    pass

# Main App with ScreenManager
class BusyBeeApp(App):
    def build(self):
        Builder.load_file("busybee.kv")
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(CalendarView(name="calendar"))
        self.screen_manager.add_widget(ToDoListView(name="todo"))
        return self.screen_manager

    def switch_to_screen(self, screen_name):
        self.root.current = screen_name

    def open_add_task_modal(self):
        AddTaskModal().open()

    def open_add_event_modal(self):
        AddEventModal().open()

# Modal for Adding a New Event
class AddEventModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.5)
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.event_name_input = TextInput(hint_text="Event Name", multiline=False)
        layout.add_widget(self.event_name_input)

        self.event_date_label = Label(text="Pick Event Date & Time")
        layout.add_widget(self.event_date_label)

        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        layout.add_widget(pick_date_button)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_event))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def open_date_picker(self, instance):
        DatePicker(self).open()

    def save_event(self, *args):
        event_name = self.event_name_input.text.strip()
        event_date = self.event_date_label.text

        if not event_name:
            print("Event Name is required.")
            return

        print(f"Event '{event_name}' scheduled for {event_date}")
        self.dismiss()


# Custom Date Picker with Time Selection
class DatePicker(Popup):
    def __init__(self, modal, **kwargs):
        super().__init__(**kwargs)
        self.modal = modal
        self.title = "Select a Date"
        self.size_hint = (0.8, 0.8)
        self.selected_button = None  # Track the currently selected button

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Grid for days of the month
        grid = GridLayout(cols=7, spacing=5, padding=10)
        days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for day in days_of_week:
            grid.add_widget(Label(text=day))

        today = datetime.today()
        first_day = today.replace(day=1)
        start_day = first_day.weekday()

        for _ in range(start_day + 1):
            grid.add_widget(Label(text=""))

        # Create buttons for days and set up click logic with highlighting
        days_in_month = (first_day + timedelta(days=32)).replace(day=1) - first_day
        for day in range(1, days_in_month.days + 1):
            button = Button(text=str(day), on_release=self.select_date)
            button.background_color = (1, 1, 1, 1)  # Default white background
            grid.add_widget(button)

        layout.add_widget(grid)

        # Time selection
        time_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.hour_spinner = Spinner(text="00", values=[f"{i:02d}" for i in range(24)])
        self.minute_spinner = Spinner(text="00", values=[f"{i:02d}" for i in range(60)])
        time_layout.add_widget(Label(text="Hour:"))
        time_layout.add_widget(self.hour_spinner)
        time_layout.add_widget(Label(text="Minute:"))
        time_layout.add_widget(self.minute_spinner)

        layout.add_widget(time_layout)

        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="OK", on_release=self.confirm_selection))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def select_date(self, button):
        """Highlight the selected date button and store the selection."""
        # Reset the previous button color if one was selected
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)  # White background

        # Highlight the new selected button
        button.background_color = (0, 0.5, 1, 1)  # Light blue background
        self.selected_button = button

        # Store the selected date
        self.selected_date = datetime.today().replace(day=int(button.text)).strftime("%Y-%m-%d")

    def confirm_selection(self, instance):
        """Update the modal with the selected date and time."""
        hour = self.hour_spinner.text
        minute = self.minute_spinner.text
        selected_datetime = f"{self.selected_date} {hour}:{minute}"
        self.modal.deadline_label.text = f"Deadline: {selected_datetime}"
        self.dismiss()

class RepeatOptionsModal(ModalView):
    """A modal with repeat options: Does not repeat, Daily, Weekly, Monthly."""
    def __init__(self, task_modal, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.4)
        self.auto_dismiss = False
        self.task_modal = task_modal

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Repeat options
        options = ["Does not repeat", "Daily repeat", "Weekly repeat", "Monthly repeat"]
        for option in options:
            button = Button(text=option, size_hint_y=None, height=50)
            button.bind(on_release=self.set_repeat_option)
            layout.add_widget(button)

        # Cancel button
        cancel_button = Button(text="CANCEL", size_hint_y=None, height=50, on_release=self.dismiss)
        layout.add_widget(cancel_button)

        self.add_widget(layout)

    def set_repeat_option(self, instance):
        """Set the selected repeat option and update the task modal."""
        self.task_modal.repeat_button.text = instance.text  # Update the task modal button text
        self.dismiss()

# Category Modals
class CategoryModal(ModalView):
    def __init__(self, task_modal, **kwargs):
        super().__init__(**kwargs)
        self.task_modal = task_modal
        self.size_hint = (0.8, 0.4)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.new_category_input = TextInput(hint_text="Enter new category")
        layout.add_widget(self.new_category_input)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_category))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def save_category(self, *args):
        new_category = self.new_category_input.text.strip()
        if new_category and new_category not in self.task_modal.categories:
            self.task_modal.categories.append(new_category)
            self.task_modal.category_spinner.values = self.task_modal.categories + ["Add New Category"]
            CategoryConfirmationModal(new_category).open()
        else:
            DuplicateCategoryModal().open()
        self.dismiss()

class DuplicateCategoryModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.3)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="This category already exists."))
        layout.add_widget(Button(text="OK", on_release=self.dismiss))
        self.add_widget(layout)

class CategoryConfirmationModal(ModalView):
    def __init__(self, category_name, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.3)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=f"Category '{category_name}' added successfully!"))
        layout.add_widget(Button(text="OK", on_release=self.dismiss))
        self.add_widget(layout)
# Modal for Adding a New Task
class AddTaskModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False

        self.categories = ["Work", "Personal", "School"]
        self.selected_categories = []

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_input = TextInput(hint_text="Task Title")
        layout.add_widget(self.title_input)

        # Deadline section
        deadline_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.deadline_label = Label(text="Pick a deadline", size_hint_x=0.8)
        deadline_layout.add_widget(self.deadline_label)

        pick_date_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        deadline_layout.add_widget(pick_date_button)
        layout.add_widget(deadline_layout)

        # Repeat button (opens RepeatOptionsModal)
        self.repeat_button = Button(text="Does not repeat", on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        # Notes input
        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

        # Category spinner
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

        # Applied categories layout
        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def open_date_picker(self, instance):
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        """Open the Repeat Options modal."""
        RepeatOptionsModal(self).open()

    def on_category_selected(self, spinner, text):
        if text == "Add New Category":
            self.open_category_modal()
        elif text not in self.selected_categories:
            self.selected_categories.append(text)
            self.update_applied_categories()

    def open_category_modal(self):
        CategoryModal(self).open()

    def update_category_spinner(self):
        self.category_spinner.values = self.categories + ["Add New Category"]

    def update_applied_categories(self):
        self.applied_categories_layout.clear_widgets()
        for category in self.selected_categories:
            label = Label(text=category)
            self.applied_categories_layout.add_widget(label)

    def save_task(self, *args):
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

        print("Task Saved:", task_data)
        self.dismiss()


if __name__ == "__main__":
    BusyBeeApp().run()
