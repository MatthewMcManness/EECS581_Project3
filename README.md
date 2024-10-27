# BusyBee
A project created by Matthew McManness [2210261], Manvir Kaur [3064194], Magaly Camacho [3072618], Mariam Oraby [3127776], and Shravya Matta [3154808].

## Description
This proposal outlines the development of a mobile-friendly calendar and to-do list application using Python with Kivy and KivyMD for the user interface. The app will feature a modern and clean design, similar to popular productivity apps, with a bottom navigation bar to easily switch between the calendar and to-do list views. The Calendar section will display a grid for the current month, allowing users to view and interact with each day, while the To-Do List section will provide a scrollable list of tasks with the ability to add, check, and remove tasks. The user interface is built with KivyMD's material design components, providing a sleek and responsive look that fits perfectly on mobile devices.

## Running BusyBee 
To run BusyBee, first download the repository and install all requirements listed in the next section. Then, in a terminal, navigate to the *EECS581_Project3* directory and run the following command:
```
python main.py
```

## Requirements
First, make sure you have Python (and pip) installed. To download them, visit the Python website [here](https://www.python.org/downloads/).

The other requirements are Kivy, KivyMD, and SQLAlchemy. To install the these run the following in the terminal:
```
pip install Kivy Kivymd SQLAlchemy
```

If you use Anaconda, run the following instead:
```
conda install kivy -c conda-forge
```

For more information visit the [Kivy website](https://kivy.org/doc/stable/gettingstarted/installation.html#kivy-wheel-install) and the [SQLAlchemy website](https://www.sqlalchemy.org/download.html).

## Documentation Instructions
Some of the documentation was generated using Doxygen. To view this documentation, open the HTML files found in `./Documentation/Doxygen/html/`. We recommend starting with the *index.html* file located at `./documentation/html/index.html`.

For a better experience, view these files in a browser after the repository is downloaded to a system.

From there, you can either click on the Namespaces or Classes tab near the top to access other pages, or you can use the search bar in the top right to search through documentation directly.
