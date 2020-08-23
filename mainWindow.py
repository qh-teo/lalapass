from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QLineEdit
from database import init_db, login_verification, create_profile, retrieve_profile, update_profile, \
    delete_profile_from_db
from create_acc import create_acc
from welcome_pg import welcome_pg
from login_pg import login_pg
from registerAccount_pg import registerAccount_pg
from accountManager_pg import accountManager_pg
from addProfile_pg import addProfile_pg
from updateProfile_pg import updateProfile_pg
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

accountDetails = None
profileDetails = None
userprofileId = None


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


class User_profiles:
    def __init__(self, profiles):
        self.profiles = profiles

    @property
    def getProfiles(self):
        return self.profiles


class Profile_Id:
    def __init__(self, profileId):
        self.profileId = profileId

    @property
    def getProfileId(self):
        return self.profileId


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
        self.accountManager_pg.profileView = QTableWidget()
        self.accountManager_pg.profileView.doubleClicked.connect(self.on_click_profileRow)
        self.accountManager_pg.deleteProfileButton.clicked.connect(self.deleteProfile)
        self.accountManager_pg.logoutButton.clicked.connect(self.logoutAccount)

        # set up add profile page
        self.addProfile_pg = addProfile_pg()
        self.stackedWidget.addWidget(self.addProfile_pg)
        self.addProfile_pg.submitButton.clicked.connect(self.add_profile)

        # set up update profile page
        self.updateProfile_pg = updateProfile_pg()
        self.stackedWidget.addWidget(self.updateProfile_pg)
        self.updateProfile_pg.showPwButton.clicked.connect(self.showPassword)
        self.updateProfile_pg.submitButton.clicked.connect(self.updateProfile)
        self.updateProfile_pg.cancelButton.clicked.connect(self.cancelUpdate)

    # Navigational Methods

    def go_to_welcome(self):  # goes to welcome page
        self.stackedWidget.setCurrentIndex(0)

    def go_to_register(self):  # goes to register acc page
        self.stackedWidget.setCurrentIndex(1)

    def go_to_login(self):  # goes to login page
        self.stackedWidget.setCurrentIndex(2)

    def go_to_accountManager(self):  # goes to account manager page
        self.createTable()
        self.stackedWidget.setCurrentIndex(3)

    def go_to_addProfile(self):  # goes to add profile page
        self.stackedWidget.setCurrentIndex(4)

    def go_to_updateProfile(self):  # goes to update profile page
        self.stackedWidget.setCurrentIndex(5)

    def showPassword(self):  # allows user to view password in plaintext
        buttonText = self.updateProfile_pg.showPwButton.text()
        if buttonText == "Show Password":
            self.updateProfile_pg.passEntry.setEchoMode(QLineEdit.Normal)
            self.updateProfile_pg.showPwButton.setText("Hide Password")
        elif buttonText == "Hide Password":
            self.updateProfile_pg.passEntry.setEchoMode(QLineEdit.Password)
            self.updateProfile_pg.showPwButton.setText("Show Password")

    def logoutAccount(self):
        QMessageBox.question(self, "Logout",
                             "You will now be logged out. Please confirm if you will want to confirm.",
                             QMessageBox.Ok)
        self.stackedWidget.setCurrentIndex(0)




    def createTable(self):  # generates profiles under account user
        profiles = retrieve_profile(accountDetails.getUserId)
        profiles = self.decrypt_pw(profiles)

        header_labels = ['Username', 'Password', 'Account Type']
        if profiles is None:
            profiles = ['']
        global profileDetails
        profileDetails = User_profiles(profiles)
        self.accountManager_pg.profileView.clearContents()
        self.accountManager_pg.profileView.setRowCount(len(profiles))
        self.accountManager_pg.profileView.setColumnCount(len(header_labels))
        self.accountManager_pg.profileView.setHorizontalHeaderLabels(header_labels)
        self.accountManager_pg.profileView.setSelectionBehavior(QTableWidget.SelectRows)
        self.accountManager_pg.profileView.verticalHeader().setVisible(False)
        # loads table
        for i, profile in enumerate(profiles):
            self.accountManager_pg.profileView.setItem(i, 0, QTableWidgetItem(profile[1]))
            self.accountManager_pg.profileView.setItem(i, 1, QTableWidgetItem(profile[2]))
            self.accountManager_pg.profileView.setItem(i, 2, QTableWidgetItem(profile[3]))

        self.accountManager_pg.verticalLayout = QVBoxLayout()
        self.accountManager_pg.verticalLayout.addWidget(self.accountManager_pg.label)
        self.accountManager_pg.verticalLayout.addWidget(self.accountManager_pg.profileView)
        self.accountManager_pg.verticalLayout.addWidget(self.accountManager_pg.addProfileButton)
        self.accountManager_pg.verticalLayout.addWidget(self.accountManager_pg.deleteProfileButton)
        self.accountManager_pg.verticalLayout.addWidget(self.accountManager_pg.logoutButton)
        self.accountManager_pg.setLayout(self.accountManager_pg.verticalLayout)
        self.accountManager_pg.show()

    @pyqtSlot()
    def on_click_profileRow(self):
        indexes = self.accountManager_pg.profileView.selectionModel().selectedRows()
        global userprofileId
        for index in sorted(indexes):
            self.updateProfile_pg.userEntry.setText(profileDetails.getProfiles[index.row()][1])
            self.updateProfile_pg.passEntry.setText(profileDetails.getProfiles[index.row()][2])
            self.updateProfile_pg.protypeEntry.setText(profileDetails.getProfiles[index.row()][3])
            userprofileId = Profile_Id(profileDetails.getProfiles[index.row()][0])
            self.go_to_updateProfile()

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
            self.go_to_welcome()
        user_value = None
        pw_value = None
        repass_value = None

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
        create_profile(accountDetails.getUserId, user_value, token, profile_type)
        QMessageBox
        QMessageBox.question(self, "Profile Created",
                             "Your profile has been created, you will now be brought to the previous page",
                             QMessageBox.Ok)
        user_value = None
        pw_value = None
        profile_type = None
        self.addProfile_pg.userEntry.clear()
        self.addProfile_pg.passEntry.clear()
        self.addProfile_pg.protypeEntry.clear()
        self.go_to_accountManager()

    def decrypt_pw(self, profiles):
        for i, profile in enumerate(profiles):
            f = Fernet(accountDetails.getEncryptionKey)
            decryptedPw = f.decrypt(profile[2])
            decodePw = decryptedPw.decode("utf-8")
            profile = list(profile)
            profile[2] = decodePw
            profiles[i] = profile
        return profiles

    def updateProfile(self):  # updating user-selected profile
        user_value = self.updateProfile_pg.userEntry.text()
        pw_value = self.updateProfile_pg.passEntry.text()
        profile_type = self.updateProfile_pg.protypeEntry.text()

        byte_pw = bytes(pw_value.encode('utf8'))
        f = Fernet(accountDetails.getEncryptionKey)
        token = f.encrypt(byte_pw)
        profile_id = userprofileId.getProfileId

        update_profile(profile_id, user_value, token, profile_type)
        QMessageBox.question(self, "Profile Updated",
                             "Your profile has been updated, you will now be brought to the previous page",
                             QMessageBox.Ok)
        self.createTable()

    def deleteProfile(self):  # gets profile id and prompts user if they want to delete it
        indexes = self.accountManager_pg.profileView.selectionModel().selectedRows()
        global userprofileId
        for index in sorted(indexes):
            userprofileId = Profile_Id(profileDetails.getProfiles[index.row()][0])

            result = QMessageBox.question(self, "Delete Profile?",
                                          "Selected profile \'" + profileDetails.getProfiles[index.row()][1] +
                                          "\' will be deleted. Are you sure?",
                                          QMessageBox.Ok | QMessageBox.Cancel)
            if result == QMessageBox.Ok:
                delete_profile_from_db(userprofileId.getProfileId)
                result = QMessageBox.question(self, "Profile deleted",
                                              "Profile deleted.",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                self.createTable()
                self.stackedWidget.setCurrentIndex(3)

    def cancelUpdate(self):  # cancel update message box
        result = QMessageBox.question(self, "Stop updating",
                                      "Your profile will not be updated, are you sure?",
                                      QMessageBox.Ok | QMessageBox.Cancel)
        if result == QMessageBox.Ok:
            self.stackedWidget.setCurrentIndex(3)


if __name__ == '__main__':
    init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
