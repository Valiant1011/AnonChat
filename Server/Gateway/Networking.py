from Gateway.RequestHandler import RequestHandler
from Gateway.ThreadedServer import ThreadedServer

import threading, socketserver, socket, time

class SocketServerManager():
	def __init__(self, dbConnection, requestQueue, exitFlag):
		print('Initialising connections...')
		self.exitFlag = exitFlag
		self.setupSocketServer(dbConnection,requestQueue) 


	def setupSocketServer(self, dbConnection, requestQueue):
		print('Initialising socket server...')
		# Listen on localhost:30000
		address = ('localhost', 30000) 
		server = ThreadedServer(
			address, 
			RequestHandler
		)

		# Connect to database
		server.databaseManager = dbConnection
		if not server.databaseManager.checkStatus():
			print('Looks like an error occured in database connection. Stopping Authentication service.')
			return

		# Shared queue to process input from threads
		server.requestQueue = requestQueue

		ip, port = server.server_address 
		print('[ GATEWAY ] Running on ', ip, ':', port)

		try:
			serverThread = threading.Thread(
				target = server.serve_forever,
				args = (0.5,)
			)
			# Don't hang on exit, free all threads
			serverThread.setDaemon(True) 
			serverThread.start()
			print('Network listen loop running in thread:', serverThread.getName())

			# Wait for system exit
			while self.exitFlag.value == 0:	
				time.sleep(3)
			
			# At this point, main server has initiated shutdown.
			server.shutdown()
			server.server_close()
			serverThread.join()

		except Exception as error:
			print('Gateway error:', error)
			server.shutdown()
			server.server_close()

		finally:
			# Reset exit flag
			self.exitFlag.value = 0
			return