import threading
import socketserver
import socket
import time

from RequestHandler import RequestHandler
from ThreadedServer import ThreadedServer

class NetworkManager():
	def __init__(self, systemFlags):
		print('Initialising connections...')
		self.systemFlags = systemFlags
		self.setupSocketServer() 


	def setupSocketServer(self):
		print('Initialising socket server...')

		# Listen on localhost:30000
		address = ('localhost', 30000) 

		server = ThreadedServer(
			address, 
			RequestHandler
		)

		with server:
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
				print('Gateway listen loop running in thread:', serverThread.getName())
				print('Press Ctrl+C to Exit.')

				# Wait until system exit
				while self.systemFlags[0] == 0:
					time.sleep(1)

			except (KeyboardInterrupt, SystemExit):
				print('Gateway Process Exiting...')
				server.shutdown()
				server.server_close()
				serverThread.join()
				print('[ EXIT ]')
				

			except Exception as error:
				print('Error while initialising gateway:', error)
				server.shutdown()
				server.server_close()