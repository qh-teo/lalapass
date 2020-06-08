from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
# https://www.programcreek.com/python/example/96001/PyQt5.uic.loadUi

class accountManager_pg(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui_folder\\accountManager.ui', self)




        # self.show()

    def createTable(self, profiles):
        header_labels = ['Username', 'Password', 'Account Type']
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(profiles))
        self.tableWidget.setColumnCount(len(header_labels))
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.verticalHeader().setVisible(False)
        #loads table
        for i, profile in enumerate(profiles):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(profile[0]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(profile[1]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(profile[2]))


        self.horizontalLayout = QVBoxLayout()
        self.horizontalLayout.addWidget(self.tableWidget)
        self.setLayout(self.horizontalLayout)


