from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from imageDisplay import imageDisplay

class editProfileWindow(QMainWindow):
	def __init__(self, userObject, editFlag):
		super().__init__()
		self.changesMade = False
		self.userObject = userObject
		self.editFlag = editFlag
		# Set app icon
		self.setWindowIcon(QIcon('Resources/Assets/logo.png'))
		# Set window title
		self.setWindowTitle('Edit Profile')
		self.setGeometry(300, 200, 1366, 768) 
		self.setMinimumWidth(1066)
		self.setMinimumHeight(600)
		profileBG = self.userObject.getProfileBG()
		style = "QMainWindow{border-image : url('Resources/BG/" + profileBG + "');}"
		self.setStyleSheet(style)

		self.vScrollWidget = QWidget()
		self.getMainLayout()
		self.vScrollWidget.setLayout(self.mainLayout)
		self.vScrollWidget.setObjectName('editProfile')
		self.vScroller = QScrollArea()
		self.vScroller.setWidgetResizable(True)
		self.vScroller.setWidget(self.vScrollWidget)

		saveButton = QPushButton('Save')
		saveButton.setFixedSize(80, 40)
		saveButton.clicked.connect(self.saveButtonClicked)
		saveButtonContainer = QWidget()
		saveButtonContainer.setObjectName('saveCont')
		saveButtonContainer.setStyleSheet("QWidget#saveCont{background-color : rgba(12, 12, 12, 180);}")
		saveButtonLayout = QHBoxLayout(saveButtonContainer)
		saveButtonLayout.addWidget(saveButton)
		saveButtonLayout.setAlignment(Qt.AlignCenter)

		containerWidget = QWidget()
		containerLayout = QVBoxLayout(containerWidget)
		containerLayout.addWidget(self.vScroller)
		containerLayout.addWidget(saveButtonContainer)
		containerLayout.setContentsMargins(0, 0, 0, 0)
		containerLayout.setSpacing(0)
		containerLayout.setStretch(0, 95)
		containerLayout.setStretch(1, 5)

		self.setCentralWidget(containerWidget)


	def getMainLayout(self):
		# User Motto settings
		self.userMottoLabel = QLabel('Motto')
		self.userMottoLabel.setAlignment(Qt.AlignCenter)
		self.userMottoLabel.setObjectName('subsectionHeading')
		self.userMottoContent = QLineEdit(self.userObject.getMotto())
		self.userMottoContent.setObjectName('userMotto')
		self.userMottoContent.setFixedWidth(800)
		self.userMottoContent.setAlignment(Qt.AlignCenter)
		self.mottoWrapper = QWidget()
		self.mottoWrapperLayout = QHBoxLayout(self.mottoWrapper)
		self.mottoWrapperLayout.addWidget(self.userMottoContent)
		self.mottoWrapperLayout.setAlignment(Qt.AlignCenter)

		# AboutMe Section
		self.aboutLabel = QLabel('About Me')
		self.aboutLabel.setAlignment(Qt.AlignCenter)
		self.aboutLabel.setObjectName('subsectionHeading')
		self.aboutContent = QPlainTextEdit(self.userObject.getAboutMe())
		# self.aboutContent.setObjectName('about')
		self.aboutContent.setFixedWidth(800)
		self.aboutContent.setMinimumHeight(300)
		self.aboutContent.setObjectName('editPlainText')
		self.aboutContent.setStyleSheet("background-color : rgba(30, 28, 36, 70);")
		self.aboutWrapper = QWidget()
		self.aboutWrapperLayout = QHBoxLayout(self.aboutWrapper)
		self.aboutWrapperLayout.addWidget(self.aboutContent)
		self.aboutWrapperLayout.setAlignment(Qt.AlignCenter)

		# Profile Picture settings
		self.avatarHeading = QLabel('Avatar')
		self.avatarHeading.setAlignment(Qt.AlignCenter)
		self.avatarHeading.setObjectName('subsectionHeading')
		currentAvatar = self.userObject.getAvatar()
		availableAvatars = self.userObject.getAvailableAvatars()
		for i in range(len(availableAvatars)):
			if availableAvatars[i] == currentAvatar:
				currentAvatar = i
				break
		self.avatarScroller = imageDisplay(
			'Resources/Avatars/', 
			availableAvatars,
			180, 
			180,
			i
		)

		# Profile Frame settings
		self.frameHeading = QLabel('Frame')
		self.frameHeading.setAlignment(Qt.AlignCenter)
		self.frameHeading.setObjectName('subsectionHeading')
		currentFrame = self.userObject.getAvatarFrame()
		availableFrames = self.userObject.getAvailableFrames()
		for i in range(len(availableFrames)):
			if availableFrames[i] == currentFrame:
				currentFrame = i
				break
		self.frameScroller = imageDisplay(
			'Resources/Frames/', 
			availableFrames,
			210,
			210,
			i
		)

		# ProfileBG settings
		self.BGHeading = QLabel('Profile Background')
		self.BGHeading.setAlignment(Qt.AlignCenter)
		self.BGHeading.setObjectName('subsectionHeading')
		currentBG = self.userObject.getProfileBG()
		availableBG = self.userObject.getAvailableBG()
		for i in range(len(availableBG)):
			if availableBG[i] == currentBG:
				currentBG = i
				break
		self.BGScroller = imageDisplay(
			'Resources/BG/', 
			availableBG,
			410,
			210,
			i
		)

		

		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(self.userMottoLabel)
		self.mainLayout.addWidget(self.mottoWrapper)

		self.mainLayout.addWidget(self.BGHeading)
		self.mainLayout.addWidget(self.BGScroller)

		self.mainLayout.addWidget(self.avatarHeading)
		self.mainLayout.addWidget(self.avatarScroller)

		self.mainLayout.addWidget(self.frameHeading)
		self.mainLayout.addWidget(self.frameScroller)

		self.mainLayout.addWidget(self.aboutLabel)
		self.mainLayout.addWidget(self.aboutWrapper)

		self.mainLayout.addStretch(1)
		

	def closeEvent(self, event):
		if self.changesMade == True:
			# Raise a dialog box for drop changes confirmation
			pass
		event.accept()


	def saveButtonClicked(self):
		selectedAvatar = self.avatarScroller.getSelected()
		selectedFrame = self.frameScroller.getSelected()
		selectedBG = self.BGScroller.getSelected()
		userMotto = self.userMottoContent.text()
		aboutMe = self.aboutContent.toPlainText()

		self.userObject.setAvatar(selectedAvatar)
		self.userObject.setAvatarFrame(selectedFrame)
		self.userObject.setProfileBG(selectedBG)
		self.userObject.setMotto(userMotto)
		self.userObject.setAboutMe(aboutMe)
		self.userObject.saveChanges()
		# Update interface
		self.editFlag.value = 1
		
		self.close()


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