from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

import sys

def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler) 

class serverWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('MainResources/Assets/logo.png'))
		self.setWindowTitle('AnonChat Server')
		self.setGeometry(200, 100, 400, 300) 
		self.setMinimumWidth(400)
		self.setMinimumHeight(300)

		return

	# This function is called when user quits the application
	def closeEvent(self, event):
		event.accept()		


class startInterface(serverWindow):
	def __init__(self):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('MainResources/style.qss', "r").read())
		app.aboutToQuit.connect(self.closeEvent)
		serverApp = serverWindow()
		serverApp.show()
		# Execute the app mainloop
		app.exec_()
		return