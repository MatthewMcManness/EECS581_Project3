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

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Main Calendar View Screen
class CalendarView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_calendar_screen()

    def build_calendar_screen(self):
        """Initializes the calendar screen layout."""
        pass

    def on_day_button_press(self, day: int):
        """Handles user interaction with a day button.

        Args:
            day (int): Selected day number.
        """
        pass

    def open_add_event_window(self):
        """Opens the Add Event window."""
        pass

# Main To-Do List View Screen
class ToDoListView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_todo_list_screen()

    def build_todo_list_screen(self):
        """Initializes the to-do list screen layout."""
        pass

    def open_add_task_window(self):
        """Opens the Add Task window."""
        pass

    def toggle_task_completion(self, task_id: int):
        """Marks a task as complete or incomplete.

        Args:
            task_id (int): Identifier for the task.
        """
        pass

# Modal for Adding a New Task
class AddTaskWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.build_add_task_dialog()

    def build_add_task_dialog(self):
        """Creates the Add Task dialog window."""
        pass

    def save_task(self, task_name: str, due_date: str):
        """Saves the new task.

        Args:
            task_name (str): Name of the task.
            due_date (str): Due date of the task.
        """
        pass

# Modal for Adding a New Event
class AddEventWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.build_add_event_dialog()

    def build_add_event_dialog(self):
        """Creates the Add Event dialog window."""
        pass

    def save_event(self, event_name: str, event_date: str):
        """Saves the new event.

        Args:
            event_name (str): Name of the event.
            event_date (str): Date of the event.
        """
        pass

# MDApp with ScreenManager and Navigation
class BusyBeeApp(MDApp):
    def build(self):
        """Initializes the app with a ScreenManager."""
        self.screen_manager = self.create_screen_manager()
        return self.screen_manager

    def create_screen_manager(self):
        """Creates and configures the ScreenManager."""
        pass

    def switch_to_screen(self, screen_name: str):
        """Switches between Calendar and To-Do List screens.

        Args:
            screen_name (str): Name of the target screen.
        """
        pass

    def on_navigation_button_press(self, screen_name: str):
        """Handles bottom navigation button presses.

        Args:
            screen_name (str): Name of the screen to navigate to.
        """
        pass
