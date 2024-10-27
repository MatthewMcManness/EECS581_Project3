from kivy.uix.screenmanager import Screen

class ToDoListView(Screen):
    """A screen for displaying the To-Do List."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self, task_data):
        """Add a new task to the list."""
        print(f"Added task: {task_data}")
