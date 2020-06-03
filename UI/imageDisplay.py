from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from os import path
from math import ceil
# Displays a carousal of images on 'path', whose names are stored in fileList.
# It will allow a single image to be in 'Active' state, ie, that image is selected by the user
class imageDisplay(QWidget):
	def __init__(
			self, 
			path = './', 
			fileList = [], 
			dimensionX = 180, 
			dimensionY = 180,
			currentSelected = 0
		):
		super().__init__()
		self.path = path
		self.fileList = fileList
		self.selectedIndex = currentSelected
		self.itemCount = len(fileList)
		self.dimensionX = dimensionX
		self.dimensionY = dimensionY
		self.imageLabels = [None] * self.itemCount
		self.selectedStyle = "QLabel{border : 10px solid rgba(150, 150, 150, 200);}"
		self.unselectedStyle = "QLabel{border : 0px;}"

		self.mainLayout = self.getScroller()
		self.setLayout(self.mainLayout)
		self.setMinimumHeight(self.dimensionY + 10)


	def getScroller(self):
		# Make carousal
		scrollWidget = QWidget()
		scrollLayout = QHBoxLayout(scrollWidget)
		scrollLayout.setContentsMargins(0, 0, 0, 0)
		
		for i in range(self.itemCount):
			fullPath = self.path + self.fileList[i]
			if not path.exists(fullPath):
				print('Error while reading a file.')
			else:
				self.imageLabels[i] = QLabel()
				self.imageLabels[i].setFixedSize(self.dimensionX, self.dimensionY)
				self.imageLabels[i].setObjectName('displayImage')
				pixmap = QPixmap(fullPath)
				scaled = pixmap.scaledToWidth(self.dimensionX)
				self.imageLabels[i].setPixmap(scaled)
				scrollLayout.addWidget(self.imageLabels[i])

		self.imageLabels[self.selectedIndex].setStyleSheet(self.selectedStyle)

		self.scrollContainer = QScrollArea()
		self.scrollContainer.setWidgetResizable(True)
		self.scrollContainer.setWidget(scrollWidget)
		self.scrollContainer.setFixedWidth(800)
		self.scrollMinimum = self.scrollContainer.horizontalScrollBar().minimum()
		self.scrollMaximum = self.scrollContainer.horizontalScrollBar().maximum()
		self.scrollInterval = self.scrollMaximum - self.scrollMinimum
		newScrollBarPos = ((self.selectedIndex + 1) * self.scrollInterval) / self.itemCount
		self.scrollContainer.horizontalScrollBar().setValue(newScrollBarPos);  

		# carousal buttons
		leftButton = QPushButton()
		leftButton.setFixedSize(40, 180)
		leftButton.setObjectName("leftButton")
		leftButton.clicked.connect(self.leftPress)
		rightButton = QPushButton()
		rightButton.setFixedSize(40, 180)
		rightButton.setObjectName("rightButton")
		rightButton.clicked.connect(self.rightPress)
		
		mainLayout = QHBoxLayout()
		mainLayout.addWidget(leftButton)
		mainLayout.addWidget(self.scrollContainer)
		mainLayout.addWidget(rightButton)
		mainLayout.setContentsMargins(0, 0, 0, 0)

		return mainLayout


	def leftPress(self):
		newSelection = (self.selectedIndex + self.itemCount - 1) % self.itemCount
		self.imageLabels[self.selectedIndex].setStyleSheet(self.unselectedStyle)
		self.selectedIndex = newSelection
		self.imageLabels[self.selectedIndex].setStyleSheet(self.selectedStyle)
		newScrollBarPos = (newSelection * self.scrollInterval * 1.3) / self.itemCount
		self.scrollContainer.horizontalScrollBar().setValue(newScrollBarPos);  

		
	
	def rightPress(self):
		newSelection = (self.selectedIndex + 1) % self.itemCount
		self.imageLabels[self.selectedIndex].setStyleSheet(self.unselectedStyle)
		self.selectedIndex = newSelection
		self.imageLabels[self.selectedIndex].setStyleSheet(self.selectedStyle)
		newScrollBarPos = ceil((newSelection * self.scrollInterval * 1.3) / self.itemCount)
		self.scrollContainer.horizontalScrollBar().setValue(newScrollBarPos);  


	def getSelected(self):
		return self.fileList[self.selectedIndex]