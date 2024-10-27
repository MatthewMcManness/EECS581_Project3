from kivy.app import App
import sys
import os

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from busybee import BusyBeeApp  # Absolute import

if __name__ == "__main__":
    BusyBeeApp().run()


