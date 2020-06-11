import multiprocessing, os, signal, sys, time 
from UI.ui import *
from Connections.makeConnection import MakeConnection

sys.path.append('../')

####################################################################
		# Tasks:
		# Login Process
			# - Status 1 : Continue
			# - Status 0 : Exit

		# Subprocesses:
			# - Interface	[Main Process]
			# - Communications [Subprocess 1 : Communications]
####################################################################
class Client():
	def __init__(self):
		# Create variables/lists that will be shared between processes
		self.flags = multiprocessing.Array('i', 10)
		# This queue will be polled from core for handling tasks
		self.taskQueue = multiprocessing.Queue(maxsize = 1000)   

		# Connect to server
		self.connect()

		# Initialize Interface handler
		self.makeGUI()
		self.handleExit()


	def makeGUI(self):
		initGUI()
		

	def connect(self):
		connectionProcess = multiprocessing.Process(
			target = MakeConnection,
			args = (self.flags,)
		)
		connectionProcess.start()
		self.connectionPID = connectionProcess.pid


	def handleExit(self):
		print('Disconnecting...')
		os.kill(self.connectionPID, signal.SIGINT)	



if __name__ == '__main__':
	Client()