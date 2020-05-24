import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QAction, \
    QInputDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from database import init_db
from create_acc import login


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'LalaPass Account Manager'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()


    def initUI(self):
        # super(App,self).__init__()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.statusBar().showMessage('Message in status bar')

        # mainMenu = self.menuBar()
        # fileMenu = mainMenu.addMenu('File')
        # editMenu = mainMenu.addMenu('Edit')
        # viewMenu = mainMenu.addMenu('View')
        # searchMenu = mainMenu.addMenu('Search')
        # toolsMenu = mainMenu.addMenu('Tools')
        # helpMenu = mainMenu.addMenu('Help')
        #
        # exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        # exitButton.setShortcut('Ctrl+Q')
        # exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        # fileMenu.addAction(exitButton)

        user_label = QLabel(self)
        user_label.setText("Username:")
        user_label.move(20, 20)

        pass_label = QLabel(self)
        pass_label.setText("Password:")
        pass_label.move(20, 50)

        # User Input
        self.user_entry = QLineEdit(self)
        self.user_entry.move(80, 25)
        self.user_entry.resize(140, 20)

        self.pw_entry = QLineEdit(self)
        self.pw_entry.setEchoMode(QLineEdit.Password)
        self.pw_entry.Password
        self.pw_entry.move(80, 55)
        self.pw_entry.resize(140, 20)

        # Create a button in the window
        self.button = QPushButton('Create Account', self)
        self.button.move(20, 80)

        self.button.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        user_value = self.user_entry.text()
        pw_value = self.pw_entry.text()
        login(user_value, pw_value)
        QMessageBox.question(self, "Message You typed: ", "You typed :" + user_value + "  " + pw_value, QMessageBox.Ok)


if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

