from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class Comment(QWidget):
	def __init__(self, comment):
		super().__init__()
		commentUser = QLabel(comment.get('commentUser', 'Ghost'))
		commentUser.setObjectName('commentUser')
		commentMessage = QLabel(comment.get('commentMessage', 'Boooooo'))
		commentMessage.setObjectName('commentMessage')
		commentDate = comment.get('commentDate', ['25', 'May', '2020'])
		commentDateFormatted = QLabel(commentDate[1] + " " + commentDate[0] + ", " + commentDate[2])
		commentDateFormatted.setObjectName('commentDate')

		userDateHolder = QWidget()
		userDateHolder.setStyleSheet("background: transparent;")
		userDateLayout = QHBoxLayout(userDateHolder)
		userDateLayout.setContentsMargins(0, 0, 0, 0)
		userDateLayout.addWidget(commentUser)
		userDateLayout.addWidget(commentDateFormatted)
		userDateLayout.setAlignment(Qt.AlignLeft)
		

		self.containedComment = QWidget()
		self.containedComment.setObjectName('comment')
		self.containedLayout = QVBoxLayout(self.containedComment)
		self.containedLayout.addWidget(userDateHolder)
		self.containedLayout.addWidget(commentMessage)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.containedComment)
		self.layout.setSizeConstraint(QLayout.SetDefaultConstraint);
		self.setMinimumWidth(900)