import multiprocessing, sys, os, time

from Gateway.Networking import SocketServerManager
from Gateway.ResponseHandler import ResponseManager
from Gateway.RequestProcessor import ProcessRequest
"""
Gateway is responsible for handling client requests, and handling them serially.
The Client-Gateway communication is handled by Web Sockets.
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

		self.processRequestExitFlag = multiprocessing.Value('i')
		self.processRequestExitFlag.value = 0

		self.setupProcesses(dbConnection)


	def setupProcesses(self, dbConnection):
		# Setup network service
		self.networkProcess = multiprocessing.Process(
			target = SocketServerManager,
			args = (dbConnection, self.requestQueue, self.networkExitFlag, )
		)
		self.networkProcessPID = self.networkProcess.pid
		self.networkProcess.start()

		# Start up request handler process
		self.processRequestProcess = multiprocessing.Process(
			target = ProcessRequest,
			args = (self.requestQueue, self.responseQueue, self.processRequestExitFlag, )
		)
		self.processRequestPID = self.processRequestProcess.pid
		self.processRequestProcess.start()

		# Start up response sender process
		self.responseProcess = multiprocessing.Process(
			target = ResponseManager,
			args = (self.responseQueue, self.responseExitFlag, )
		)
		self.responsePID = self.responseProcess.pid
		self.responseProcess.start()


	def processExit(self):
		print('\nGateway initiating Exit...')

		print('Closing Network subprocess...')
		self.networkExitFlag.value = 1
		# Wait for network process exit
		try:
			while self.networkExitFlag.value != 0:
				print('.', end = '')
				time.sleep(1)
		except:
			print('\nNetwork subprocess abandoned...')
			return
		finally:
			print('Network subprocess closed.')

		print('\nClosing ProcessRequest subprocess...')
		self.processRequestExitFlag.value = 1
		# Wait for response process exit
		try:
			while self.processRequestExitFlag.value != 0:
				print('.', end = '')
				time.sleep(1)
		except:
			print('ProcessRequest subprocess abandoned...')
			return
		finally:
			print('ProcessRequest subprocess closed.')

		print('\nClosing Response subprocess...')
		self.responseExitFlag.value = 1
		# Wait for response process exit
		try:
			while self.responseExitFlag.value != 0:
				print('.', end = '')
				time.sleep(1)
		except:
			print('Response subprocess abandoned...')
			return
		finally:
			print('Response subprocess closed.')

		print('\nGateway closed successfully.')
