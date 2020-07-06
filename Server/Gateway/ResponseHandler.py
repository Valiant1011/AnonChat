'''
This class accepts messages from Response queue
and sends a response to the client the message is intended for.
'''
class ResponseManager():
	def __init__(self, requestQueue, exitFlag):
		self.requestQueue = requestQueue
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
				data = self.requestQueue.get(block = False, timeout = 3)
				IP = data.get('IP', None)
				PORT = data.get('PORT', None)
				MESSAGE = data.get('MESSAGE', None)

				if IP == None or PORT == None or MESSAGE == None:
					print('[ WARNING ] Message is in wrong format : Discarding')
				else:
					# TODO : Do this in a thread
					self.startResponseThread(MESSAGE, IP, PORT)
			
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

		# Inform Gateway of clean exit
		self.exitFlag.value = 0
		return

			
	def startResponseThread(self, MESSAGE, IP, PORT):
		# This Thread will try to send MESSAGE to IP:PORT 
		# In case of any error, it will retry two times and then discard the message.
		pass