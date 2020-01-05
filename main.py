#!/usr/bin/python3
'''
Script   : main.py

Copyright: LiKneu 2019
'''

import sys
import glob
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

# Create a class of the main window to allow all widgets that are placed on it
# to communicate with each other
class MyWindow(QMainWindow):
    '''Class of the Main Window'''

    def __init__(self):
        '''Initializes the Main Window'''
        super(MyWindow, self).__init__()
        self.setGeometry(800, 200, 250, 300)
        self.setWindowTitle('gis')
        self.init_ui()

    def init_ui(self):
        '''Initializes the elements on the Main Window'''

        # Line Edit
        self.le_input = QtWidgets.QLineEdit(self)
        self.le_input.setGeometry(2, 0, 246, 30)
        self.le_input.setPlaceholderText('# indicates wanted activity')
        self.le_input.setClearButtonEnabled(True)
        self.le_input.textChanged.connect(self.input_changed)
        self.le_input.returnPressed.connect(self.line_edit_return)

        # List Widget
        self.lst = QtWidgets.QListWidget(self)
        self.lst.setSortingEnabled(True)
        self.lst.setAlternatingRowColors(True)
        self.lst.setGeometry(2, 30, 246, 100)
        # There is no returnPressed event for the List Widget
        # ~ self.lst.returnPressed.connect(self.list_return)

    def keyPressEvent(self, event):
        # ~ print(event.key())
        if event.key() == Qt.Key_Return:
            self.list_return()
        elif event.key() == Qt.Key_Enter:
            print('Enter')

    def input_changed(self):
        '''Handling of the users input is mainly done here.'''

        # Handling of bookmarks
        my_bookmarks = self.read_bookmark_files()
        
        if self.le_input.text().startswith('#b') and len(self.le_input.text()) <= 3:
            # ~ my_bookmarks = self.read_bookmark_files()
            self.lst.clear()
            for bm in my_bookmarks:
                self.lst.addItem(bm)

        if len(self.le_input.text()) > 3:
            command, user_input = self.le_input.text().split(' ', 1)
            self.lst.clear()
            for bm in my_bookmarks:
                if user_input.lower() in bm.lower():
                    self.lst.addItem(bm)
            
        # Clear the list in case no user input available
        if len(self.le_input.text()) < 2:
            self.lst.clear()

    def line_edit_return(self):
        '''Returns the first item of the list on RETURN in line edit field.'''

        # Get the text of the topmost item
        if self.lst.item(0):
            bookmark_key = self.lst.item(0).text()
            print('LE ->', bookmark_key)
            my_bookmarks = self.read_bookmark_files()
            print(my_bookmarks[bookmark_key])

    def list_return(self):
        '''Returns the selected list item on RETURN'''
        if self.lst.currentItem():
            bookmark_key = self.lst.currentItem().text()
            print('LI ->', bookmark_key)
            my_bookmarks = self.read_bookmark_files()
            print(my_bookmarks[bookmark_key])


    def read_bookmark_files(self, filetype='_bookmarks.txt'):
        """Returns a list of lists containing the bookmarks titles and URLs."""

        lines = {}
        for entry in glob.glob('./config_files/*'):
            if filetype in entry:
                with open(entry) as cf:
                    # Read the file content line by line
                    for line in cf:
                        # Ensure the line is not empty
                        if '|' in line:
                            # Remove whitespace from the line
                            line = line.strip()
                            # Split the string into Title and Command
                            title, command = line.split('|')
                            # Append Title and Command to the others
                            lines[title] = command
        return lines

def window():
    '''Main function'''
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
