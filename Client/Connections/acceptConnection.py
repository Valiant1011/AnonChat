import socket, time

"""
This class listens for any message from Server, and handles it accordingly.
"""
class ManageServerResponse():
	def __init__(self, recieverSocket, flags):
		self.recieverSocket  =recieverSocket
		self.flags = flags


	def recieveData(self):
		# This thread acts as a "Server" for our main server, as in it listens for 
		# socket requests from our main server, or Gateway to be precise, and accepts data from it.
		# The data is then passed on to a shared queue for further processing.
		print('[ CLIENT ] Started recieveing thread.')
		print('Client info: ', self.recieverSocket.getsockname())

		self.stopFlag = False
		
		while not self.stopFlag:
			if self.recieverSocket._closed == True:
				break

			# Every second, try to accept connection. This is done to prevent Thread blocking.
			r, w, e = select.select((self.recieverSocket,), (), (), 1)
			for l in r:
				conn, addr = self.recieverSocket.accept()
				# Check if the data is from the Server
				if addr[0] == self.serverIP:			
					with conn:
						self.processServerData(conn)
					
			else:
				if self.flags[0]:
					self.stopFlag = True
					break

		self.recieverSocket.close()
		print('[ CLIENT ] Stopped recieveing thread.')


