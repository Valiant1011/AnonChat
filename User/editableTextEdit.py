from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class editableTextEdit(QWidget):
	def __init__(self, text = '', objectName = ''):
		super().__init__()
		self.flag = 0
		self.state = 'static'
		self.objectName = objectName
		self.mainContent = QPlainTextEdit(text)

		self.mainContent.setObjectName('editableTextEdit')
		self.mainContent.setReadOnly(True)

		self.editButton = QPushButton('Edit')
		self.editButton.setFixedSize(40, 22)
		self.editButton.clicked.connect(self.handleEditTrigger)
		self.editButton.setObjectName('editButton')
		self.editButton.setToolTip('Edit ' + self.objectName)

		self.contentLayout = QVBoxLayout()
		self.contentLayout.addWidget(self.mainContent)
		self.contentLayout.addWidget(self.editButton)
		self.contentLayout.setAlignment(Qt.AlignTop)
		self.contentLayout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.contentLayout)
		self.setState(self.state)


	def handleEditTrigger(self):
		if self.flag == 0:
			# Edit Mode
			self.flag = 1
			self.mainContent.setReadOnly(False)
			self.editButton.setToolTip('Save ' + self.objectName)
			self.editButton.setText('Save')
			self.mainContent.update()
			self.mainContent.setFocus()

		elif self.flag == 1:
			# Save Mode
			self.flag = 0
			self.mainContent.setReadOnly(True)
			self.editButton.setToolTip('Edit ' + self.objectName)
			self.editButton.setText('Edit')
			self.mainContent.update()


	def setState(self, state):
		if state == 'static':
			self.editButton.setVisible(False)
		elif state == 'edit':
			self.editButton.setVisible(True)


	def getText(self):
		return self.mainContent.toPlainText()