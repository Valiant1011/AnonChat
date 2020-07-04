import multiprocessing, sys, os, time

from Gateway.Networking import SocketServerManager
from Gateway.ResponseHandler import ResponseManager
"""
Gateway is responsible for handling client requests, and passing them serially to the Server
The Client-Gateway communication is handled by Web Sockets, while the Server-Gateway connection is handled by RabbitMQ internally.
"""
class Gateway():
	"""
	Create 2 processes:
	0. Network Service
	1. Response manager

	This class also handles the correct shutdown event of the above two processes.
	"""
	def __init__(self, dbConnection, requestQueue, responseQueue):
		self.responseQueue = responseQueue
		self.requestQueue = requestQueue
		
		# The following shared flags are used to send Exit signal to network and response manager processes:
		self.networkExitFlag = multiprocessing.Value('i')
		self.networkExitFlag.value = 0

		self.responseExitFlag = multiprocessing.Value('i')
		self.responseExitFlag.value = 0

		self.setupProcesses(dbConnection)


	def setupProcesses(self, dbConnection):
		# Setup network service
		self.networkProcess = multiprocessing.Process(
			target = SocketServerManager,
			args = (dbConnection, self.requestQueue, self.networkExitFlag, )
		)
		self.networkProcessPID = self.networkProcess.pid
		self.networkProcess.start()

		self.responseProcess = multiprocessing.Process(
			target = ResponseManager,
			args = (self.requestQueue, self.responseExitFlag, )
		)
		self.responsePID = self.responseProcess.pid
		self.responseProcess.start()


	def processExit(self):
		print('\nGateway initiating Exit...')

		print('Closing Network process...')
		self.networkExitFlag.value = 1
		# Wait for network process exit
		try:
			while self.networkExitFlag.value != 0:
				print('.', end = '')
				time.sleep(1)
		except:
			print('\nNetwork process abandoned...')
			return

		print('\nClosing Response process...')
		self.responseExitFlag.value = 1
		# Wait for response process exit
		try:
			while self.responseExitFlag.value != 0:
				print('.', end = '')
				time.sleep(1)
		except:
			print('Response process abandoned...')
			return

		print('\nGateway closed successfully.')
