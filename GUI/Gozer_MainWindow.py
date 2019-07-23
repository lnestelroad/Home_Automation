#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow
from Gozer_MainWidget import SimpleWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.setWindowTitle("Gozer the Gozerian")
      # mainWidget = MainWidget()
      mainWidget = SimpleWidget()
      self.setCentralWidget(mainWidget)
