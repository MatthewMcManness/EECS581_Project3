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
class BusyBeeApp(App):  # Inherit from App
    def build(self):
        Builder.load_file("busybee.kv")
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(CalendarView(name="calendar"))
        self.screen_manager.add_widget(ToDoListView(name="todo"))
        return self.screen_manager

    def switch_to_screen(self, screen_name):
        """Switch between Calendar and To-Do List screens."""
        self.root.current = screen_name

    def open_add_task_modal(self):
        """Opens the Add Task modal."""
        AddTaskModal().open()

# Custom Time Picker Popup
class TimePicker(Popup):
    def __init__(self, task_modal, **kwargs):
        super().__init__(**kwargs)
        self.task_modal = task_modal
        self.title = "Select Time"
        self.size_hint = (0.8, 0.8)

        # Main layout for the time picker
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Hour and Minute pickers
        time_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.hour_input = Spinner(text="00", values=[f"{i:02d}" for i in range(24)])
        self.minute_input = Spinner(text="00", values=[f"{i:02d}" for i in range(60)])
        time_layout.add_widget(Label(text="Hour:"))
        time_layout.add_widget(self.hour_input)
        time_layout.add_widget(Label(text="Minute:"))
        time_layout.add_widget(self.minute_input)
        layout.add_widget(time_layout)

        # Action Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="OK", on_release=self.confirm_time))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def confirm_time(self, instance):
        """Handles the selected time."""
        hour = self.hour_input.text
        minute = self.minute_input.text
        self.task_modal.deadline_label.text += f" {hour}:{minute}"
        self.dismiss()

# Custom Date Picker Popup
class DatePicker(Popup):
    def __init__(self, task_modal, **kwargs):
        super().__init__(**kwargs)
        self.task_modal = task_modal
        self.title = "Select a Date"
        self.size_hint = (0.8, 0.8)

        # Layout to display days
        layout = GridLayout(cols=7, spacing=5, padding=10)

        # Add labels for days of the week
        days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days_of_week:
            layout.add_widget(Label(text=day, halign="center"))

        # Generate the current month's days
        today = datetime.today()
        first_day = today.replace(day=1)
        start_day = first_day.weekday()

        # Add empty slots for days before the first day of the month
        for _ in range(start_day + 1):
            layout.add_widget(Label(text=""))

        # Add buttons for each day of the month
        days_in_month = (first_day + timedelta(days=32)).replace(day=1) - first_day
        for day in range(1, days_in_month.days + 1):
            button = Button(text=str(day), on_release=self.select_date)
            layout.add_widget(button)

        self.add_widget(layout)

    def select_date(self, button):
        """Handle date selection and open the time picker."""
        today = datetime.today()
        selected_date = today.replace(day=int(button.text)).strftime("%Y-%m-%d")
        self.task_modal.deadline_label.text = f"Deadline: {selected_date}"
        self.dismiss()

        # Open the Time Picker after selecting the date
        TimePicker(self.task_modal).open()

# Modal for Adding a New Task
class AddTaskModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False

        self.categories = ["Work", "Personal", "School"]
        self.selected_categories = []

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_input = TextInput(hint_text="Title")
        layout.add_widget(self.title_input)

        deadline_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.deadline_label = Label(text="Pick a deadline", halign="left", size_hint_x=0.8)
        deadline_layout.add_widget(self.deadline_label)

        deadline_button = Button(text="Pick Date & Time", on_release=self.open_date_picker)
        deadline_layout.add_widget(deadline_button)
        layout.add_widget(deadline_layout)

        self.repeat_button = Button(text="Does not repeat", on_release=self.open_repeat_window)
        layout.add_widget(self.repeat_button)

        self.notes_input = TextInput(hint_text="Notes", multiline=True)
        layout.add_widget(self.notes_input)

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

        self.applied_categories_layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(self.applied_categories_layout)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="CANCEL", on_release=self.dismiss))
        button_layout.add_widget(Button(text="SAVE", on_release=self.save_task))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def open_date_picker(self, instance):
        """Opens the custom DatePicker popup."""
        DatePicker(self).open()

    def open_repeat_window(self, instance):
        print("Open Repeat Window")

    def on_category_selected(self, spinner, text):
        if text == "Add New Category":
            self.open_category_modal()
        elif text not in self.selected_categories:
            self.selected_categories.append(text)
            self.update_applied_categories()

    def open_category_modal(self):
        CategoryModal(self).open()

    def update_applied_categories(self):
        self.applied_categories_layout.clear_widgets()
        for category in self.selected_categories:
            label = Label(text=category, halign="center")
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
