import socketserver
import threading

# The handle method is called everytime a new request appears, on a separate thread.
class RequestHandler(socketserver.BaseRequestHandler):
	# All incoming client requests are handled here:
	def handle(self):
		cur_thread = threading.currentThread()
		threadName = cur_thread.getName()

		try:
			data = self.request.recv(4096).decode('utf-8')
		except:
			print('Error: Could not parse client data')
			return

		# Get client INFO:
		self.clientAddress = self.request.getpeername()
		print('Client Address:', self.clientAddress)

		# Process data and do something with it

		
		response = "Server says: " + ':' + data + " from Thread: " + threadName
		response = response.encode('utf-8')

		# Make an acknowledgement response and send it to client
		try:
			self.request.send(response)
		except:
			print('Error: Could not send response!')
		finally:
			print('Thread:', threadName,' closed.')
			return

		# This thread is closed here.