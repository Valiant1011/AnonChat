from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt
from chatWidget import ChatWidget
import time

class Chat(QWidget):
	def __init__(self, state = 'search', talkingTo = None, talkingToID = '__SEARCH__'):
		super().__init__()
		self.state = state
		self.talkingTo = talkingTo
		self.talkingToID = talkingToID

		# Stores backup of chat widgets
		self.chatsLoaded = {}    # Map ID to chatTabs index

		self.loadingWidget = self.loadingState()
		self.chatTabs = QTabWidget()
		self.chatTabs.addTab(self.loadingWidget, '')
		self.chatTabsCount = 0		# (Number of tabs - 1) because of 0 based indexing

		self.mainLayout = QVBoxLayout(self)	
		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.addWidget(self.chatTabs)


	def setState(self, state = 'search', receiver = None, ID = '__SEARCH__'):
		if state == 'search':
			self.chatTabs.setCurrentIndex(0)
			return

		# Check if this chat has been loaded earlier
		if self.chatsLoaded.get(ID, -1) != -1:
			self.chatTabs.setCurrentIndex(self.chatsLoaded[ID])
		else:
			newChatWidget = ChatWidget(ID, receiver)
			self.chatTabs.addTab(newChatWidget, '')
			self.chatTabsCount += 1
			self.chatsLoaded[ID] = self.chatTabsCount
			self.chatTabs.setCurrentIndex(self.chatTabsCount)


	def loadingState(self):
		loadingAnimation = QLabel()
		loadingAnimation.setStyleSheet("border:0px;")
		loadingAnimation.setAlignment(Qt.AlignCenter)
		loadingAnimation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		anim = QMovie('Resources/Assets/loading.webp')
		loadingAnimation.setMovie(anim)
		anim.start()

		loadingAnimContainer = QWidget()
		loadingAnimContainerLayout = QVBoxLayout(loadingAnimContainer)
		loadingAnimContainerLayout.addWidget(loadingAnimation)
		loadingAnimContainerLayout.setContentsMargins(0, 0, 0, 0)

		loadingText = QLabel('Searching...')
		loadingText.setObjectName('subsectionHeading')
		loadingText.setAlignment(Qt.AlignCenter)

		containerLayout = QVBoxLayout()
		containerLayout.addWidget(loadingAnimContainer)
		containerLayout.addWidget(loadingText)
		containerLayout.setAlignment(Qt.AlignCenter)
		containerLayout.setContentsMargins(0, 0, 0, 0)
		containerLayout.setStretch(0, 70)
		containerLayout.setStretch(1, 30)

		subWidget = QWidget()
		subWidget.setLayout(containerLayout)
		return subWidget