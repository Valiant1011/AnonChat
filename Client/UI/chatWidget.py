from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt
import time

class ChatWidget(QWidget):
	def __init__(self, ID, receiver):
		super().__init__()
		self.ID = ID
		self.receiver = receiver
		self.initUI()


	def initUI(self):
		self.receiverLabel = QLabel(self.receiver)
		self.receiverLabel.setObjectName('subsectionHeading')

		self.clearButton = QPushButton('Clear')
		self.clearButton.setFixedHeight(40)
		self.clearButton.clicked.connect(self.clearChat)

		self.topWidget = QWidget()
		self.topLayout = QHBoxLayout(self.topWidget)
		self.topLayout.addWidget(self.receiverLabel)
		self.topLayout.addWidget(self.clearButton)
		self.topLayout.setContentsMargins(0, 0, 0, 0)
		self.topLayout.setStretch(0, 90)
		self.topLayout.setStretch(1, 10)

		self.chatWidget = QWidget()
		self.chatWidget.setObjectName('chatWidget')
		self.chatLayout = QVBoxLayout(self.chatWidget)
		self.chatLayout.setAlignment(Qt.AlignBottom)

		self.chatScroller = QScrollArea()
		self.chatScroller.setWidgetResizable(True)
		self.chatScroller.setWidget(self.chatWidget)
		self.chatScroller.verticalScrollBar().rangeChanged.connect(
			self.moveScrollBarToBottom
		)

		self.inputBox = QPlainTextEdit()
		self.inputBox.setObjectName('messageField')
		self.inputBox.setPlaceholderText('What\'s on your mind?')
		self.inputBox.setMinimumHeight(40)
		
		self.sendButton = QPushButton('Send')
		self.sendButton.setFixedHeight(40)
		self.sendButton.clicked.connect(self.userInputHandler)
		self.sendButton.setDefault(True)

		self.inputAreaWidget = QWidget()
		self.inputAreaLayout = QHBoxLayout(self.inputAreaWidget)
		self.inputAreaLayout.addWidget(self.inputBox)
		self.inputAreaLayout.addWidget(self.sendButton)
		self.inputAreaLayout.setContentsMargins(0, 10, 0, 10)
		self.inputAreaLayout.setStretch(0, 90)
		self.inputAreaLayout.setStretch(1, 10)

		self.primaryLayout = QVBoxLayout()
		self.primaryLayout.addWidget(self.topWidget)
		self.primaryLayout.addWidget(self.chatScroller)
		self.primaryLayout.addWidget(self.inputAreaWidget)
		self.primaryLayout.setStretch(0, 5)
		self.primaryLayout.setStretch(1, 85)
		self.primaryLayout.setStretch(2, 10)
		
		self.setLayout(self.primaryLayout)


	def userInputHandler(self):
		userInput = self.inputBox.toPlainText()
		if userInput == '':
			return

		self.inputBox.clear()
		
		# userInput = self.processText(userInput)
		currentTime = time.strftime('%H:%M:%S', time.localtime())
		userInputWidget = self.getChatLabel(userInput, '', currentTime)
		userInputWidget.setObjectName('userInput')

		self.chatLayout.addWidget(userInputWidget)
		self.chatLayout.setAlignment(userInputWidget, Qt.AlignRight)
		self.chatLayout.addSpacing(10)


	def processNewMessage(self, sender = '', text = ''):
		# text = self.processText(text)
		currentTime = time.strftime('%H:%M:%S', time.localtime())
		userInputWidget = self.getChatLabel(text, sender, currentTime)
		userInputWidget.setObjectName('response')
		self.chatLayout.addWidget(userInputWidget)
		self.chatLayout.setAlignment(userInputWidget, Qt.AlignLeft)
		self.chatLayout.addSpacing(10)
		

	def clearChat(self):
		while self.chatLayout.count():
			child = self.chatLayout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()


	def getChatLabel(self, text = '', sender = '', time = ''):
		widget = QWidget()
		layout = QVBoxLayout(widget)
		if sender != '':
			senderLabel = QLabel(sender)
			senderLabel.setObjectName('chatSender')
			layout.addWidget(senderLabel)

		messageLabel = QLabel(text)
		messageLabel.setObjectName('chatMessage')
		layout.addWidget(messageLabel)
		timeLabel = QLabel(time)
		timeLabel.setObjectName('chatTime')
		layout.addWidget(timeLabel)
		layout.setAlignment(timeLabel, Qt.AlignRight)
		widget.adjustSize()
		return widget


	def moveScrollBarToBottom(self, min, max):
		self.chatScroller.verticalScrollBar().setValue(max)
		return