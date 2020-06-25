import json, socket, threading, select, time

class MakeConnection():
	def __init__(self, flags, sessionData):
		print('Connecting to server...')
		self.flags = flags
		self.sessionData = sessionData
		self.load()


	def load(self):
		self.serverIP = self.sessionData.get('ip', 'localhost')
		self.serverPort = self.sessionData.get('port', None)
		print('Server IP >', self.serverIP, ':', self.serverPort)

		# Ports are fixed to limit instances of AnonChat to one per PC
		self.clientHost = ''
		self.senderPort = 40000
		self.receiverPort = 40001

		try:
			self.recieverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.recieverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.recieverSocket.bind((self.clientHost, self.receiverPort))
			self.recieverSocket.listen(1)
			self.recieveThread = threading.Thread(target = self.recieveData)
			self.recieveThread.setDaemon(True)
			self.recieveThread.start()
		except Exception as error:
			print('Error : Can not launch multiple instances of Client.')
			self.flags[0] = 1


	def getListenIP(self):
		return self.clientHost


	def getListenPort(self):
		return self.receiverPort


	def sendData(self, message):
		response = 'NULL'
		if type(message) != type({}):
			print('Error while sending data to server: Expected a python dict object.')
			return "NULL"

		if message.get('code', 'NULL') == 'Login':
			self.userName = message.get('userName', 'NULL')
			self.password = message.get('password', 'NULL')
			self.clientID = message.get('userID', 'NULL')
		elif message.get('code', 'NULL') == 'Register':
			pass
		else:
			# Add authentication fields to message
			message['userName'] = self.userName
			message['password'] = self.password
			message['userID'] = self.clientID

		# Convert the message to JSON format:
		message = json.dumps(message)

		# Make a socket connection to the Server:
		try:
			self.senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# This socket is used to send info
			self.senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make our pot reuseable
			self.senderSocket.bind((self.clientHost, self.senderPort))	# Bind sender socket to port 40000
			self.senderSocket.connect((self.serverIP, self.serverPort))
		except Exception as error:
			print('Error: Host not reachable:', error)
			return "ERROR"

		# Try to send data in specific format to the server
		#----------------------------------------------------------- Format is Yet to be decided
		try:
			blank = ''
			self.senderSocket.sendall(message.encode('utf-8'))
			response = self.recvall(self.senderSocket)
			self.senderSocket.close()

		except Exception as error:
			print('Error: Could not send data:', error)
			self.senderSocket.close()
			return "NULL"

		finally:
			return response


	def recvall(self, sock, timeout = 1):
		# setup to use non-blocking sockets
		# if no data arrives it assumes transaction is done
		# recv() returns a string
		sock.setblocking(0)
		total_data=[]
		data = ''
		begin = time.time()

		while True:
			# If you got some data, then break after wait sec
			if total_data and time.time() - begin > timeout:
				break

			# If you got no data at all, wait a little longer
			elif time.time() - begin > timeout * 2:
				break
			wait = 0
			try:
				data = sock.recv(4096).decode('utf-8')
				if data:
					total_data.append(data)
					begin = time.time()
					data = ''
					wait = 0
				else:
					time.sleep(0.1)
			except:
				pass
			#When a recv returns 0 bytes, other side has closed
		result=''.join(total_data)
		return result


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
		sock.setblocking(0)
		total_data=[]
		data = ''
		begin = time.time()
		timeout = 1
		while True:
			# If you got some data, then break after wait sec
			if total_data and time.time() - begin > timeout:
				break

			# If you got no data at all, wait a little longer
			elif time.time() - begin > timeout * 2:
				break

			wait = 0
			try:
				data = sock.recv(4096).decode('utf-8')
				if data:
					total_data.append(data)
					begin = time.time()
					data = ''
					wait = 0
				else:
					time.sleep(0.1)
			except:
				pass
			#When a recv returns 0 bytes, other side has closed
		result=''.join(total_data)
		print(result)


	def handleExit(self):
		print('Closing network connections...')
		self.flags[0] = 1
		self.recieveThread.join()
		