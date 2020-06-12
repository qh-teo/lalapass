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
        # self.profileView = QTableWidget()
        # self.profileView.doubleClicked.connect(self.on_click)


    # def createTable(self, profiles):
    #     header_labels = ['Username', 'Password', 'Account Type']
    #
    #     if profiles == None:
    #         profiles = ['Empty']
    #
    #     self.profileView.setRowCount(len(profiles))
    #     self.profileView.setColumnCount(len(header_labels))
    #     self.profileView.setHorizontalHeaderLabels(header_labels)
    #     self.profileView.setSelectionBehavior(QTableWidget.SelectRows)
    #
    #     self.profileView.verticalHeader().setVisible(False)
    #     #loads table
    #     for i, profile in enumerate(profiles):
    #         self.profileView.setItem(i, 0, QTableWidgetItem(profile[0]))
    #         self.profileView.setItem(i, 1, QTableWidgetItem(profile[1]))
    #         self.profileView.setItem(i, 2, QTableWidgetItem(profile[2]))
    #
    #     self.verticalLayout = QVBoxLayout()
    #     self.verticalLayout.addWidget(self.label)
    #     self.verticalLayout.addWidget(self.profileView)
    #     self.verticalLayout.addWidget(self.addProfileButton)
    #     self.verticalLayout.addWidget(self.deleteProfileButton)
    #     self.verticalLayout.addWidget(self.updateProfileButton)
    #     self.verticalLayout.addWidget(self.logoutButton)
    #     self.setLayout(self.verticalLayout)
    #
    #     self.show()


    # def on_click(self):
    #     print("sucess")
    #     self.go_to_addProfile()




