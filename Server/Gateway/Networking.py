import threading
import socketserver
import socket
import time

from Gateway.RequestHandler import RequestHandler
from Gateway.ThreadedServer import ThreadedServer


class SocketServerManager():
	def __init__(self, systemFlags, dbConnection, requestQueue):
		print('Initialising connections...')
		self.systemFlags = systemFlags
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
			# don't hang on exit
			serverThread.setDaemon(True) 
			serverThread.start()
			print('Network listen loop running in thread:', serverThread.getName())

			# Wait until system exit
			while self.systemFlags[0] == 0:
				time.sleep(1)

		except (KeyboardInterrupt, SystemExit):
			print('Network Process Exiting...')
			server.shutdown()
			server.server_close()
			serverThread.join()
			print('[ EXIT ]')
			

		except Exception as error:
			print('Error while initialising gateway:', error)
			server.shutdown()
			server.server_close()