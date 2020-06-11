import multiprocessing, sys, os

from Networking import NetworkManager
"""
Gateway is responsible for handling client requests, and passing them serially to the Server
The Client-Gateway communication is handled by Web Sockets, while the Server-Gateway connection is handled by RabbitMQ internally.
"""
class Gateway():
	"""
	Create 3 processes:
	0. Network Service
	1. RabbitMQ Service
	"""
	def __init__(self):
		self.initSystemQueue()
		self.setupProcesses()


	def initSystemQueue(self):
		self.systemQueue = multiprocessing.Array('i', 10)
		self.systemQueue[0] = 0			# Global shutdown flag

	def setupProcesses(self):
		# Setup network service
		self.networkProcess = multiprocessing.Process(
			target = NetworkManager,
			args = (self.systemQueue,)
		)
		self.networkProcessPID = self.networkProcess.pid
		self.networkProcess.start()

if __name__ == '__main__':
	Gateway()