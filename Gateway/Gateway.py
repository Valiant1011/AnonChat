import multiprocessing, sys, os

from Networking import NetworkManager
"""
Gateway is responsible for handling client requests, and passing them serially to the Server
The Client-Gateway communication is handled by Web Sockets, while the Server-Gateway connection is handled by RabbitMQ internally.
"""
class Gateway():
	"""
	Create 2 processes:
	0. Network Service
	1. RabbitMQ Service
	"""
	def __init__(self):
		self.initSystemData()
		self.setupProcesses()

		self.tempWait()


	def initSystemData(self):
		self.systemFlags = multiprocessing.Array('i', 10)
		self.systemFlags[0] = 0			# Global shutdown flag


	def setupProcesses(self):
		# Setup network service
		self.networkProcess = multiprocessing.Process(
			target = NetworkManager,
			args = (self.systemFlags,)
		)
		self.networkProcessPID = self.networkProcess.pid
		self.networkProcess.start()


	def tempWait(self):
		try:
			while True:
				pass
		except KeyboardInterrupt:
			self.systemFlags[0] = 1


if __name__ == '__main__':
	Gateway()