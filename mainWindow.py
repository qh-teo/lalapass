from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from database import init_db,login_verification,create_profile, retrieve_profile
from create_acc import create_acc
from welcome_pg import welcome_pg
from login_pg import login_pg
from registerAccount_pg import registerAccount_pg
from accountManager_pg import accountManager_pg
from addProfile_pg import addProfile_pg
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

accountDetails = None
profileDetails = None


class User_account:
    def __init__(self, user_id, encryptionKey):
        self.user_id = user_id
        self.encryptionKey = encryptionKey

    @property
    def getUserId(self):
        return self.user_id

    @property
    def getEncryptionKey(self):
        return self.encryptionKey


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_folder\mainwindow.ui", self)

        # set up welcome page
        self.welcome_pg = welcome_pg()
        self.stackedWidget.addWidget(self.welcome_pg)
        self.welcome_pg.loginButton.clicked.connect(self.go_to_login)
        self.welcome_pg.registerButton.clicked.connect(self.go_to_register)

        # set up register account page
        self.registerAccount_pg = registerAccount_pg()
        self.stackedWidget.addWidget(self.registerAccount_pg)
        self.registerAccount_pg.registerAcc_but.clicked.connect(self.registering)

        # set up login page
        self.login_pg = login_pg()
        self.stackedWidget.addWidget(self.login_pg)
        self.login_pg.login_but.clicked.connect(self.logging_in)

        # set up account manager page
        self.accountManager_pg = accountManager_pg()
        self.stackedWidget.addWidget(self.accountManager_pg)
        self.accountManager_pg.addProfileButton.clicked.connect(self.go_to_addProfile)

        # set up add profile page
        self.addProfile_pg = addProfile_pg()
        self.stackedWidget.addWidget(self.addProfile_pg)
        self.addProfile_pg.submitButton.clicked.connect(self.add_profile)

    # Navigational Methods

    def go_to_first(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_register(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_login(self):
        self.stackedWidget.setCurrentIndex(2)

    def go_to_accountManager(self):
        self.stackedWidget.setCurrentIndex(3)
        profiles = retrieve_profile(accountDetails.getUserId)
        # print(profiles)
        profiles = self.decrypt_pw(profiles)
        self.accountManager_pg.createTable(profiles)

    def go_to_addProfile(self):
        self.stackedWidget.setCurrentIndex(4)

    def registering(self):
        user_value = self.registerAccount_pg.userEntry.text()
        pw_value = self.registerAccount_pg.passEntry.text()
        repass_value = self.registerAccount_pg.repassEntry.text()

        if pw_value != repass_value:
            QMessageBox.question(self, "Error", "Passwords do not match. Please try again.", QMessageBox.Ok)
            self.registerAccount_pg.passEntry.clear()
            self.registerAccount_pg.repassEntry.clear()
        else:
            create_acc(user_value, pw_value)
            QMessageBox.question(self, "Account Created", "Please login to access features.", QMessageBox.Ok)
            self.registerAccount_pg.userEntry.clear()
            self.registerAccount_pg.passEntry.clear()
            self.registerAccount_pg.repassEntry.clear()
            self.go_to_first()
        user_value = None
        pw_value = None
        repass_value =None

    # Log in and verification methods

    def logging_in(self):
        user_value = self.login_pg.userEntry.text()
        pw_value = self.login_pg.passEntry.text()
        loginSuccess = login_verification(user_value, pw_value)
        if loginSuccess[0] is True:
            encryptionKey = self.generateEncryptionKey(user_value, pw_value, loginSuccess[2])
            global accountDetails
            accountDetails = User_account(loginSuccess[1], encryptionKey)
            self.go_to_accountManager()
        else:
            QMessageBox.question(self, "Login error", "Username/Password incorrect. Please retry again.",
                                 QMessageBox.Ok)
            self.login_pg.userEntry.clear()
            self.login_pg.passEntry.clear()
        user_value = None
        pw_value = None

    def generateEncryptionKey(self, user, pw, salt):
        password = pw + user
        byte_pw = bytes(password.encode('utf8'))
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(byte_pw))
        return key

    def add_profile(self):
        user_value = self.addProfile_pg.userEntry.text()
        pw_value = self.addProfile_pg.passEntry.text()
        profile_type = self.addProfile_pg.protypeEntry.text()
        byte_pw = bytes(pw_value.encode('utf8'))
        f = Fernet(accountDetails.getEncryptionKey)
        token = f.encrypt(byte_pw)
        create_profile(accountDetails.getUserId,user_value, token, profile_type)

        user_value = None
        pw_value = None
        profile_type = None

    def decrypt_pw(self, profiles):
        for i, profile in enumerate(profiles):
            f = Fernet(accountDetails.getEncryptionKey)
            decryptedPw = f.decrypt(profile[1])
            decodePw = decryptedPw.decode("utf-8")
            profile = list(profile)
            profile[1] = decodePw
            profiles[i] = profile
        return profiles


if __name__ == '__main__':
    init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()