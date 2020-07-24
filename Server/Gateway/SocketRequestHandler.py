import socketserver
import threading, time, json
from User import User

# The handle method is called everytime a new request appears, on a separate thread.
class RequestHandler(socketserver.BaseRequestHandler):
	# All incoming client requests are handled here:
	def handle(self):
		cur_thread = threading.currentThread()
		threadName = cur_thread.getName()

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
			code = data.get("code")
			if code == "Login":
				print('> Login Request')
				return self.processLogin(data)

			elif code == "Register":
				print('> Register request')
				return self.processRegisteration(data)

			elif code == "ProfileUpdate":
				print('> Profile Update request')
				return self.processProfileUpdate(data)

		except Exception as e:
			print('Invalid message sent by client:', data, '\nError:', e)
			return "INVALID"


	def authenticateUser(self, data):
		userID = data.get("userID", "")
		userName = data.get("userName", "")
		password = data.get("password", "")
		code = data.get("code", "NULL")
		IP = data.get('IP', '')
		PORT = data.get('PORT', '')

		if userName == "" or password == "" or userID == "" or code == "NULL":
			print('Invalid user details:', userID, userName, password)
			return False

		if IP == '' or PORT == '':
			print('Invalid connection details: IP or PORT is NULL')
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
			# The request is confirmed to be valid.
			print('[ LOGIN ] Success')
			# Put this request in server requestQueue for further processing
			message = {
				'IP' : data.get('IP'),
				'PORT' : data.get('PORT'),
				'Code' : 'Login',
				'userName' : userName,
				'userID' : userID
			}
			self.server.requestQueue.put(message)
			return "OK"
			
		except Exception as error:
			print('Error during login:', error)
			return "INVALID"
		

	def processRegisteration(self, data):
		userName = data.get("userName", "")
		password = self.Hash(data.get("password", ""))
		
		# Add user to database:
		userID = self.server.databaseManager.getNewUserID()
		status = self.server.databaseManager.addUser(userID, userName, password)	
		if not status:
			print('Could not register user.')
			# Username is taken.
			return "UsernameTaken"

		# User is added to the database now.
		# Make user profile:	
		user = User(userID, userName)	 # Makes user profile and maintains its dictionary
	
		# Send user profile to the client
		try:
			print('[ REGISTER ] Success')
			message = {
				'IP' : data.get('IP'),
				'PORT' : data.get('PORT'),
				'Code' : 'Login',
				'userName' : userName,
				'userID' : userID
			}
			self.server.requestQueue.put(message)

			return 'OK'
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
		except Exception as e:
			print('Error while processing request:', e)
			return 'ERROR'
