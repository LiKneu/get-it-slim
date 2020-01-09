#!/usr/bin/python3
'''
Script   : main.py

Copyright: LiKneu 2019
'''

import os
import sys
import glob
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

# Create a class of the main window to allow all widgets that are placed on it
# to communicate with each other
class MyWindow(QMainWindow):
    '''Class of the Main Window'''

    def __init__(self):
        '''Initializes the Main Window'''
        super(MyWindow, self).__init__()
        self.setGeometry(800, 200, 300, 167)
        self.setWindowTitle('g-i-s     v.2020-01-09')
        self.init_ui()
        self.user_command = ''
        self.user_input = ''

    def init_ui(self):
        '''Initializes the elements on the Main Window'''

        # Line Edit
        self.le_input = QtWidgets.QLineEdit(self)
        self.le_input.setGeometry(2, 0, 296, 30)
        self.le_input.setPlaceholderText('<command> <input>')
        self.le_input.setClearButtonEnabled(True)
        self.le_input.installEventFilter(self)
        self.le_input.textChanged.connect(self.input_changed)

        # List Widget
        self.lst = QtWidgets.QListWidget(self)
        self.lst.setSortingEnabled(True)
        self.lst.setAlternatingRowColors(True)
        self.lst.setGeometry(2, 35, 296, 130)
        self.lst.installEventFilter(self)

    def eventFilter(self, obj, event):
        '''Event filter needed to catch the change of focus.'''
        if event.type() == QEvent.FocusIn:
            if obj == self.lst:
                print('List Widget')
                self.FOCUS = 'List Widget'
            if obj == self.le_input:
                print('Line Edit')
                self.FOCUS = 'Line Edit'
                # Deselect all list items if List Widget looses the focus
                self.lst.setCurrentRow(0)
                self.lst.clearSelection()

        return super(MyWindow, self).eventFilter(obj, event)

    def keyPressEvent(self, event):
        '''Detect that the RETURN key was pressed.'''
        if event.key() == Qt.Key_Return:
            self.return_pressed()
        elif event.key() == Qt.Key_Enter:
            print('Enter')

    def input_changed(self):
        '''Handling of the users input is mainly done here.'''

        # Try to split the user input into the parts 'command' and 'user_input'.
        # The delimiter is a space. Thus it's possible to have commands of arbi-
        # trary length.
        try:
            self.user_command, self.user_input = self.le_input.text().split(' ', 1)
            print(f'\tUser input: <{self.user_command}>, <{self.user_input}>')
        except:
            # Reset user command and input to empty strings
            self.user_command = ''
            self.user_input = ''
            
            # List Widget has to be cleared if no valid user input is available
            self.lst.clear()
            self.main_win_small()
            return

        # Handling of bookmarks
        if self.user_command == 'b' and self.user_input == '':
            my_bookmarks = self.read_bookmark_files()
            self.lst.clear()
            for bm in my_bookmarks:
                self.lst.addItem(bm)
            self.main_win_large()
        elif self.user_command == 'b' and self.user_input:
            my_bookmarks = self.read_bookmark_files()
            self.lst.clear()
            for bm in my_bookmarks:
                if self.user_input.lower() in bm.lower():
                    self.lst.addItem(bm)
            self.main_win_large()
        # No known command
        else:
            self.lst.clear()
            self.main_win_small()

    def main_win_large(self):
        '''Set dimensions of main window so that all widgets can be seen.'''
        self.resize(300, 167)

    def main_win_small(self):
        '''Set dimensions of main window so that just Line Edit can be seen.'''
        self.resize(300, 32)

    def return_pressed(self):
        print('return_pressed', self.FOCUS)
        if self.FOCUS == 'List Widget':
            self.list_return()
        elif self.FOCUS == 'Line Edit':
            if self.user_command == 'b':
                self.line_edit_return()
            elif self.user_command == 'p' and self.user_input:
                settings = self.read_config_file()
                cmd = settings['PCR-URL']
                cmd = cmd + self.user_input
                self.run_command(cmd)
            # Handle CSCs
            elif self.user_command == 'c' and self.user_input:
                settings = self.read_config_file()
                cmd = settings['CSC-URL']
                cmd = cmd + self.user_input
                self.run_command(cmd)
        else:
            print('Error in RETURN handler')

    def line_edit_return(self):
        '''Returns the first item of the list on RETURN in line edit field.'''

        # Get the text of the topmost item
        if self.lst.item(0):
            bookmark_key = self.lst.item(0).text()
            # TODO: remove print statement
            print('\tBookmark title:', bookmark_key)
            my_bookmarks = self.read_bookmark_files()
            # TODO: remove print statement
            print('\tBookmark command:', my_bookmarks[bookmark_key])
            self.run_command(my_bookmarks[bookmark_key])

    def list_return(self):
        '''Returns the selected list item on RETURN'''
        if self.lst.currentItem():
            bookmark_key = self.lst.currentItem().text()
            # TODO: remove print statement
            print('\tBookmark title:', bookmark_key)
            my_bookmarks = self.read_bookmark_files()
            # TODO: remove print statement
            print('\tBookmark command:', my_bookmarks[bookmark_key])
            self.run_command(my_bookmarks[bookmark_key])

    def run_command(self, command):
        '''Runs the command provided by Line Edit or List Widget.'''
        my_os = os.name
        # TODO: Remove print statement
        print('OS:', my_os)
        print(f'Try to run command: {command}')
        # FIXIT: In case the app runs on Linux add '&' to the command
        if my_os == 'posix':
            command = command + ' &'
            os.system(command)
        elif my_os == 'windows':
            command = 'start ' + command
            os.system(command)
        else:
            print(f'Unknown OS: {my_os}. Script might not work as expected.')

    def read_bookmark_files(self, filetype='_bookmarks.txt'):
        """Returns a list of lists containing the bookmarks titles and URLs."""

        lines = {}
        for entry in glob.glob('./config_files/bookmarks/*'):
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

    def read_config_file(self):
        '''Returns configuration settings in a dict'''
        settings = {}
        cfg_file = './config_files/get-it-slim_conf.txt'
        with open(cfg_file) as cfg:
            for line in cfg:
                if '|' in line:
                    line = line.strip()
                    key, value = line.split('|', 1)
                    settings[key] = value
        return settings

def window():
    '''Main function'''
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
