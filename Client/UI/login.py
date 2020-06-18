from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

import sys, json

def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler) 

class LoginWindow(QMainWindow):
	def __init__(self, flags, networkManager, sessionData):
		super().__init__()
		self.flags = flags
		self.networkManager = networkManager
		self.sessionData = sessionData

		self.setWindowIcon(QIcon('Resources/Assets/logo.png'))
		self.setWindowTitle('AnonChat [ LOGIN ]')
		self.setObjectName('loginWindow')

		loginWidget = QWidget()
		loginLayout = self.getMainLayout()
		loginWidget.setLayout(loginLayout)
		self.setCentralWidget(loginWidget)
		self.setFixedSize(600, 700)
		self.setGeometry(600, 200, 600, 700) 


	def getMainLayout(self):
		self.loginWidget = self.getLoginWidget()
		self.registerWidget = self.getRegisterWidget()
		self.mainTabs = QTabWidget()
		self.mainTabs.setObjectName('loginTabs')
		self.mainTabs.addTab(self.loginWidget, '')
		self.mainTabs.addTab(self.registerWidget, '')

		self.topHeading = QLabel('AnonChat')
		self.topHeading.setObjectName('subsectionHeading')
		self.topHeading.setAlignment(Qt.AlignCenter)

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(self.topHeading)
		mainLayout.addWidget(self.mainTabs)
		mainLayout.setSpacing(0)
		mainLayout.setStretch(0, 10)
		mainLayout.setStretch(1, 90)
		mainLayout.setContentsMargins(0, 20, 0, 0)
		return mainLayout


	def handleLoginButtonPress(self):
		self.mainTabs.setCurrentIndex(0)


	def handleRegisterButtonPress(self):
		self.mainTabs.setCurrentIndex(1)


	def getLoginWidget(self):
		self.usernameInput = QLineEdit(self.sessionData.get('username', ''))
		self.usernameInput.setPlaceholderText('Username')
		self.usernameInput.setAlignment(Qt.AlignCenter)
		self.usernameInput.setFixedWidth(400)
		self.usernameInput.setObjectName('loginInput')
		self.usernameInput.setMaxLength(50)

		self.passwordInput = QLineEdit(self.sessionData.get('password', ''))
		self.passwordInput.setPlaceholderText('Password')
		self.passwordInput.setAlignment(Qt.AlignCenter)
		self.passwordInput.setEchoMode(QLineEdit.Password)
		self.passwordInput.setFixedWidth(400)
		self.passwordInput.setObjectName('loginInput')
		self.passwordInput.setMaxLength(50)

		self.submitButton = QPushButton('Login')
		self.submitButton.setFixedSize(250, 40)
		self.submitButton.setObjectName('loginButton')
		self.submitButton.clicked.connect(self.handleLoginSubmitPress)
		self.submitButtonContainer = QWidget()
		self.submitButtonContainerLayout = QHBoxLayout(self.submitButtonContainer)
		self.submitButtonContainerLayout.addWidget(self.submitButton)
		self.submitButtonContainerLayout.setAlignment(Qt.AlignCenter)
		self.submitButtonContainerLayout.setContentsMargins(0, 0, 0, 0)

		self.bottomWidget = QWidget()
		self.bottomLayout = QHBoxLayout(self.bottomWidget)
		self.namText = QLabel('New User?')
		self.namText.setStyleSheet('color:#ffffff;')
		self.registerButton = QPushButton('Register Here')
		self.registerButton.setMinimumHeight(40)
		self.registerButton.clicked.connect(self.handleRegisterButtonPress)
		self.registerButton.setStyleSheet('border : 0px;font-size:18px;')
		self.bottomLayout.addWidget(self.namText)
		self.bottomLayout.addWidget(self.registerButton)
		self.bottomLayout.setAlignment(Qt.AlignCenter)
		self.bottomLayout.setContentsMargins(0, 0, 0, 0)

		loginWidget = QWidget()
		loginLayout = QVBoxLayout(loginWidget)
		loginLayout.addStretch(3)
		loginLayout.addWidget(self.usernameInput)
		loginLayout.addStretch(1)
		loginLayout.addWidget(self.passwordInput)
		loginLayout.addStretch(3)
		loginLayout.addWidget(self.submitButtonContainer)
		loginLayout.addStretch(1)
		loginLayout.addWidget(self.bottomWidget)
		loginLayout.setAlignment(Qt.AlignCenter)

		return loginWidget


	def handleLoginSubmitPress(self):
		print('Trying to Login...')
		self.submitButton.setEnabled(False)
		self.submitButton.setText('Logging In...')
		self.submitButton.repaint()
		message = {
			"code" : "Login",
			"username" : self.usernameInput.text(),
			"password" : self.passwordInput.text(),
			"listenIP" : self.networkManager.getListenIP(),
			"listenPort" : self.networkManager.getListenPort()
		}

		response = self.networkManager.sendData(message)

		if response == "NULL":
			# Some error occured during login process.
			self.flags[1] = 3
			self.close()
		elif response == "INVALID":
			# Invalid login request
			self.flags[1] = 2
			self.submitButton.setEnabled(True)
			self.submitButton.setText('Login')
			# Pop up a message
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Critical)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('Login Failed! Retry.')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()
		else:
			try:
				print('Logged in!')
				response = eval(response)
				with open('profile.json', "w") as file:
					json.dump(response, file, indent = 4)

			except Exception as error:
				print(error)
				infoBox = QMessageBox()
				infoBox.setIcon(QMessageBox.Critical)
				infoBox.setWindowTitle('Alert')
				infoBox.setText('Server Connection failed! Retry.')
				infoBox.setStandardButtons(QMessageBox.Ok)
				infoBox.exec_()
			finally:
				self.flags[1] = 1
				self.close()


	def getRegisterWidget(self):
		tempLabel = QLabel('Feature available in\nAlpha stage.')
		tempLabel.setObjectName('subsectionHeading')
		tempLabel.setStyleSheet('font-size : 25px;')

		self.backWidget = QWidget()
		self.backLayout = QHBoxLayout(self.backWidget)
		self.loginButton = QPushButton('< Back')
		self.loginButton.setMinimumHeight(40)
		self.loginButton.clicked.connect(self.handleLoginButtonPress)
		self.loginButton.setStyleSheet('border : 0px;font-size:18px;')
		self.backLayout.addWidget(self.loginButton)
		self.backLayout.setAlignment(Qt.AlignCenter)
		self.backLayout.setContentsMargins(0, 0, 0, 0)

		registerWidget = QWidget()
		registerLayout = QVBoxLayout(registerWidget)
		registerLayout.setContentsMargins(0, 0, 0, 0)
		registerLayout.addStretch(1)
		registerLayout.addWidget(tempLabel)
		registerLayout.addStretch(1)
		registerLayout.addWidget(self.backWidget)
		registerLayout.setAlignment(Qt.AlignCenter)
		return registerWidget


	def closeEvent(self, event):
		event.accept()



class Login(LoginWindow):
	def __init__(self, flags, networkManager, sessionData):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		QFontDatabase.addApplicationFont("Resources/Fonts/Adequate.ttf")
		app.setStyleSheet(open('style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		loginApp = LoginWindow(flags, networkManager, sessionData)
		loginApp.show()
		# Execute the app mainloop
		app.exec_()


	
		

	