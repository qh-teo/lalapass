from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class addProfile_pg(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui_folder\\addProfile.ui', self)