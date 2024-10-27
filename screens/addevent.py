from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from screens.usefulwidgets import DatePicker
from screens.usefulwidgets import TimePicker

class AddEventModal(ModalView):
    #A modal for adding a new event.
    
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
        #Open the DatePicker popup.
        DatePicker(self).open()

    def save_event(self, *args):
        #Save the event.
        event_name = self.event_name_input.text.strip()
        event_date = self.event_date_label.text

        # Ensure the event has a name before saving
        if not event_name:
            print("Event Name is required.")
            return

        print(f"Event '{event_name}' scheduled for {event_date}")
        self.dismiss()  # Close the modal