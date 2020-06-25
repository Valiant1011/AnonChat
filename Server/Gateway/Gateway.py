import multiprocessing, sys, os, time

from Gateway.Networking import SocketServerManager
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
	def __init__(self, dbConn, requestQueue, responseQueue):
		self.responseQueue = responseQueue
		self.systemFlags = multiprocessing.Array('i', 10)
		self.systemFlags[0] = 0			# Global shutdown flag
		self.setupProcesses(dbConn, requestQueue)


	def startResponsePoll(self):
		print('[ RUNNING ] Press Ctrl+C to Exit.')
		while True:
			if self.systemFlags[0]:
				break

			try:
				data = self.responseQueue.get(block = True, timeout = 5)
				self.processResponseData(data)

			except KeyboardInterrupt:
				print('[ GATEWAY ] Exiting...')
				self.systemFlags[0] = 1

			except Exception as e:
				if "Empty" in str(e) or str(e) == '':
					pass
				else:
					print('[ GATEWAY ][ RESPONSE ] Error:', e)
					self.systemFlags[0] = 1
					break
			try:
				time.sleep(1)
			except:
				pass

			
	def processResponseData(self, data):
		if data == 'EXIT':
			self.systemFlags[0] = 1
			return

		print(data)


	def setupProcesses(self, dbConn, requestQueue):
		# Setup network service
		self.networkProcess = multiprocessing.Process(
			target = SocketServerManager,
			args = (self.systemFlags, dbConn, requestQueue,)
		)
		self.networkProcessPID = self.networkProcess.pid
		self.networkProcess.start()
