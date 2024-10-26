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
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel

# Calendar View Screen
class CalendarView(MDScreen):
    pass

# To-Do List View Screen
class ToDoListView(MDScreen):
    pass

# Modal for Adding a New Task
class AddTaskWindow(BoxLayout):
    def open(self):
        """Opens the Add Task dialog."""
        dialog = MDDialog(
            title="Add New Task",
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss()),
            ],
        )
        dialog.content_cls.add_widget(MDLabel(text="Task Name: (Enter task here)", halign="center"))
        dialog.open()

# Modal for Adding a New Event
class AddEventWindow(BoxLayout):
    def open(self):
        """Opens the Add Event dialog."""
        dialog = MDDialog(
            title="Add New Event",
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss()),
            ],
        )
        dialog.content_cls.add_widget(MDLabel(text="Event Name: (Enter event here)", halign="center"))
        dialog.open()

# Main App with ScreenManager
class BusyBeeApp(MDApp):
    def build(self):
        """Initializes the app and loads the KV file."""
        Builder.load_file("busybee.kv")
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(CalendarView(nafrom kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel

# Calendar View Screen
class CalendarView(MDScreen):
    pass  # TODO: Add logic to display calendar grid dynamically. (Mariam)

# To-Do List View Screen
class ToDoListView(MDScreen):
    pass  # TODO: Add logic to display and manage task items. (Manvir)

# Modal for Adding a New Task
class AddTaskWindow(BoxLayout):
    def open(self):
        """Opens the Add Task dialog."""
        dialog = MDDialog(
            title="Add New Task",
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss()),
            ],
        )
        # TODO: Add input fields here. (Matthew)
        dialog.content_cls.add_widget(
            MDLabel(text="Task Name: (Enter task here)", halign="center")
        )
        dialog.open()

# Modal for Adding a New Event
class AddEventWindow(BoxLayout):
    def open(self):
        """Opens the Add Event dialog."""
        dialog = MDDialog(
            title="Add New Event",
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss()),
            ],
        )
        # TODO: Add input fields here. (Shravya)
        dialog.content_cls.add_widget(
            MDLabel(text="Event Name: (Enter event here)", halign="center")
        )
        dialog.open()

# Main App with ScreenManager
class BusyBeeApp(MDApp):
    def build(self):
        """Initializes the app and loads the KV file."""
        Builder.load_file("busybee.kv")
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(CalendarView(name="calendar"))
        screen_manager.add_widget(ToDoListView(name="todo"))
        return screen_manager

    def switch_to_screen(self, screen_name: str):
        """Switch between Calendar and To-Do List screens."""
        self.root.current = screen_name

    def open_add_task_window(self):
        """Opens the Add Task dialog."""
        AddTaskWindow().open()

    def open_add_event_window(self):
        """Opens the Add Event dialog."""
        AddEventWindow().open()

if __name__ == "__main__":
    BusyBeeApp().run()
