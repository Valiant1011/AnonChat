class ResponseManager():
	def __init__(self, requestQueue, exitFlag):
		self.requestQueue = requestQueue
		self.exitFlag = exitFlag
		print('Start response process')
		self.startResponsePoll()

	def startResponsePoll(self):
		while not self.exitFlag.value:
			try:
				data = self.requestQueue.get(block = False, timeout = 3)
				self.processResponseData(data)
			
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

			
	def processResponseData(self, data):
		if data == 'EXIT':
			return

		print(data)