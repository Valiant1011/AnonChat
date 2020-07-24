import time , sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from multiprocessing import Queue, Value

from UI.profile import ProfileWidget
from UI.friendList import FriendList
from UI.chat import Chat
from UI.user import User
# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler) 

# This class handles the main window of client
class clientWindow(QMainWindow):
	def __init__(self, networkManager, taskQueue):
		super().__init__()
		self.editFlag = Value('i')
		self.editFlag.value = 0 
		self.profileLoadedFlag = Value('i')
		self.profileLoadedFlag.value = 0
		self.dataQueue = Queue(100)
		self.userChatsDict = {}  # Maps userID to their chat widget
		self.networkManager = networkManager
		self.taskQueue = taskQueue

		# Set app icon
		self.setWindowIcon(QIcon('Resources/Assets/logo.png'))
		# self.setWindowOpacity(0.99) # USEFUL later?
		# Set window title
		self.setWindowTitle('AnonChat')
		self.setGeometry(200, 100, 1600, 900) 
		self.setMinimumWidth(1066)
		self.setMinimumHeight(600)

		# Timer to handle server messages
		self.serverDataTimer = QTimer()
		self.serverDataTimer.timeout.connect(self.processServerData)
		self.serverDataTimer.start(500)

		# Timer to update GUI
		self.timer = QTimer()
		self.timer.timeout.connect(self.processClientData)
		self.timer.start(500)

		self.loadingUI()
		return 


	# This function checks for UI updates every second
	def processClientData(self):
		if self.editFlag.value == 1:
			self.editFlag.value = 0
			self.initUI()
			self.repaint()

		if self.profileLoadedFlag.value == 1:
			self.profileLoadedFlag.value = 0
			self.initUI()
			self.repaint()

		# Handle Client to server data
		try:
			# dataQueue contains all data which has to go from client to server
			data = self.dataQueue.get(block = False, timeout = 0.5)
			status = self.networkManager.sendData(data)
			if status == 'OK':
				pass
			else:
				print('Error: Could not save data to Server.')

		except Exception as e:
			if "Empty" in str(e) or str(e) == "":
				pass
			else:
				print('Error: ', e)


	def processServerData(self):
		# Handle Server to Client data
		try:
			# taskQueue contains all data which has to go from client to server
			data = self.taskQueue.get(block = False, timeout = 0.5)
			
			code = data.get('Code', 'NULL')
			if code == 'Profile':
				userID = data.get('userID')
				userName = data.get('userAlias')
				self.updateSessionInfo(userName, userID)

				with open('profile.json', "w") as file:
					json.dump(data, file, indent = 4)
				# --- Profile has been loaded into file

				# Send this information to client data handler function
				print('Loading profile...')
				self.profileLoadedFlag.value = 1

		except:
			pass

		
	def updateSessionInfo(self, userName, userID):
		filename = 'session.json'
		with open(filename, 'r') as file:
			sessionData = json.load(file)

		sessionData['username'] = userName
		sessionData['userID'] = userID
		with open(filename, 'w') as file:
			json.dump(sessionData, file, indent = 4)


	def loadingUI(self):
		# This is a temporary screen shown until the client gets all data from server
		# Sort of a Loading screen, as the name suggests
		# More work needed--------------------------------------------------------------------------------------------------<<!
		self.loadingWidget = QWidget()
		self.loadingLayout = QVBoxLayout(self.loadingWidget)
		self.setCentralWidget(self.loadingWidget)
		
	# This function is responsible for creating the main UI of client
	def initUI(self):
		try:
			# Load user (self) data
			self.userObject = User()
			self.userObject.loadUser()

			# Get user data
			self.userID = self.userObject.getID()
			self.userName = self.userObject.getAlias()

			# Main layout -> TopWidget[Sidebar + CentralArea + MenuBar]
			self.topWidget = QWidget()
			self.topWidget.setObjectName('mainWidget')
			profileBG = self.userObject.getProfileBG()
			style = "QWidget#mainWidget{border-image : url('Resources/BG/" + profileBG + "');}"
			self.topWidget.setStyleSheet(style)
			self.topLayout = QHBoxLayout(self.topWidget)

			# Generate reuired items by calling their constructors
			self.makeSidebar()
			self.makeCentralArea()
			self.makeMenuBar()

			# Add these items in the main layout
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
			print('[ UI ][ ERROR ] : ' , exc_type, fname, exc_tb.tb_lineno)
		return

	# Generates the sidebar portion
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
		self.sideBar.setFixedWidth(360)
		self.sideBar.setObjectName('sideBar')
		self.sideBarLayout = QVBoxLayout(self.sideBar)
		self.sideBarLayout.addWidget(sideBarTopWidget)
		self.sideBarLayout.addWidget(self.friendsListWidget)
		self.sideBarLayout.setStretch(0, 5)
		self.sideBarLayout.setStretch(1, 95)
		self.sideBarLayout.setAlignment(Qt.AlignTop)

	# This function is called when a chat label is clicked on
	def chatChanged(self, ID):
		info = self.friendsListWidget.getInfoFromID(ID)
		fName = info['Alias']
		self.chatWidget.setState(state = 'chat', receiver = fName, ID = ID)
		self.contentTabs.setCurrentIndex(1)

	# This function is called when user clicks on the Search button in the sidebar
	def searchButtonPressed(self):
		print('Press')

	# Generates the central portion [ Profile + Chats ]
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

	# Reads the user object and generates its profile view
	def makeProfileWidget(self):
		try:
			profileWidget = ProfileWidget(self.editFlag, self.dataQueue, self.userObject, self.userName)
		except:
			profileWidget = QWidget()
		scrollArea = QScrollArea()
		scrollArea.setWidgetResizable(True)
		scrollArea.setWidget(profileWidget)
		self.profileWidget = scrollArea

	# Generates a chat view for a user
	def makeChatWidget(self):
		try:
			self.chatWidget = Chat()
		except Exception as error:
			print(error)

	# Right side menu with profile and random chat butttons
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

	# This function is called when profile button is clicked
	def handleProButtonClick(self):
		self.contentTabs.setCurrentIndex(0)

	# This function is called when random button is clicked
	def handleChatButtonClick(self):
		self.contentTabs.setCurrentIndex(1)
		self.chatWidget.setState('search')

	# This function is called when user quits the application
	def closeEvent(self, event):
		# Reset profile.json file
		with open('profile.json', "w") as file:
			file.write('Nothing to see here!')

		event.accept()		


# This class runs the main app loop for interface and calls its object
class initGUI(clientWindow):
	def __init__(self, networkManager, taskQueue):
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

		client_app = clientWindow(networkManager, taskQueue)
		client_app.showMaximized()
		# Execute the app mainloop
		app.exec_()
		return