from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from editableLineEdit import editableLineEdit
from editableTextEdit import editableTextEdit
from prestigeWidget import prestigeWidget

class ProfileWidget(QWidget):
	def __init__(self, userObject):
		super().__init__()
		self.layout = self.getCentralLayout(userObject)
		self.layout.setContentsMargins(5, 5, 5, 5)
		self.setLayout(self.layout)


	def getCentralLayout(self, userObject):
		mainLayout = QVBoxLayout()

		header = self.makeHeader(userObject)
		badge = self.makeBadges(userObject)
		aboutMe = self.makeAboutMe(userObject)

		mainLayout.addWidget(header)
		mainLayout.addWidget(badge)
		mainLayout.addWidget(aboutMe)

		mainLayout.setAlignment(Qt.AlignTop)
		mainLayout.addStretch(1)
		mainLayout.setContentsMargins(0, 0, 0, 0)
		return mainLayout


	def makeBadges(self, userObject):
		overlayWidget = QWidget()
		overlayWidget.setObjectName('contentBox')
		overlayLayout = QHBoxLayout(overlayWidget)
		
		badgesLabelImage = QWidget()
		badgesLabelImage.setObjectName('badgesBox')
		badgesLabelImage.setFixedHeight(170)

		badgeWidget = QWidget()
		badgeLayout = QHBoxLayout(badgeWidget)
		badgeLayout.setContentsMargins(0, 0, 0, 0)

		badgeCount = 0
		for badge in userObject.badges:
			newBadge = QLabel()
			try:
				badgeImage = QPixmap('Resources/Badges/' + badge + '.png')
				newBadge.setPixmap(badgeImage)
			except:
				pass
			else:
				badgeCount += 1
				badgeLayout.addWidget(newBadge)

		while badgeCount < 6:
			badgeCount += 1
			newBadge = QLabel()
			try:
				badgeImage = QPixmap('Resources/Badges/Empty.png')
				newBadge.setPixmap(badgeImage)
				badgeLayout.addWidget(newBadge)
			except:
				pass

		overlayLayout.addWidget(badgesLabelImage)
		overlayLayout.addWidget(badgeWidget)
		overlayLayout.setStretch(0, 5)
		overlayLayout.setStretch(1, 95)
		overlayLayout.setContentsMargins(0, 0, 0, 0)

		return overlayWidget


	def makeAboutMe(self, userObject):
		overlayWidget = QWidget()
		overlayWidget.setObjectName('contentBox')
		overlayLayout = QHBoxLayout(overlayWidget)

		aboutImage = QWidget()
		aboutImage.setObjectName('aboutBox')
		aboutImage.setFixedHeight(170)

		aboutMeContent = QLabel(userObject.aboutMe)
		aboutMeContent.setAlignment(Qt.AlignTop)
		aboutMeContent.setObjectName('h4')

		overlayLayout.addWidget(aboutImage)
		overlayLayout.addWidget(aboutMeContent)
		overlayLayout.setStretch(0, 5)
		overlayLayout.setStretch(1, 95)
		overlayLayout.setContentsMargins(0, 0, 0, 0)
		overlayLayout.setAlignment(Qt.AlignTop)
		return overlayWidget


	def makeHeader(self, userObject):
		headerWidget = QWidget()
		headerWidget.setObjectName('headerBox')
		headerLayout = QHBoxLayout(headerWidget)

		nameBox = QWidget()
		nameLayout = QVBoxLayout(nameBox)

		prestigeIcon = prestigeWidget(userObject.userPrestige)
		userAliasLabel = QLabel(userObject.userAlias)
		userAliasLabel.setObjectName('h1')
		userAliasWidget = self.getComboWidget(prestigeIcon, userAliasLabel)

		userMottoLabel = QLabel(userObject.userMotto[:100])
		userMottoLabel.setObjectName('h4')

		repLabel = QLabel('Reputation:')
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