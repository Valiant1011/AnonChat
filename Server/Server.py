from Gateway.Gateway import Gateway  #From Gateway Folder's Gateway.py file, import Gateway class.
from DatabaseManager import DatabaseManager
from UI.Interface import startInterface
import multiprocessing, time

class Server():
	def __init__(self):
		self.initQueues()
		print('[ SERVER ] Making a connection to Database...')
		self.dbConncetion = DatabaseManager()
		print('[ SERVER ] Initialising Gateway...')
		self.gatewayConnection = Gateway(self.dbConncetion, self.requestQueue, self.responseQueue)
		

	def initQueues(self):
		self.requestQueue = multiprocessing.Queue(1000)
		self.responseQueue = multiprocessing.Queue(1000)


	def waitForExit(self):		
		print('[ SERVER ] Exiting...')
		self.gatewayConnection.processExit()
		self.dbConncetion.closeConnection()
		print('[ SERVER ] Closed.')

mainServer = Server()
mainInterface = startInterface()
mainServer.waitForExit()