from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

import sys, json 

def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler) 

class LoginWindow(QMainWindow):
	def __init__(self, flags, networkManager, sessionData, taskQueue):
		super().__init__()
		self.flags = flags
		self.networkManager = networkManager
		self.sessionData = sessionData
		self.taskQueue = taskQueue

		self.setWindowIcon(QIcon('Resources/Assets/logo.png'))
		self.setWindowTitle('AnonChat [ LOGIN ]')
		self.setObjectName('loginWindow')

		loginWidget = QWidget()
		loginLayout = self.getMainLayout()
		loginWidget.setLayout(loginLayout)
		self.setCentralWidget(loginWidget)
		self.setFixedSize(600, 700)
		self.setGeometry(600, 200, 600, 700) 

		# Timer to get Server data
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateData)
		self.timer.start(1000)


	def updateData(self):
		try:
			data = self.taskQueue.get(block = False, timeout = 0.5)
			# data is guarenteed to be a dict type object.
		except Exception as e:
			if "Empty" in str(e) or str(e) == "":
				pass
			else:
				print('Error: ', e)


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

		self.passwordInput = QLineEdit()
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
		self.registerNowButton = QPushButton('Register Here')
		self.registerNowButton.setMinimumHeight(40)
		self.registerNowButton.clicked.connect(self.handleRegisterButtonPress)
		self.registerNowButton.setStyleSheet('border : 0px;font-size:18px;')
		self.bottomLayout.addWidget(self.namText)
		self.bottomLayout.addWidget(self.registerNowButton)
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
			"userID" : self.sessionData.get("userID", -1),
			"userName" : self.usernameInput.text(),
			"password" : self.passwordInput.text()
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
		elif response == 'ERROR':
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Critical)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('Server Connection failed! Please Retry.')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()
			self.flags[1] = 3
			self.close()
		else:
			try:
				print('Logged in!')
				response = eval(response)
				userID = response.get('userID')
				self.updateSessionInfo(self.usernameInput.text(), userID)
				with open('profile.json', "w") as file:
					json.dump(response, file, indent = 4)

			except Exception as error:
				print(error)
				infoBox = QMessageBox()
				infoBox.setIcon(QMessageBox.Critical)
				infoBox.setWindowTitle('Alert')
				infoBox.setText('Server Connection failed! Please Retry.')
				infoBox.setStandardButtons(QMessageBox.Ok)
				infoBox.exec_()
			finally:
				self.flags[1] = 1
				self.close()


	def getRegisterWidget(self):
		self.registerUsernameInput = QLineEdit()
		self.registerUsernameInput.setPlaceholderText('Create a unique Alias')
		self.registerUsernameInput.setAlignment(Qt.AlignCenter)
		self.registerUsernameInput.setFixedWidth(400)
		self.registerUsernameInput.setObjectName('loginInput')
		self.registerUsernameInput.setMaxLength(50)

		self.registerPasswordInput = QLineEdit()
		self.registerPasswordInput.setPlaceholderText('Choose a Password')
		self.registerPasswordInput.setAlignment(Qt.AlignCenter)
		self.registerPasswordInput.setEchoMode(QLineEdit.Password)
		self.registerPasswordInput.setFixedWidth(400)
		self.registerPasswordInput.setObjectName('loginInput')
		self.registerPasswordInput.setMaxLength(50)

		self.registerPasswordInputConfirm = QLineEdit()
		self.registerPasswordInputConfirm.setPlaceholderText('Confirm Password')
		self.registerPasswordInputConfirm.setAlignment(Qt.AlignCenter)
		self.registerPasswordInputConfirm.setEchoMode(QLineEdit.Password)
		self.registerPasswordInputConfirm.setFixedWidth(400)
		self.registerPasswordInputConfirm.setObjectName('loginInput')
		self.registerPasswordInputConfirm.setMaxLength(50)

		self.registerButton = QPushButton('Register')
		self.registerButton.setFixedSize(250, 40)
		self.registerButton.setObjectName('loginButton')
		self.registerButton.clicked.connect(self.handleRegisterSubmitPress)
		self.registerButtonContainer = QWidget()
		self.registerButtonContainerLayout = QHBoxLayout(self.registerButtonContainer)
		self.registerButtonContainerLayout.addWidget(self.registerButton)
		self.registerButtonContainerLayout.setAlignment(Qt.AlignCenter)
		self.registerButtonContainerLayout.setContentsMargins(0, 0, 0, 0)

		self.backWidget = QWidget()
		self.backLayout = QHBoxLayout(self.backWidget)
		self.backButton = QPushButton('< Back')
		self.backButton.setMinimumHeight(40)
		self.backButton.clicked.connect(self.handleLoginButtonPress)
		self.backButton.setStyleSheet('border : 0px;font-size:18px;')
		self.backLayout.addWidget(self.backButton)
		self.backLayout.setAlignment(Qt.AlignCenter)
		self.backLayout.setContentsMargins(0, 0, 0, 0)

		uselessInput = QLineEdit()
		uselessInput.setFixedSize(0, 0)

		registerWidget = QWidget()
		registerLayout = QVBoxLayout(registerWidget)
		registerLayout.setContentsMargins(0, 0, 0, 0)
		registerLayout.addStretch(3)
		registerLayout.addWidget(uselessInput)
		registerLayout.addWidget(self.registerUsernameInput)
		registerLayout.addStretch(1)
		registerLayout.addWidget(self.registerPasswordInput)
		registerLayout.addStretch(1)
		registerLayout.addWidget(self.registerPasswordInputConfirm)
		registerLayout.addStretch(3)
		registerLayout.addWidget(self.registerButtonContainer)
		registerLayout.addStretch(1)
		registerLayout.addWidget(self.backWidget)
		registerLayout.setAlignment(Qt.AlignCenter)
		return registerWidget


	def handleRegisterSubmitPress(self):
		# Some checks on user input:
		if len(self.registerUsernameInput.text()) == 0:
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Information)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('Alias field can not be empty!')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()
			return
			
		if len(self.registerPasswordInput.text()) == 0:
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Information)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('Password field can not be empty!')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()
			return

		if not self.registerPasswordInput.text() == self.registerPasswordInputConfirm.text():
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Information)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('Confirmed password does not match. Please Retry!')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()
			return

		print('Trying to Register...')

		self.registerButton.setEnabled(False)
		self.registerButton.setText('On it!')
		self.registerButton.repaint()

		message = {
			"code" : "Register",
			"userID" : "NULL",
			"userName" : self.registerUsernameInput.text(),
			"password" : self.registerPasswordInput.text()
		}

		response = self.networkManager.sendData(message)

		if response == "NULL" or response == "INVALID":
			# Some error occured during login process.
			# Here, INVALID is only possible if the client sent garbage data to the Server.
			self.flags[1] = 3
			self.close()

		elif response == "ERROR":
			# Network error
			self.flags[1] = 2
			self.registerButton.setEnabled(True)
			self.registerButton.setText('Register')
			# Pop up a message
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Information)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('A Network error occured during processing your request. Please check your Internet connection.')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()

		elif response == "UsernameTaken":
			infoBox = QMessageBox()
			infoBox.setIcon(QMessageBox.Information)
			infoBox.setWindowTitle('Alert')
			infoBox.setText('Sorry, this Username is already taken. Please try another Username.')
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.exec_()
			# Re enable the Register button
			self.registerButton.setEnabled(True)
			self.registerButton.setText('Register')
			self.registerButton.repaint()

		else:
			try:
				print('Registered and Logged in!')
				response = eval(response)
				userID = response.get('userID')
				self.updateSessionInfo(self.registerUsernameInput.text(), userID)
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


	def updateSessionInfo(self, userName, userID):
		filename = 'session.json'
		with open(filename, 'r') as file:
			sessionData = json.load(file)

		sessionData['username'] = userName
		sessionData['userID'] = userID
		with open(filename, 'w') as file:
			json.dump(sessionData, file, indent = 4)


	def closeEvent(self, event):
		event.accept()



class Login(LoginWindow):
	def __init__(self, flags, networkManager, sessionData, taskQueue):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		QFontDatabase.addApplicationFont("Resources/Fonts/Adequate.ttf")
		app.setStyleSheet(open('style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		loginApp = LoginWindow(flags, networkManager, sessionData, taskQueue)
		loginApp.show()
		# Execute the app mainloop
		app.exec_()


	
		

	