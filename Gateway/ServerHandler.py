class ServerHandler(socketserver.BaseRequestHandler)
	def handle(self):
		try:
			data = self.request.recv(4096).decode('utf-8')
		except:
			print('Error: Could not parse server data')
			return

		# Get server INFO:
		self.serverAddress = self.request.getpeername()
		print('Server Address:', serverAddress)

		# Process data and do something with it

		ack = "OK"
		ack = ack.encode('utf-8')
		# Make an ack and send it to server
		try:
			self.request.send(ack)
		except:
			print('Error: Could not send ack!')
		finally:
			return