#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtCore import Qt
import os

class SimpleWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

        self.simpleLayout = QHBoxLayout()
        self.simpleTitle = QLabel("Under Development")

        self.simpleLayout.addStretch(0)
        self.simpleLayout.addWidget(self.simpleTitle)
        self.simpleLayout.addStretch(0)

        self.dockAble()


    def dockAble(self):
        items = QDockWidget("Menu", self)
        items.setAllowedAreas(Qt.LeftDockWidgetArea)

        self.options = ["Manage Users", "Manage Rooms", "Logs", "Diagnostics"]
        self.listOptions = QListWidget(items)
        self.listOptions.addItems(self.options)
        self.listOptions.setAlternatingRowColors(True)

        items.setWidget(self.listOptions)