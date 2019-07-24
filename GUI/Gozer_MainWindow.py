#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QStackedLayout
from Gozer_MainWidget import SimpleLabel, SimpleButton, leftList, Workspace

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Gozer the Gozerian")
        # mainWidget = MainWidget()
        mainWidget = Workspace()
        
        self.setCentralWidget(mainWidget)