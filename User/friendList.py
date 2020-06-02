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
		return QVBoxLayout()
