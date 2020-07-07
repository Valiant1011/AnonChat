"""
This class takes serial requests from REQUESTS queue, processes it, 
and sends the response to RESPONSE queue, which is handled by ResponseHandler subprocess.
"""
class ProcessRequest():
	def __init__(self, requestQueue, responseQueue, exitFlag):
		self.requestQueue = requestQueue
		self.responseQueue = responseQueue
		self.exitFlag = exitFlag

		print('Start ProcessRequest subprocess')
		self.startProcessPoll()

	def startProcessPoll(self):
		while not self.exitFlag.value:
			try:
				data = self.requestQueue.get(block = False, timeout = 3)
				self.processRequestData(data)
				
			except KeyboardInterrupt:
				self.exitFlag.value = 0
				return

			except Exception as e:
				# If queue is empty
				if "Empty" in str(e) or str(e) == '':
					pass
				else:
					print('[ GATEWAY ][ PROCESS REQUEST ] Error:', e)
					break

		# Inform Gateway of clean exit
		self.exitFlag.value = 0
		return

			
	def processRequestData(self, data):
		# print('Got a new message in request queue:', data)
		try:
			IP = data.get('IP')
			PORT = data.get('PORT')
			MESSAGE = "Hello dude!"

			response = {
				'MESSAGE' : MESSAGE,
				'IP' : IP,
				'PORT' : PORT
			} 
		except:
			print('Invalid request received. Discarded.')
		finally:
			self.responseQueue.put(response)