import time , sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from profile import ProfileWidget
from chat import ChatWidget
from user import User
# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler) 

# This class handles the main window of server
class serverWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		# Get user data
		self.userObject = User()
		self.userObject.loadUser()

		# Set app icon
		self.setWindowIcon(QIcon('Resources/logo.png'))
		# Set window title
		self.setWindowTitle('AnonChat')
		self.setGeometry(300, 200, 1366, 768) 
		self.setMinimumWidth(1066)
		self.setMinimumHeight(600)

		self.makeSidebar()
		self.makeProfileWidget()
		self.makeChatWidget()
		self.makeCentralArea()
		self.makeMenuBar()
		serverWindow.initUI(self)
		return

	
	def initUI(self):
		try:
			self.topWidget = QWidget()
			self.topWidget.setObjectName('mainWidget')
			self.topLayout = QHBoxLayout(self.topWidget)

			self.topLayout.addWidget(self.sideBar)
			self.topLayout.addWidget(self.centralArea)
			self.topLayout.addWidget(self.menuBar)

			self.topLayout.setContentsMargins(0, 0, 0, 0)
			self.topLayout.setStretch(0, 20)
			self.topLayout.setStretch(1, 74)
			self.topLayout.setStretch(2, 6)
			
			self.setCentralWidget(self.topWidget)
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[ ERROR ] : ' , exc_type, fname, exc_tb.tb_lineno)
		return


	def makeSidebar(self):
		self.sideBar = QWidget()
		self.sideBar.setObjectName('sideBar')
		self.sideBarLayout = QVBoxLayout(self.sideBar)

		self.searchBarInput = QLineEdit()
		self.searchBarInput.setPlaceholderText('Search')

		self.sideBarLayout.addWidget(self.searchBarInput)
		self.sideBarLayout.setAlignment(Qt.AlignTop)


	def makeProfileWidget(self):
		self.profileWidget = ProfileWidget(self.userObject)


	def makeChatWidget(self):
		self.chatWidget = ChatWidget()


	def makeCentralArea(self):
		self.centralArea = QWidget()
		self.centralLayout = QVBoxLayout(self.centralArea)

		self.contentTabs = QTabWidget()
		self.contentTabs.setObjectName('mainTabs')
		self.contentTabs.addTab(self.profileWidget, '')
		self.contentTabs.addTab(self.chatWidget, '')

		self.centralLayout.addWidget(self.contentTabs)
		self.centralLayout.setAlignment(Qt.AlignTop)
		self.centralLayout.setContentsMargins(0, 0, 0, 0)


	def makeMenuBar(self):
		self.menuBar = QWidget()
		self.menuBar.setObjectName('menuBar')
		self.menuBarLayout = QVBoxLayout()
		self.menuBar.setLayout(self.menuBarLayout)

		self.profileButton = QPushButton()
		self.profileButton.setFixedSize(64, 64)
		self.profileButton.setObjectName('menuButton')
		self.profileButton.setStyleSheet(
			"background-image : url(Resources/profile.png);background-position: center;"
		)
		self.profileButton.setToolTip('Your profile')
		self.profileButton.clicked.connect(self.handleProButtonClick)

		self.chatButton = QPushButton()
		self.chatButton.setFixedSize(64, 64)
		self.chatButton.setObjectName('menuButton')
		self.chatButton.setStyleSheet(
			"background-image : url(Resources/chat.png);background-position: center;"
		)
		self.chatButton.clicked.connect(self.handleChatButtonClick)
		
		self.menuBarLayout.addStretch(1)
		self.menuBarLayout.addWidget(self.profileButton)
		self.menuBarLayout.addStretch(1)
		self.menuBarLayout.addWidget(self.chatButton)
		self.menuBarLayout.addStretch(50)
		self.menuBarLayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
		self.menuBarLayout.setContentsMargins(0, 20, 0, 0)

		# self.menuBar.setVisible(False)


	def handleProButtonClick(self):
		self.contentTabs.setCurrentIndex(0)


	def handleChatButtonClick(self):
		self.contentTabs.setCurrentIndex(1)


	def closeEvent(self, event):
		event.accept()
		



class initGUI(serverWindow):
	def __init__(self):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		server_app = serverWindow()
		server_app.show()
		# Execute the app mainloop
		app.exec_()
		return

initGUI()