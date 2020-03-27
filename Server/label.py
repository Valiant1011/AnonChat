from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class label():
	def get_widget(text = '', sender = '', time = ''):
		widget = QWidget()
		layout = QVBoxLayout(widget)

		if sender != '':
			label_sender = QLabel(sender)
			label_sender.setObjectName('sender')
			layout.addWidget(label_sender)

		label_text = QLabel(text)
		label_text.setObjectName('text')
		layout.addWidget(label_text)

		label_time = QLabel(time)
		label_time.setObjectName('time')
		layout.addWidget(label_time)

		layout.setAlignment(label_time, Qt.AlignRight)
		
		widget.adjustSize()

		return widget
