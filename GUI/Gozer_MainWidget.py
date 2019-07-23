#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLineEdit, QSizePolicy, QComboBox, QLabel
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
        
        self.setLayout(self.simpleLayout)

