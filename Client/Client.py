import multiprocessing, os, signal, sys, time 
from UI.ui import *
from UI.login import *
from Connections.makeConnection import MakeConnection

sys.path.append('../')

####################################################################
		# Tasks:
		# Login Process
			# - Status 1 : Continue
			# - Status 0 : Exit
		# Make connection object
		# Start interface, and pass on the connection object to it.
####################################################################
class Client():
	def __init__(self):
		# Create variables/lists that will be shared between processes
		self.flags = multiprocessing.Array('i', 10)
		self.flags[0] = 0	# Global Exit Flag
		self.flags[1] = 0  # Login status : 0 Init, 1 Accept, 2 Reject, 3 Error
		# This queue will be polled from core for handling tasks
		self.taskQueue = multiprocessing.Queue(maxsize = 1000) 

		# Load data
		self.loadData()

		# Connect to server
		self.networkManager = MakeConnection(self.flags, self.sessionData)

		# Initiate register/login UI
		Login(self.flags, self.networkManager, self.sessionData)

		# Initialize Interface handler
		if self.flags[1] == 1:
			self.makeGUI()

		self.handleExit()


	def loadData(self):
		filename = 'session.json'
		with open(filename, 'r') as file:
			self.sessionData = json.load(file)


	def makeGUI(self):
		initGUI() 
			

	def handleExit(self):
		self.flags[0] = 1	# Exit flag
		self.networkManager.handleExit()
		


if __name__ == '__main__':
	Client()