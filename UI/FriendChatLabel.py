from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt

class clickSignal(QObject):
	# This signal acepts a string, ie, the ID of the label that is clicked
	clicked = pyqtSignal(['QString'])

class friendChatLabel(QWidget):
	def __init__(self, fID, fName, fStatus, fAvatar):
		super().__init__()
		self.setAttribute(Qt.WA_StyledBackground, True)
		self.setObjectName('friendWidget')
		self.pressSignal = clickSignal()

		self.fID = fID

		friendAvatar = QWidget()
		friendAvatar.setFixedSize(64, 64)
		style = "border-image : url('Resources/Avatars/" + fAvatar + "') center center;"
		friendAvatar.setStyleSheet(style)

		friendName = QLabel(fName)
		friendName.setObjectName('sidebarName')
		friendName.setAlignment(Qt.AlignTop)

		self.statusLabel = QLabel(fStatus)
		self.statusLabel.setAlignment(Qt.AlignRight)
		self.setStatus(fStatus)

		containerWidget = QWidget()
		containerLayout = QVBoxLayout(containerWidget)
		containerLayout.addWidget(friendName)
		containerLayout.addWidget(self.statusLabel)

		friendWidgetLayout = QHBoxLayout(self)
		friendWidgetLayout.addWidget(friendAvatar)
		friendWidgetLayout.addWidget(containerWidget)
		friendWidgetLayout.setStretch(0, 10)
		friendWidgetLayout.setStretch(1, 90)


	def setStatus(self, status):
		if status == 'Online':
			self.statusLabel.setObjectName('online')
		else:
			self.statusLabel.setObjectName('offline')
		self.update()


	def mousePressEvent(self, event):
		# On mouse click, emit the clicked signal with ID of the label that is clicked
		if event.button() == Qt.LeftButton:
			self.pressSignal.clicked.emit(self.fID)