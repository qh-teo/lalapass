from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from database import init_db,login_verification
from create_acc import create_acc
from welcome_pg import welcome_pg
from login_pg import login_pg
from registerAccount_pg import registerAccount_pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_folder\mainwindow.ui", self)

        # set up welcome page page
        self.welcome = welcome_pg()
        self.stackedWidget.addWidget(self.welcome)
        self.welcome.loginButton.clicked.connect(self.go_to_login)
        self.welcome.registerButton.clicked.connect(self.go_to_register)

        # set up register account page
        self.registerAccount = registerAccount_pg()
        self.stackedWidget.addWidget(self.registerAccount)
        self.registerAccount.registerAcc_but.clicked.connect(self.registering)

        # set up login page
        self.login = login_pg()
        self.stackedWidget.addWidget(self.login)
        self.login.login_but.clicked.connect(self.logging_in)


    def go_to_first(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_register(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_login(self):
        self.stackedWidget.setCurrentIndex(2)

    def registering(self):
        user_value = self.registerAccount.userEntry.text()
        pw_value = self.registerAccount.passEntry.text()
        create_acc(user_value, pw_value)
        QMessageBox.question(self, "Account Created", "Please login to access features." + user_value + " "
                             + pw_value, QMessageBox.Ok)
        self.go_to_first()

    def logging_in(self):
        user_value = self.login.userEntry.text()
        pw_value = self.login.passEntry.text()
        login_verification(user_value,pw_value)


if __name__ == '__main__':
    init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()