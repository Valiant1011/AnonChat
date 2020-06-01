from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt

class ChatWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.state = 'search'
		try:
			self.reloadCentralLayout()
		except Exception as error:
			print(error)


	def reloadCentralLayout(self):
		if self.state == 'search':
			self.layout = self.loadingState()
			self.setStyleSheet('QWidget{background : rgba(6, 6, 6, 50);}')

		self.setLayout(self.layout)
		self.repaint()
		

	def loadingState(self):
		loadingAnimation = QLabel()
		loadingAnimation.setStyleSheet("border:0px;")
		loadingAnimation.setAlignment(Qt.AlignCenter)
		loadingAnimation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		anim = QMovie('Resources/Assets/loading.webp')
		loadingAnimation.setMovie(anim)
		anim.start()
		loadingAnimContainer = QWidget()
		# loadingAnimContainer.setStyleSheet(
		# 	"background-image : url('Resources/Assets/LoadingBG.png');" + 
		# 	"background-repeat : no-repeat;" + 
		# 	"background-position : center;"
		# )
		loadingAnimContainerLayout = QVBoxLayout(loadingAnimContainer)
		loadingAnimContainerLayout.addWidget(loadingAnimation)
		loadingAnimContainerLayout.setContentsMargins(0, 0, 0, 0)


		loadingText = QLabel('Loading...')
		loadingText.setObjectName('subsectionHeading')
		loadingText.setAlignment(Qt.AlignCenter)


		containerLayout = QVBoxLayout()
		containerLayout.addWidget(loadingAnimContainer)
		containerLayout.addWidget(loadingText)
		containerLayout.setAlignment(Qt.AlignCenter)
		containerLayout.setContentsMargins(0, 0, 0, 0)
		containerLayout.setStretch(0, 70)
		containerLayout.setStretch(1, 30)


		return containerLayout


	def setState(self, state = 'search'):
		self.state = state
		self.reloadCentralLayout()