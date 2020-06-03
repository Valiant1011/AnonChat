from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class FriendList(QWidget):
	def __init__(self, userObject):
		super().__init__()
		self.userObject = userObject

		self.emptyLayout = self.getEmptyLayout()
		self.friendsLayout = self.getFriendListLayout()

		if self.userObject.getFriendCount() == 0:
			mainLayout = self.emptyLayout
		else:
			mainLayout = self.friendsLayout

		self.setLayout(mainLayout)


	def getEmptyLayout(self):
		noFriendsTopLabel = QLabel('Your friend list is Empty!')
		noFriendsTopLabel.setAlignment(Qt.AlignCenter)
		noFriendsTopLabel.setObjectName('sidebarText')

		noFriendsImage = QLabel()
		noFriendsImage.setAlignment(Qt.AlignCenter)
		pixmap = QPixmap("Resources/Assets/emptyList.png")
		noFriendsImage.setPixmap(pixmap)

		noFriendsBottomLabel = QLabel('To add new friends, connect to\nrandom chat or look up your\nfriend\'s username in the Search field!')
		noFriendsBottomLabel.setAlignment(Qt.AlignCenter)
		noFriendsBottomLabel.setObjectName('sidebarText')

		layout = QVBoxLayout()
		layout.addStretch(2)
		layout.addWidget(noFriendsTopLabel)
		layout.addStretch(3)
		layout.addWidget(noFriendsImage)
		layout.addStretch(3)
		layout.addWidget(noFriendsBottomLabel)
		layout.addStretch(1)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setAlignment(Qt.AlignCenter)

		return layout

	def getFriendListLayout(self):
		widgetList = [None] * self.userObject.getFriendCount()
		friendList = self.userObject.getFriends()

		for i in range(len(friendList)):
			# friendList[i] is a dict type object with entities
			# ID
			# Alias
			# Avatar
			
			avatar = friendList[i].get('Avatar', 'Default.png')
			friendAvatar = QWidget()
			friendAvatar.setFixedSize(64, 64)
			style = "border-image : url('Resources/Avatars/" + avatar + "') center center;"
			friendAvatar.setStyleSheet(style)

			friendName = QLabel(friendList[i].get('Alias'))
			friendName.setObjectName('sidebarName')
			friendName.setAlignment(Qt.AlignTop)

			status = friendList[i].get('Status', 'Offline')
			statusLabel = QLabel(status)
			statusLabel.setAlignment(Qt.AlignRight)
			if status == 'Online':
				statusLabel.setObjectName('online')
			else:
				statusLabel.setObjectName('offline')

			containerWidget = QWidget()
			containerLayout = QVBoxLayout(containerWidget)
			containerLayout.addWidget(friendName)
			containerLayout.addWidget(statusLabel)

			friendWidget = QWidget()
			friendWidget.setObjectName('friendWidget')
			friendWidgetLayout = QHBoxLayout(friendWidget)
			friendWidgetLayout.addWidget(friendAvatar)
			friendWidgetLayout.addWidget(containerWidget)
			friendWidgetLayout.setStretch(0, 10)
			friendWidgetLayout.setStretch(1, 90)
			friendWidget.setStyleSheet("QWidget#friendWidget{background-color : rgba(200, 200, 200, 5);}")

			widgetList[i] = friendWidget

		primaryWidget = QWidget()
		primaryLayout = QVBoxLayout(primaryWidget)
		primaryLayout.setAlignment(Qt.AlignTop)
		for i in range(len(widgetList)):
			primaryLayout.addWidget(widgetList[i])

		friendScroller = QScrollArea()
		friendScroller.setWidgetResizable(True)
		friendScroller.setWidget(primaryWidget)

		containerLayout = QVBoxLayout()
		containerLayout.setContentsMargins(0, 0, 0, 0)
		containerLayout.addWidget(friendScroller)
			
		return containerLayout
