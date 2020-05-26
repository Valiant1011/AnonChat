from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class editableLineEdit(QWidget):
	def __init__(self, text = ''):
		super().__init__()
		self.flag = 0
		self.mainContent = QLineEdit(text)
		self.mainContent.setObjectName('editableLineEdit')
		self.mainContent.setReadOnly(True)

		self.editButton = QPushButton('Edit')
		self.editButton.setFixedSize(40, 22)
		self.editButton.clicked.connect(self.handleEditTrigger)
		self.editButton.setObjectName('editButton')
		self.editButton.setToolTip('Edit Motto')

		self.contentLayout = QHBoxLayout()
		self.contentLayout.addWidget(self.mainContent)
		self.contentLayout.addWidget(self.editButton)
		self.contentLayout.setAlignment(Qt.AlignLeft)
		self.contentLayout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.contentLayout)


	def handleEditTrigger(self):
		if self.flag == 0:
			# Edit Mode
			self.flag = 1
			self.mainContent.setReadOnly(False)
			self.editButton.setToolTip('Save Motto')
			self.editButton.setText('Save')
			self.mainContent.setStyleSheet("QLineEdit{border-bottom : 1px solid #008080;}")
			self.mainContent.update()
			self.mainContent.setFocus()

		elif self.flag == 1:
			# Save Mode
			self.flag = 0
			self.mainContent.setReadOnly(True)
			self.editButton.setToolTip('Edit Motto')
			self.editButton.setText('Edit')
			self.mainContent.setStyleSheet("QLineEdit{border-bottom : 0px;}")
			self.mainContent.update()
			
