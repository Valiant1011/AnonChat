from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

class prestigeWidget(QWidget):
	def __init__(self, prestigeLevel):
		super().__init__()
		self.prestigeIcon = QLabel(self.getHexValue(prestigeLevel))
		self.prestigeIcon.setFixedSize(40, 40)
		self.prestigeIcon.setObjectName('prestigeLabel')
		self.prestigeIcon.setAlignment(Qt.AlignCenter)
		
		self.setObjectAttributes(prestigeLevel)

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.prestigeIcon)
		self.layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.layout)


	def setText(self, text):
		print('Updating prestige icon...')
		self.prestigeIcon.setText(self.getHexValue(text))
		self.setObjectAttributes(text)


	def getHexValue(self, prestigeLevel):
		hexMap = {10:'A', 11:'B', 12 : 'C', 13 : 'D', 14 : 'E', 15 : 'F'}
		hexVal = ''
		try:
			prestigeLevel = int(prestigeLevel)
			if prestigeLevel > 255:
				prestigeLevel = 255
		except:
			prestigeLevel = 0

		while prestigeLevel:
			temp = prestigeLevel % 16
			prestigeLevel = int(prestigeLevel / 16)
			tChar = hexMap.get(temp, temp)
			hexVal += str(tChar)

		hexVal = hexVal[::-1]
		return hexVal


	def setObjectAttributes(self, prestigeLevel):
		prestigeLevel = int(prestigeLevel)
		style = self.prestigeIcon.styleSheet()

		if prestigeLevel > 200:
			# Golden Profile!
			style = "border-color : #ffdf00; border-radius : 20px; color : #ffdf00;"
			self.prestigeIcon.setStyleSheet(style)
			self.prestigeIcon.update()
			return

		# Get Border color
		if prestigeLevel < 50:
			style += "border-color : #aaaaaa;"
		elif prestigeLevel < 100: 
			style += "border-color : #ffdf00;"
		elif prestigeLevel < 150:
			style += "border-color : #ff033e;"
		else:
			style += "border-color : #089d20;"
		
		# Get shape
		prestigeLevel = prestigeLevel%50
		if prestigeLevel < 10:
			style += "border-radius : 0px;"
		elif prestigeLevel < 20:
			style += "border-top-right-radius : 20px;"
			style += "border-top-left-radius : 4px;"
			style += "border-bottom-left-radius : 4px;"
			style += "border-bottom-right-radius : 4px;"
		elif prestigeLevel < 30:
			style += "border-top-right-radius : 20px;"
			style += "border-top-left-radius : 20px;"
			style += "border-bottom-left-radius : 4px;"
			style += "border-bottom-right-radius : 4px;"
		elif prestigeLevel < 40:
			style += "border-top-right-radius : 20px;"
			style += "border-top-left-radius : 20px;"
			style += "border-bottom-left-radius : 20px;"
			style += "border-bottom-right-radius : 4px;"
		else:
			style += "border-top-right-radius : 20px;"
			style += "border-top-left-radius : 20px;"
			style += "border-bottom-left-radius : 20px;"
			style += "border-bottom-right-radius : 20px;"

		# Get Color
		prestigeLevel = prestigeLevel%10
		if prestigeLevel == 0:
			style += "color : #aaaaaa;"
		elif prestigeLevel == 1:
			style += "color : #ffffff;"
		elif prestigeLevel == 2:
			style += "color : #ffee00;"
		elif prestigeLevel == 3:
			style += "color : #c5fa69;"
		elif prestigeLevel == 4:
			style += "color : #9ff5e7;"
		elif prestigeLevel == 5:
			style += "color : #2db0ed;"
		elif prestigeLevel == 6:
			style += "color : #a56ee0;"
		elif prestigeLevel == 7:
			style += "color : #faa023;"
		elif prestigeLevel == 8:
			style += "color : #f55b47;"
		elif prestigeLevel == 9:
			style += "color : #3c8f81;"
			
		
		self.prestigeIcon.setStyleSheet(style)
		self.prestigeIcon.update()