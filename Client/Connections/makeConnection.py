import json, socket, threading, select

class MakeConnection():
	def __init__(self, flags):
		print('Connecting to server...')
		self.flags = flags
		self.load()


	def load(self):
		filename = 'Connections/session.json'
		with open(filename, 'r') as file:
			self.sessionData = json.load(file)

		self.serverIP = self.sessionData.get('ip', 'localhost')
		self.serverPort = self.sessionData.get('port', None)
		print('Server IP >', self.serverIP, ':', self.serverPort)

		self.host = ''
		self.senderPort = 40000
		self.receiverPort = 40001

		self.recieverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.recieverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.recieverSocket.bind((self.host, self.receiverPort))
		self.recieverSocket.listen(1)

		self.recieveThread = threading.Thread(target = self.recieveData)
		self.recieveThread.setDaemon(True)
		self.recieveThread.start()


	def sendData(self, message):
		if type(message) != type({}):
			print('Error while sending data to server: Expected a python dict object.')
			return -1

		message = json.dumps(message)

		# Make a socket connection to the Server
		try:
			self.senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# This socket is used to send info
			self.senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make our pot reuseable
			self.senderSocket.bind((self.host, self.senderPort))	# Bind sender socket to port 40000
			self.senderSocket.connect((self.serverIP, self.serverPort))
		except Exception as error:
			print('Error: Host not reachable:', error)
			return -1

		# Try to send data in specific format, to the server
		# Format is Yet to be decided
		try:
			self.senderSocket.sendall(message.encode('utf-8'))
		except Exception as error:
			print('Error: Could not send data:', error)
			self.senderSocket.close()
			return -1

		response = str(self.senderSocket.recv(4096).decode('utf-8'))
		self.senderSocket.close()

		print('Server Response: ', response)
		return response


	def recieveData(self):
		# This thread acts as a "Server" for our main server, as in it listens for 
		# socket requests from our main server, or Gateway to be precise, and accepts data from it.
		# The data is then passed on to a shared queue for further processing.
		print('[ CLIENT ] Started recieveing thread.')
		print('Client info: ', self.recieverSocket.getsockname())

		self.stopFlag = False
		
		while not self.stopFlag:
			if self.recieverSocket._closed == True:
				break

			r, w, e = select.select((self.recieverSocket,), (), (), 1)
			for l in r:
				conn, addr = self.recieverSocket.accept()
				# Check if the data is from the Server
				if addr[0] == self.serverIP:			
					with conn:
						self.processServerData(conn)
					
			else:
				if self.flags[0]:
					self.stopFlag = True
					break

		self.recieverSocket.close()
		print('[ CLIENT ] Stopped recieveing thread.')


	def processServerData(self, conn):
		# Recieve Server Data is decided format:
		while True:
			data = conn.recv(4096)
			if not data: 
				break
		print(data)


	def handleExit(self):
		print('Closing network connections...')
		self.flags[0] = 1
		self.recieveThread.join()
		