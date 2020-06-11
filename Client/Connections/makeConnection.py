import json, socket

class MakeConnection():
	def __init__(self, flags):
		print('Connecting to server...')
		self.flags = flags
		self.load()


	def load(self):
		filename = 'Connections/session.json'
		with open(filename, 'r') as file:
			self.sessionData = json.load(file)

		self.ip = self.sessionData.get('ip', 'localhost')
		self.port = self.sessionData.get('port', None)

		print('Connecting to ', self.ip, ':', self.port)

		self.connect(self.ip, self.port, 'Hello server!!!')
		

	def connect(self, ip, port, message):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((ip, port))
			sock.sendall(bytes(message, 'utf-8'))

			response = str(sock.recv(1024), 'utf-8')
			print("Received: {}".format(response))

	def disconnect(self):
		pass


