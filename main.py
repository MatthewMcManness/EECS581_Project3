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
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.checkbox import CheckBox

# Calendar View Screen
class CalendarView(MDScreen):
    pass  # TODO: Add logic to display calendar grid dynamically. (Mariam)

# To-Do List View Screen
class ToDoListView(MDScreen):
    pass  # TODO: Add logic to display and manage task items. (Manvir)

# Modal for Adding a New Task
class AddTaskWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.priority = "Low"  # Default priority

        # Scrollable layout
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        inner_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        inner_layout.bind(minimum_height=inner_layout.setter('height'))

        # Input fields for task data
        inner_layout.add_widget(MDTextField(hint_text="Task Title", id="task_title"))
        inner_layout.add_widget(MDTextField(hint_text="Time (HH:MM)", id="task_time"))
        inner_layout.add_widget(MDTextField(hint_text="Location", id="task_location"))
        inner_layout.add_widget(MDTextField(hint_text="Notes", multiline=True, id="task_notes"))
        inner_layout.add_widget(MDTextField(hint_text="Deadline (YYYY-MM-DD)", id="task_deadline"))

        # Priority selection using CheckBox
        inner_layout.add_widget(MDLabel(text="Priority", halign="left"))
        priority_layout = BoxLayout(orientation='horizontal', spacing=10)
        for text in ["High", "Medium", "Low"]:
            checkbox = CheckBox(group="priority")
            checkbox.bind(active=lambda cb, state, p=text: self.set_priority(p) if state else None)
            priority_layout.add_widget(checkbox)
            priority_layout.add_widget(MDLabel(text=text))
        inner_layout.add_widget(priority_layout)

        # Add the inner layout to the scroll view
        scroll_view.add_widget(inner_layout)
        self.add_widget(scroll_view)

        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(MDFlatButton(text="CANCEL", on_release=lambda x: MDApp.get_running_app().close_task_window()))
        button_layout.add_widget(MDFlatButton(text="SAVE", on_release=self.save_task))
        self.add_widget(button_layout)

    def set_priority(self, priority):
        """Sets the selected priority."""
        self.priority = priority

    def save_task(self, *args):
        """Saves the task data."""
        task_data = {
            "title": self.ids.task_title.text,
            "time": self.ids.task_time.text,
            "location": self.ids.task_location.text,
            "notes": self.ids.task_notes.text,
            "deadline": self.ids.task_deadline.text,
            "priority": self.priority,
        }

        if not task_data["title"] or not task_data["time"]:
            print("Task Title and Time are required.")
            return

        print("Task Saved:", task_data)  # Placeholder for DB integration
        MDApp.get_running_app().close_task_window()

# Modal for Adding a New Event
class AddEventWindow(BoxLayout):
    def open(self):
        """Opens the Add Event dialog."""
        dialog = MDDialog(
            title="Add New Event",
            type="custom",
            content_cls=self,
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())],
        )
        dialog.content_cls.add_widget(MDLabel(text="Event Name: (Enter event here)", halign="center"))
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
        """Switches between Calendar and To-Do List screens."""
        self.root.current = screen_name

    def open_add_task_window(self):
        """Opens the Add Task dialog."""
        self.dialog = MDDialog(
            title="Add New Task",
            type="custom",
            content_cls=AddTaskWindow(),
            buttons=[MDFlatButton(text="CLOSE", on_release=self.close_task_window)],
            size_hint=(0.9, 0.9)  # Set size to fit the screen better
        )
        self.dialog.open()

    def close_task_window(self, *args):
        """Closes the Add Task dialog."""
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()

    def open_add_event_window(self):
        """Opens the Add Event dialog."""
        AddEventWindow().open()

if __name__ == "__main__":
    BusyBeeApp().run()