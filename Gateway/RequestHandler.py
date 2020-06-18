import socketserver
import threading, time, json

# The handle method is called everytime a new request appears, on a separate thread.
class RequestHandler(socketserver.BaseRequestHandler):
	# All incoming client requests are handled here:
	def handle(self):
		cur_thread = threading.currentThread()
		threadName = cur_thread.getName()

		# Get client INFO:
		self.clientAddress = self.request.getpeername()
		print('Client Address:', self.clientAddress)

		# Get client DATA:
		data = self.recvall(self.request)

		# Process the data sent by client
		try:
			response = self.processData(data)
			response = response.encode('utf-8')
		except Exception as error:
			print('Error while making response:', error)
			response = "NULL"

		# Send response to client
		try:
			self.request.send(response)
		except:
			print('Error: Could not send response!')
		finally:
			print('Thread:', threadName,' closed.')
			return

		# This thread is closed here.


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


	def processData(self, data):
		try:
			data = json.loads(data)
		except:
			print('JSON load error.')
			return "NULL"

		try:
			code = data.get("code", "NULL")
			if code == "NULL":
				return code
			elif code == "Login":
				print('Login Request')
				return self.processLogin(data)
			else:
				print('Invalid code')
				return "INVALID"
		except:
			print('Invalid message sent by client')
			return "INVALID"


	def processLogin(self, data):
		try:
			status = False
			username = data.get("username", "")
			password = data.get("password", "")
			
			if username == "" or password == "" :
				print('Invalid user details:', username, password)
				return "INVALID"

			# Validate Login
			status = True
			# Upto here
			# ------------------------------------
			
			# If request is valid, load the client's json data and send it to our client
			if status:
				# Get user data
				filename = "Users/" + username + '.json'
				with open(filename, 'r') as file:
					response = json.load(file)
				response = json.dumps(response)
				return response
			else:
				print('Login not verifed!')
				return "INVALID"
		except Exception as error:
			print('Error during login:', error)
			return "INVALID"
		


			