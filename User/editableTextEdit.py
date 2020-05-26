from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class editableTextEdit(QWidget):
	def __init__(self, text = '', title = ''):
		super().__init__()
		self.flag = 0

		self.title = QLabel(title)
		self.title.setObjectName('h4')

		self.mainContent = QTextEdit(text)
		self.mainContent.setObjectName('editableTextEdit')
		self.mainContent.setReadOnly(True)

		self.editButton = QPushButton('Edit')
		self.editButton.setFixedSize(40, 22)
		self.editButton.clicked.connect(self.handleEditTrigger)
		self.editButton.setObjectName('editButton')
		self.editButton.setToolTip('Edit About Section')

		self.contentLayout = QVBoxLayout()
		self.contentLayout.addWidget(self.title)
		self.contentLayout.addWidget(self.mainContent)
		self.contentLayout.addWidget(self.editButton)
		self.contentLayout.setAlignment(Qt.AlignTop)
		self.contentLayout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.contentLayout)
		self.setFixedHeight(200)


	def handleEditTrigger(self):
		if self.flag == 0:
			# Edit Mode
			self.flag = 1
			self.mainContent.setReadOnly(False)
			self.editButton.setToolTip('Save About Section')
			self.editButton.setText('Save')
			self.mainContent.update()
			self.mainContent.setFocus()

		elif self.flag == 1:
			# Save Mode
			self.flag = 0
			self.mainContent.setReadOnly(True)
			self.editButton.setToolTip('Edit About Section')
			self.editButton.setText('Edit')
			self.mainContent.update()
			
