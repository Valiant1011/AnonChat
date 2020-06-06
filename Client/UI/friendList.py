from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from UI.FriendChatLabel import friendChatLabel

class changeSignal(QObject):
	# This signal acepts a string, ie, the ID of the label that is clicked
	chatChanged = pyqtSignal(['QString'])

class FriendList(QWidget):
	def __init__(self, userObject):
		super().__init__()
		self.userObject = userObject
		# Signal to send clcik information to its master(client.py)
		self.chatChangeSignal = changeSignal()
		# This dictionary will return friend index in its list from the friend ID
		self.getIndexFromID = {}
		self.friendList = self.userObject.getFriends()
		self.mapIDtoIndex()

		self.emptyLayout = self.getEmptyLayout()
		self.friendsLayout = self.getFriendListLayout()

		if self.userObject.getFriendCount() == 0:
			mainLayout = self.emptyLayout
		else:
			mainLayout = self.friendsLayout

		self.setLayout(mainLayout)


	def mapIDtoIndex(self):
		for i in range(len(self.friendList)):
			self.getIndexFromID[self.friendList[i].get("ID")] = i


	def getInfoFromID(self, ID):
		index = self.getIndexFromID[ID]
		return self.friendList[index]


	def getFriendListLayout(self):
		widgetList = [None] * self.userObject.getFriendCount()

		for i in range(len(self.friendList)):
			# friendList[i] is a dict type object with entities
			# ID
			# Alias
			# Avatar
			fID = self.friendList[i].get('ID', None)
			fName = self.friendList[i].get('Alias', 'Ghost')
			status = self.friendList[i].get('Status', 'Offline')
			avatar = self.friendList[i].get('Avatar', 'Default.png')
			
			try:
				friendWidget = friendChatLabel(fID, fName, status, avatar)
				friendWidget.pressSignal.clicked.connect(self.chatLabelClicked)
				widgetList[i] = friendWidget
			except Exception as error:
				print(error)

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


	def chatLabelClicked(self, ID):
		# Gives us the ID of the chat label that is clicked.
		# Signals and slots magic!!!
		# Pass this signal to the main UI
		self.chatChangeSignal.chatChanged.emit(ID)
		


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


	def addFriend(self, friendObject):
		pass
