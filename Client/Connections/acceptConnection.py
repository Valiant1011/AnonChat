import socket, select, time, json

"""
This class listens for any message from Server, and handles it accordingly.
"""
class ManageServerResponse():
	def __init__(self, host, port, flags, taskQueue, serverIP = '127.0.0.1'):
		print('Starting listen process...')
		self.recieverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.recieverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.recieverSocket.bind((host, port))
		self.recieverSocket.listen(5)
		self.flags = flags
		self.serverIP = serverIP
		self.taskQueue = taskQueue
		self.recieveData()


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

			# Every second, try to accept connection. This is done to prevent Thread blocking.
			r, w, e = select.select((self.recieverSocket,), (), (), 1)
			for l in r:
				conn, addr = self.recieverSocket.accept()
				print('Accepted a new connection from', addr)
			
				with conn:
					self.processServerData(conn)
					
			else:
				if self.flags[0]:
					self.stopFlag = True
					break

		self.recieverSocket.close()
		print('[ CLIENT ] Stopped recieveing thread.')


	def processServerData(self, conn):
		try:
			data = self.recvall(conn)
			data = json.loads(data)
			self.taskQueue.put(data)
		except Exception as e:
			print('Error while receiving server data:', e)


	def recvall(self, sock, timeout = 1):
		# setup to use non-blocking sockets
		# if no data arrives it assumes transaction is done
		# recv() returns a string
		sock.setblocking(0)
		total_data = []
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
			except Exception as error:
				pass
			
				#When a recv returns 0 bytes, other side has closed
		try:
			result = ''.join(total_data)
		except Exception as e:
			print('Error while building server data: ', e)
			return 'NULL'

		return result