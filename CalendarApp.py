from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivy.metrics import dp
import calendar
from datetime import datetime

Window.size = (350, 600)

KV = """
ScreenManager:
    CalendarScreen:

<CalendarScreen>:
    name: "calendar"
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: "Calendar"
            pos_hint: {"top": 1}
            left_action_items: [["menu", lambda x: app.open_menu()]]
        MDLabel:
            text: root.get_month_year()
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H5"
            size_hint_y: None
            height: self.texture_size[1] + dp(30)
        BoxLayout:
            size_hint_y: None
            height: "50dp"
            MDLabel:
                text: "Mon"
                halign: "center"
            MDLabel:
                text: "Tue"
                halign: "center"
            MDLabel:
                text: "Wed"
                halign: "center"
            MDLabel:
                text: "Thu"
                halign: "center"
            MDLabel:
                text: "Fri"
                halign: "center"
            MDLabel:
                text: "Sat"
                halign: "center"
            MDLabel:
                text: "Sun"
                halign: "center"
        ScrollView:
            GridLayout:
                id: calendar_grid
                cols: 7
                padding: dp(10)
                spacing: dp(5)
                row_default_height: dp(40)
                row_force_default: True
                adaptive_height: True
"""

class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

    def on_enter(self):
        if 'calendar_grid' in self.ids:
            self.populate_calendar()
        else:
            print("calendar_grid not found!")

    def get_month_year(self):
        """Returns the month and year for display."""
        return datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def populate_calendar(self):
        """Generates the calendar grid."""
        grid = self.ids['calendar_grid']
        grid.clear_widgets()

        # Get the days of the week and days in the month
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Add day numbers to the grid
        for week in cal:
            for day in week:
                if day == 0:
                    grid.add_widget(MDLabel())  # Empty label for blank spaces
                else:
                    grid.add_widget(
                        MDRaisedButton(
                            text=str(day),
                            on_press=self.on_day_press,
                            size_hint=(1,None),
                            height=dp(40),
                        )
                    )

    def on_day_press(self, instance):
        """Handles the event when a day is pressed."""
        print(f"You selected day: {instance.text}")

class ToDoListScreen(Screen):
    pass

class CalendarApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def open_menu(self):
        print("Menu button pressed")

if __name__ == "__main__":
    CalendarApp().run()
