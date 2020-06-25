import socketserver
import threading, time, json
from Gateway.User import User

# The handle method is called everytime a new request appears, on a separate thread.
class RequestHandler(socketserver.BaseRequestHandler):
	# All incoming client requests are handled here:
	def handle(self):
		cur_thread = threading.currentThread()
		threadName = cur_thread.getName()

		# # Check DB connection:
		# self.server.databaseManager.sayHi()	

		# Get client INFO:
		self.clientAddress = self.request.getpeername()
		print('\nNew request from >', self.clientAddress[0], ':', self.clientAddress[1])

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
		# Convert JSON data to python dict
		try:
			data = json.loads(data)
		except:
			print('JSON load error.')
			return "ERROR"

		# Authenticate request
		try:
			status = self.authenticateUser(data)
			if not status:
				print('[ REQUEST ] Authentication Failed')
				return "INVALID"
			else:
				pass
		except Exception as e:
			print('Error while Authentication:', e)
			return "INVALID"

		# Pass the request to its handler function
		try:
			code = data.get("code", "NULL")
			if code == "NULL":
				return "NULL"

			elif code == "Login":
				print('Login Request')
				return self.processLogin(data)

			elif code == "Register":
				print('Register request')
				return self.processRegisteration(data)

			elif code == "ProfileUpdate":
				return self.processProfileUpdate(data)

			else:
				print('Client sent:', data)
				# Send data to Server for processing
				self.server.requestQueue.put(data)
				if code in []:
					return "WAIT"		# Ask client to resume as normal
				else:
					return "OK"   # Ask client to wait

		except Exception as e:
			print('Invalid message sent by client:', e)
			return "INVALID"


	def authenticateUser(self, data):
		userID = data.get("userID", "")
		userName = data.get("userName", "")
		password = data.get("password", "")
		code = data.get("code", "NULL")

		if userName == "" or password == "" or userID == "":
			print('Invalid user details:', userID, userName, password)
			return False

		if code == "Register":
			# A new registeration need not be checked in database.
			return True
		# For all other requests, the client must be present in the database

		# Hash the password
		password = self.Hash(password)

		return self.server.databaseManager.authenticateUser(userID, userName, password)	


	def Hash(self, password):
		# TODO
		return password


	def processLogin(self, data):
		userID = data.get("userID", "")
		userName = data.get("userName", "")
		password = data.get("password", "")

		try:
			# The request is confirmed to be valid. So send client data.
			# Get user data
			print('[ LOGIN ] Success')
			filename = "Users/" + userName + '.json'
			with open(filename, 'r') as file:
				response = json.load(file)
			response = json.dumps(response)
			return response
			
		except Exception as error:
			print('Error during login:', error)
			return "INVALID"
		

	def processRegisteration(self, data):
		userName = data.get("userName", "")
		password = data.get("password", "")
		# Hash the password
		password = self.Hash(password)

		# Add user to database:
		userID = self.server.databaseManager.getNewUserID()
		status = self.server.databaseManager.addUser(userID, userName, password)	
		if not status:
			print('Could not register user.')
			# Username is taken.
			return "UsernameTaken"

		# User is added to the database now.
		# Make user profile:	
		user = User(userID, userName)	# Makes user profile and maintains its dictionary
		data = user.getData()
	
		# Send user profile to the client
		try:
			print('[ REGISTER ] Success')
			response = json.dumps(data)
			return response
		except Exception as error:
			print('Error during registeration:', error)
			return "NULL"


	def processProfileUpdate(self, data):
		motto = data.get('motto', 'NULL')
		avatar = data.get('avatar', 'NULL')
		frame = data.get('frame', 'NULL')
		bg = data.get('bg', 'NULL')
		about = data.get('about', 'NULL')
		userName = data.get('userName', 'NULL')

		try:
			filename = "Users/" + userName + '.json'
			with open(filename, 'r') as file:
				data = json.load(file)
			data['userAvatar'] = avatar
			data['userProfileBG'] = bg
			data['userAvatarFrame'] = frame
			data['userMotto'] = motto
			data['aboutMe'] = about

			with open(filename, 'w') as file:
				json.dump(data, file, indent = 4)

			return 'OK'
		except:
			return 'ERROR'
