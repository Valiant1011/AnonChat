from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from imageDisplay import imageDisplay

class editProfileWindow(QMainWindow):
	def __init__(self, userObject):
		super().__init__()
		self.changesMade = False
		self.userObject = userObject
		# Set app icon
		self.setWindowIcon(QIcon('Resources/Assets/logo.png'))
		# Set window title
		self.setWindowTitle('Edit Profile')
		self.setGeometry(300, 200, 1366, 768) 
		self.setMinimumWidth(1066)
		self.setMinimumHeight(600)
		profileBG = self.userObject.userProfileBG
		style = "QMainWindow{border-image : url('Resources/BG/" + profileBG + "');}"
		self.setStyleSheet(style)

		self.vScrollWidget = QWidget()
		self.getMainLayout()
		self.vScrollWidget.setLayout(self.mainLayout)
		self.vScrollWidget.setObjectName('editProfile')
		self.vScroller = QScrollArea()
		self.vScroller.setWidgetResizable(True)
		self.vScroller.setWidget(self.vScrollWidget)
		self.setCentralWidget(self.vScroller)


	def getMainLayout(self):
		# Profile Picture settings
		avatarHeading = QLabel('Select Avatar')
		avatarHeading.setAlignment(Qt.AlignCenter)
		avatarHeading.setObjectName('subsectionHeading')
		avatarScroller = imageDisplay('Resources/Avatars/', self.userObject.availableAvatars)

		# Profile Frame settings
		frameHeading = QLabel('Select Frame')
		frameHeading.setAlignment(Qt.AlignCenter)
		frameHeading.setObjectName('subsectionHeading')
		frameScroller = imageDisplay('Resources/Frames/', self.userObject.availableFrames)


		saveButton = QPushButton('Save')
		saveButton.setFixedSize(80, 40)
		saveButton.clicked.connect(self.saveButtonClicked)
		saveButtonContainer = QWidget()
		saveButtonLayout = QHBoxLayout(saveButtonContainer)
		saveButtonLayout.addWidget(saveButton)
		saveButtonLayout.setAlignment(Qt.AlignCenter)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(avatarHeading)
		self.mainLayout.addWidget(avatarScroller)
		self.mainLayout.addWidget(frameHeading)
		self.mainLayout.addWidget(frameScroller)

		self.mainLayout.addStretch(1)
		self.mainLayout.addWidget(saveButtonContainer)


		


	def closeEvent(self, event):
		if self.changesMade == True:
			# Raise a dialog box for drop changes confirmation
			pass
		event.accept()


	def saveButtonClicked(self):
		pass


	def getComboWidget(self, widget1, widget2, align = 'H'):
		widget = QWidget()
		if align == 'H':
			layout = QHBoxLayout(widget)
			layout.setAlignment(Qt.AlignLeft)
		else:
			layout = QVBoxLayout(widget)
			layout.setAlignment(Qt.AlignTop)
		layout.addWidget(widget1)
		layout.addWidget(widget2)
		layout.setContentsMargins(0, 0, 0, 0)
		return widget