from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from editableLineEdit import editableLineEdit
from prestigeWidget import prestigeWidget

class ProfileWidget(QWidget):
	def __init__(self, userObject):
		super().__init__()
		self.layout = self.getCentralLayout(userObject)
		self.layout.setContentsMargins(10, 10, 10, 10)
		self.setLayout(self.layout)


	def getCentralLayout(self, userObject):
		mainLayout = QVBoxLayout()
		header = self.makeHeader(userObject)

		mainLayout.addWidget(header)
		mainLayout.setAlignment(Qt.AlignTop)
		return mainLayout


	def makeHeader(self, userObject):
		headerWidget = QWidget()
		headerWidget.setObjectName('contentBox')
		headerLayout = QHBoxLayout(headerWidget)

		nameBox = QWidget()
		nameLayout = QVBoxLayout(nameBox)

		prestigeIcon = prestigeWidget(userObject.userPrestige)
		userAliasLabel = QLabel(userObject.userAlias)
		userAliasLabel.setObjectName('h1')
		userAliasWidget = self.getComboWidget(prestigeIcon, userAliasLabel)

		userMottoLabel = editableLineEdit(userObject.userMotto[:100])

		repLabel = QLabel('Rep:')
		repLabel.setObjectName('repLabel')
		repContent = QLabel(userObject.userRep)
		repContent.setObjectName('repContent')
		repWidget = self.getComboWidget(repLabel, repContent)

		memberSinceLabel = QLabel('Member Since:')
		memberSinceLabel.setObjectName('memberSinceLabel')
		memberSinceContent = QLabel(userObject.memberSince)
		memberSinceContent.setObjectName('memberSinceContent')
		memberSinceWidget = self.getComboWidget(memberSinceLabel, memberSinceContent)

		nameLayout.addWidget(userAliasWidget)
		nameLayout.addWidget(userMottoLabel)
		nameLayout.addWidget(repWidget)
		nameLayout.addWidget(memberSinceWidget)
		nameLayout.setAlignment(userAliasWidget, Qt.AlignTop)
		nameLayout.setAlignment(userMottoLabel, Qt.AlignTop)
		nameLayout.setAlignment(repWidget, Qt.AlignBottom)
		nameLayout.setAlignment(memberSinceWidget, Qt.AlignBottom)

		avatarBox = QLabel()
		avatarBox.setObjectName('avatarBox')
		avatarImage = userObject.userAvatar + '.png'
		avatar = QPixmap("Resources/Avatars/" + avatarImage);
		scaled = avatar.scaled (180, 180, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		avatarBox.setPixmap(scaled)
		
		headerLayout.addWidget(nameBox)
		headerLayout.addWidget(avatarBox)
		headerLayout.setAlignment(nameBox, Qt.AlignLeft)
		headerLayout.setAlignment(avatarBox, Qt.AlignRight)

		return headerWidget

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