from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from addProfile_pg import addProfile_pg
# https://www.programcreek.com/python/example/96001/PyQt5.uic.loadUi
from PyQt5.uic.properties import QtWidgets, QtGui


#to come back and look at it once done. currently ui from designer and actual page does not tally

class accountManager_pg(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui_folder\\accountManager.ui', self)




