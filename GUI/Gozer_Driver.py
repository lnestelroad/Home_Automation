#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from Gozer_MainWindow import MainWindow

import sys
import os
import signal

def main():
    app = QApplication(sys.argv)
    
    mw = MainWindow()
    mw.setGeometry(0, 0, mw.width()*2, mw.height()*2)
    mw.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit(app.exec())

if __name__ == "__main__":
    main()