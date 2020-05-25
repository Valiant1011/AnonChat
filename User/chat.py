from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class ChatWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = self.getCentralLayout()
		self.layout.setContentsMargins(10, 0, 0, 0)
		self.setLayout(self.layout)

	def getCentralLayout(self):
		mainLayout = QVBoxLayout()

		chatName = QLabel(' Chat')
		chatName.setObjectName('h1')

		mainLayout.addWidget(chatName)
		return mainLayout