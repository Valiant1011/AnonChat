import threading, socket, json
'''
This class accepts messages from Response queue
and sends a response to the client the message is intended for.
'''
class ResponseManager():
	def __init__(self, responseQueue, exitFlag):
		self.responseQueue = responseQueue
		self.exitFlag = exitFlag
		print('Start Response subprocess')
		self.startResponsePoll()

	def startResponsePoll(self):
		while not self.exitFlag.value:
			try:
				# Accept data from response queue in the following format:
				# Message to be sent
				# IP of the client
				# Port of the client
				data = self.responseQueue.get(block = False, timeout = 3)

				IP = data.get('IP', None)
				PORT = data.get('PORT', None)
				MESSAGE = data.get('MESSAGE', None)

				if IP == None or PORT == None or MESSAGE == None:
					print('[ WARNING ] Message is in wrong format : Discarding')
					# print("IP: ", IP, " Port: ", PORT, " MESSAGE: ", MESSAGE)

				else:
					print('\nSending a new message to client:', MESSAGE)
					# Create a new thread and send the message
					responseThread = threading.Thread(
						target = self.startResponseThread,
						args = (MESSAGE, IP, PORT,)
					)
					# Release resources after main program exits.
					responseThread.setDaemon(True)
					responseThread.start()
				
			except KeyboardInterrupt:
				self.exitFlag.value = 0
				return

			except Exception as e:
				# If queue is empty
				if "Empty" in str(e) or str(e) == '':
					pass
				else:
					print('[ GATEWAY ][ RESPONSE ] Error:', e)
					break

		# Wait for all active threads, or kill them if they are taking too long
		main_thread = threading.current_thread()		# We do not want to kill this thread itself.
		for t in threading.enumerate():
			if t is main_thread:
				continue
			print('Waiting for ', t.getName(), ' to close...')
			# Wait for 500ms for the thread to close.
			t.join(0.5)	

		# Inform Gateway of clean exit
		self.exitFlag.value = 0
		return

			
	def startResponseThread(self, MESSAGE, IP, PORT):
		# This Thread will try to send MESSAGE to IP:PORT 
		# In case of any error, it will retry two times and then discard the message.
		print('New response thread started to send:', MESSAGE, 'to', IP, ':', PORT)
		try:
			MESSAGE = json.dumps(MESSAGE)
		except:
			print('Error while converting message to JSON object.')
			return
		print('Connecting to ', IP, ':', PORT)
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				sock.connect((IP, PORT))
				sock.sendall(MESSAGE.encode('utf-8'))
			print('A new response has been sent to the client < ')
		except Exception as e:
			print('Error : Unable to send data to client:', e)