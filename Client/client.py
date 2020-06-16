import multiprocessing, os, signal, sys, time 
from UI.ui import *
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
		self.flags[0] = 0
		# This queue will be polled from core for handling tasks
		self.taskQueue = multiprocessing.Queue(maxsize = 1000)   

		# Connect to server
		self.connect()
		self.networkManager.sendData({'info' : 'Hello server!'})

		# Initialize Interface handler
		self.makeGUI()
		self.handleExit()


	def makeGUI(self):
		initGUI() 
		

	def connect(self):
		self.networkManager = MakeConnection(self.flags)


	def handleExit(self):
		self.flags[0] = 1	# Exit flag
		self.networkManager.handleExit()
		


if __name__ == '__main__':
	Client()