# Name: themes.py
# Description: Light mode and dark mode settings
# Programmer: Magaly Camacho (3072618)
# Date Created: December 7, 2024
# Revision History:
# - December 7, 2024: Initial version created (Author: Magaly Camacho)

from enum import Enum
from kivy.utils import get_color_from_hex

class Theme(Enum):
    LIGHT = 0
    DARK = 1
    
    @staticmethod
    def toggle(theme):
        if theme == Theme.LIGHT:
            return Theme.DARK
        
        return Theme.LIGHT
    
    def get_settings(self) -> dict:
        return THEME_SETTINGS[self.value]


LIGHT_MODE = {
    "Title_Color": get_color_from_hex("#FFFFFF"),
    "Background_Color": get_color_from_hex("#BFB1C1"),
    "Button_Color": get_color_from_hex("#4381C1"),
    "Day_Label_Color": get_color_from_hex("#92DCE5"),
    "Day_Button_Color": get_color_from_hex("#EEE5E9")
}

DARK_MODE = {
    "Title_Color": get_color_from_hex("#FFFFFF"),
    "Background_Color": get_color_from_hex("#000000"),
    "Button_Color": get_color_from_hex("#4381C1"),
    "Day_Label_Color": get_color_from_hex("#92DCE5"),
    "Day_Button_Color": get_color_from_hex("#EEE5E9")
}

THEME_SETTINGS = [LIGHT_MODE, DARK_MODE]