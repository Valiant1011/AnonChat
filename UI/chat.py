from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt

class ChatWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.state = 'chat'
		try:
			self.setState(self.state, 'Neo')
		except Exception as error:
			print(error)


	def setState(self, state = 'search', reciever = ''):
		self.state = state
		if state == 'search':
			self.layout = self.loadingState()
		else:
			self.layout = self.chatState(reciever)

		self.setLayout(self.layout)
		self.repaint()


	def chatState(self, reciever):
		recieverLabel = QLabel(reciever)
		recieverLabel.setObjectName('subsectionHeading')

		chatWidget = QWidget()
		chatLayout = QVBoxLayout(chatWidget)
		chatScroller = QScrollArea()
		chatScroller.setWidgetResizable(True)
		chatScroller.setWidget(chatWidget)

		inputBox = QPlainTextEdit()
		inputBox.setObjectName('messageField')
		inputBox.setPlaceholderText('What\'s on your mind?')
		inputBox.setMinimumHeight(40)
		sendButton = QPushButton('Send')
		sendButton.setFixedHeight(40)

		inputAreaWidget = QWidget()
		inputAreaLayout = QHBoxLayout(inputAreaWidget)
		inputAreaLayout.addWidget(inputBox)
		inputAreaLayout.addWidget(sendButton)
		inputAreaLayout.setStretch(0, 90)
		inputAreaLayout.setStretch(1, 10)

		primaryLayout = QVBoxLayout()
		primaryLayout.addWidget(recieverLabel)
		primaryLayout.addWidget(chatScroller)
		primaryLayout.addWidget(inputAreaWidget)
		primaryLayout.setStretch(0, 5)
		primaryLayout.setStretch(1, 85)
		primaryLayout.setStretch(2, 10)
		return primaryLayout


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

		return containerLayout


	