==========
car_log.py
==========


Author:
==========
CAM 


About:
==========
UI program written in Python and PyQt5 and uses SQLite for the backend database. 
The purpose is to create an application to track car maintenance performed and a 
gas log. Several features includes a car payment calculator (under "Tools"), ability 
to change the theme (App display), calculation of the total cost of maintenance, 
and fuel economy calulation for the last gas log. See the screen shots under the
screenshots folder for further examples

Several files support the car_log program

- car_log.py 
	Main program
- car_log_layout.pptx (under files)
	Used for originial concept of the layout of the PyQt widgets
- create_db.py
	Used to create the database used for the car_log.py program
- read_db.py
	Used to review the database ensuring that it was created correctly

Usage:
==========
Simply run the program. 

Development:
===========
The car maintenance program has the following features:

- Menu - (PyQt5 menuBar) Dropdown menus with "File", "Menu", and "Help"
- Add Row - (PyQt5 QPushButton) Allows the user to add a row that can be populated
- Delete Row - (PyQt5 QPushButton) Allows the user to delete any row
- Sorting Options - (PyQt5 QComboBox) Aloows the user to sort by "Date", "Mileage", or "Item"
- Exit - (PyQt5 QPushButton)Prompts the user if they want to exit or not, if "Yes" db table will be saved
- Message Bar - (PyQt5 statusBar) Message welcoming the user to the Car Maintenance Log program
- Qt Style Sheets (QSS) - For changing the display (Themes)


Notes:
==========
None

Screen Shots:
==========
.. image:: screenshots
