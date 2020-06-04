import time , sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from multiprocessing import Queue, Value
from profile import ProfileWidget
from friendList import FriendList
from chat import Chat
from user import User
# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler) 

# This class handles the main window of client
class clientWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.editFlag = Value('i')
		self.editFlag.value = 0 
		self.userChatsDict = {}  # Maps userID to their chat widget
		# Set app icon
		self.setWindowIcon(QIcon('Resources/Assets/logo.png'))
		# self.setWindowOpacity(0.99) # USEFUL later?
		# Set window title
		self.setWindowTitle('AnonChat')
		self.setGeometry(300, 200, 1366, 768) 
		self.setMinimumWidth(1066)
		self.setMinimumHeight(600)

		# Timer to update GUI
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateData)
		self.timer.start(1000)

		self.initUI()
		return


	def updateData(self):
		if self.editFlag.value == 1:
			self.editFlag.value = 0
			self.initUI()
			self.repaint()
		
	
	def initUI(self):
		try:
			# Get user (self) data
			self.userObject = User()
			self.userObject.loadUser()
			self.userObject.loadFriends()
			self.userID = self.userObject.getID()
			self.userName = self.userObject.getAlias()

			self.topWidget = QWidget()
			self.topWidget.setObjectName('mainWidget')
			profileBG = self.userObject.getProfileBG()
			style = "QWidget#mainWidget{border-image : url('Resources/BG/" + profileBG + "');}"
			self.topWidget.setStyleSheet(style)
			self.topLayout = QHBoxLayout(self.topWidget)

			self.makeSidebar()
			self.makeCentralArea()
			self.makeMenuBar()

			self.topLayout.addWidget(self.sideBar)
			self.topLayout.addWidget(self.centralArea)
			self.topLayout.addWidget(self.menuBar)
			self.topLayout.setSpacing(0)

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
		self.searchBarInput = QLineEdit()
		self.searchBarInput.setObjectName('searchBarInput')
		self.searchBarInput.setPlaceholderText('Search')

		# Top search area in sidebar _Search______________________
		self.sideBarButton = QPushButton('')
		self.sideBarButton.setObjectName('sideBarButton')
		self.sideBarButton.clicked.connect(self.searchButtonPressed)

		sideBarTopWidget = QWidget()
		sideBarTopLayout = QHBoxLayout(sideBarTopWidget)
		sideBarTopLayout.setContentsMargins(0, 0, 0, 0)
		sideBarTopLayout.addWidget(self.searchBarInput)
		sideBarTopLayout.addWidget(self.sideBarButton)
		sideBarTopLayout.setStretch(0, 85)
		sideBarTopLayout.setStretch(0, 15)
		sideBarTopLayout.setSpacing(0)
		
		# Friends List
		self.friendsListWidget = FriendList(self.userObject)
		self.friendsListWidget.chatChangeSignal.chatChanged.connect(self.chatChanged) 
		
		self.sideBar = QWidget()
		self.sideBar.setFixedWidth(330)
		self.sideBar.setObjectName('sideBar')
		self.sideBarLayout = QVBoxLayout(self.sideBar)
		self.sideBarLayout.addWidget(sideBarTopWidget)
		self.sideBarLayout.addWidget(self.friendsListWidget)
		self.sideBarLayout.setStretch(0, 5)
		self.sideBarLayout.setStretch(1, 95)
		self.sideBarLayout.setAlignment(Qt.AlignTop)


	def chatChanged(self, ID):
		info = self.friendsListWidget.getInfoFromID(ID)
		fName = info['Alias']
		self.chatWidget.setState(state = 'chat', receiver = fName, ID = ID)
		self.contentTabs.setCurrentIndex(1)

		
	def searchButtonPressed(self):
		print('Press')


	def makeCentralArea(self):
		#  Generate Profile widget and chat widget
		self.makeProfileWidget()
		self.makeChatWidget()

		self.centralArea = QWidget()
		self.centralLayout = QVBoxLayout(self.centralArea)

		self.contentTabs = QTabWidget()
		self.contentTabs.setObjectName('mainTabs')
		self.contentTabs.addTab(self.profileWidget, '')
		self.contentTabs.addTab(self.chatWidget, '')

		self.centralLayout.addWidget(self.contentTabs)
		self.centralLayout.setAlignment(Qt.AlignTop)
		self.centralLayout.setContentsMargins(0, 0, 0, 0)


	def makeProfileWidget(self):
		try:
			profileWidget = ProfileWidget(self.editFlag, self.userObject, self.userName)
		except:
			profileWidget = QWidget()
		scrollArea = QScrollArea()
		scrollArea.setWidgetResizable(True)
		scrollArea.setWidget(profileWidget)
		self.profileWidget = scrollArea


	def makeChatWidget(self):
		try:
			self.chatWidget = Chat()
		except Exception as error:
			print(error)


	def makeMenuBar(self):
		self.menuBar = QWidget()
		self.menuBar.setFixedWidth(80)
		self.menuBar.setObjectName('menuBar')
		self.menuBarLayout = QVBoxLayout()
		self.menuBar.setLayout(self.menuBarLayout)

		self.profileButton = QPushButton()
		self.profileButton.setFixedSize(64, 64)
		self.profileButton.setObjectName('menuButton')
		self.profileButton.setStyleSheet(
			"background-image : url(Resources/Assets/profile.png);background-position: center;"
		)
		self.profileButton.setToolTip('Your profile')
		self.profileButton.clicked.connect(self.handleProButtonClick)

		self.chatButton = QPushButton()
		self.chatButton.setFixedSize(64, 64)
		self.chatButton.setObjectName('menuButton')
		self.chatButton.setStyleSheet(
			"background-image : url(Resources/Assets/chat.png);background-position: center;"
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
		



class initGUI(clientWindow):
	def __init__(self):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		QFontDatabase.addApplicationFont("Resources/Fonts/Cyberpunk.ttf")
		QFontDatabase.addApplicationFont("Resources/Fonts/Adequate.ttf")
		QFontDatabase.addApplicationFont("Resources/Fonts/White Smith.otf")
		QFontDatabase.addApplicationFont("Resources/Fonts/Andromeda.ttf")
		QFontDatabase.addApplicationFont("Resources/Fonts/Roboto.ttf")
		QFontDatabase.addApplicationFont("Resources/Fonts/Padaloma.ttf")
		app.setStyleSheet(open('style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		client_app = clientWindow()
		client_app.show()
		# Execute the app mainloop
		app.exec_()
		return

initGUI()