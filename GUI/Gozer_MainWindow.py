#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMenuBar
from Gozer_Widgets import Workspace, ManageRooms, ManageUsers, Logs, Diagnostics, SelfDestruct

class MenuBar(QMenuBar):
    """
        Summary: This class is a custom widget for the menu bar. As of now, it will only have 3 options 
            and the file option will only have a quite button.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fileMenu = QMenu("File")
        self.editMenu = QMenu("Edit")
        self.viewMenu = QMenu("View")

        self.addMenu(self.fileMenu)
        self.addMenu(self.editMenu)
        self.addMenu(self.viewMenu)

        self.quitAction = QAction("Quit", self)
        self.fileMenu.addAction(self.quitAction)

        self.quitAction.setShortcut("Ctrl+w")
        self.quitAction.triggered.connect(self.exitApp)

    def exitApp(self):
        sys.exit()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Gozer the Gozerian")

        menuBar = MenuBar()
        mainWidget = Workspace()
        
        self.setCentralWidget(mainWidget)
        self.setMenuBar(menuBar)