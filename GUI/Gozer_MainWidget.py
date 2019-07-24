#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget, QStackedWidget
from PyQt5.QtCore import Qt
import os

class leftList(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SimpleButton(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QPushButton("Manage Users")
        self.layout.addWidget(self.simpleText)


class SimpleLabel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QLabel("Manages Rooms")
        self.layout.addWidget(self.simpleText)

class SimpleLineEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QLineEdit("Logs")
        self.layout.addWidget(self.simpleText)

class SimpleComboBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QTextEdit("Diagnostics")
        self.layout.addWidget(self.simpleText)
        
        
class Workspace(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Menu = QListWidget()
        
        self.Menu.insertItem(0, "Manage Users")
        self.Menu.insertItem(1, "Manage Rooms")
        self.Menu.insertItem(2, "Logs")
        self.Menu.insertItem(3, "Diagnostics")

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(SimpleButton())
        self.Stack.addWidget(SimpleLabel())
        self.Stack.addWidget(SimpleLineEdit())
        self.Stack.addWidget(SimpleComboBox())

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.Menu)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.Menu.currentRowChanged.connect(self.display)

    def display(self,i):
        self.Stack.setCurrentIndex(i)
