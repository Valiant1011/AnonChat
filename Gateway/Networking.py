import threading
import socketserver
import socket
import time

from RequestHandler import RequestHandler
from ThreadedServer import ThreadedServer

class NetworkManager():
	def __init__(self, systemQueue):
		print('Initialising connections...')
		self.systemQueue = systemQueue
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
				print ('Server loop running in thread:', serverThread.getName())

				# Run the server until flag ( for now, run for 10 seconds )
				# while self.systemQueue[0] == 0:
				# 	time.sleep(1)
				serverThread.join()
				
				server.shutdown()
				server.server_close()
				print('[ EXIT ]')

			except (KeyboardInterrupt, SystemExit):
				print('Forcefully Exiting...')
				server.shutdown()
				server.server_close()
				serverThread.join()

			except Exception as error:
				print('Error while initialising server:', error)
				server.shutdown()
				server.server_close()