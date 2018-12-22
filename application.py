import counters
import averages
import people

import sys

from PyQt5.QtWidgets import *


# Constants
APP_NAME = "Facebook Messenger Counter"

# Global Variables
data = {}
message_types = {}
people_data = {}


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setObjectName("Window")
        self.colours = {"bg_primary": "ffffff", "bg_secondary": "f5f5f5", "fg_primary": "3e4245",
                        "fg_secondary": "606368", "txt_primary": "141418", "context_primary": "355dd0",
                        "context_secondary": "e9effe"}

def main(data_, message_types_, people_data_):
    global data
    global message_types
    global people_data
    data = data_
    message_types = message_types_
    people_data = people_data_

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)

    window = Window()
    window.setWindowTitle(APP_NAME)
    window.show()

    app.exec_()
