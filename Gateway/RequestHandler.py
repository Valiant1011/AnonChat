import socketserver
import threading

# The handle method is called everytime a new request appears, on a separate thread.
class RequestHandler(socketserver.BaseRequestHandler):
	# All incoming client requests are handled here:
	def handle(self):
		try:
			data = self.request.recv(4096).decode('utf-8')
		except:
			print('Error: Could not parse client data')
			return

		# Process data and do something with it

		cur_thread = threading.currentThread()
		response = cur_thread.getName() + ':' + data
		response = response.encode('utf-8')

		# Make an acknowledgement response and send it to client
		try:
			self.request.send(response)
		except:
			print('Error: Could not send response!')
		finally:
			return

		# This thread is closed here.