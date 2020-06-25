from Gateway.Gateway import Gateway  #From Gateway Folder's Gateway.py file, import Gateway class.
from Gateway.DatabaseManager import DatabaseManager
import multiprocessing, time

class Server():
	def __init__(self):
		self.initQueues()
		print('[ SERVER ] Making a connection to Database...')
		dbConncetion = DatabaseManager()
		print('[ SERVER ] Initialising Gateway...')
		gatewayConnection = Gateway(dbConncetion, self.requestQueue, self.responseQueue)
		gatewayConnection.startResponsePoll()


	def initQueues(self):
		self.requestQueue = multiprocessing.Queue(1000)
		self.responseQueue = multiprocessing.Queue(1000)


	def handleRequests(self):
		# Poll request Queue
		# TODO
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			print('[ SERVER ] Exiting...')
			self.responseQueue.put('EXIT')
			gatewayConnection.close()
			dbConncetion.closeConnection()

Server()