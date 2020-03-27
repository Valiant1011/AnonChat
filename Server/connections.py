import sys, time, pika, json, random, string
from users import users

class connection_manager():
	def __init__(self, flags, task_queue, username, channel, queue, key):
		self.flags = flags
		self.task_queue = task_queue
		self.username = username
		self.channel = channel
		self.queue = queue
		self.key = key
		self.listen_clients()
		
	def listen_clients(self):
		try: 
			self.channel.basic_consume(
				queue = self.queue, 
				on_message_callback = self.handler,
				auto_ack = True
			)
			self.channel.start_consuming()
		# Handle keyboard interrupt ctrl+c and terminate successfully
		except (KeyboardInterrupt, SystemExit):
			self.channel.stop_consuming()
		except Exception as error: 
			print('Connection Error: ', error)
		finally: 
			self.flags[0] = 1
			return

	def handler(self, ch, method, properties, body):
		try:
			message = str(body.decode('utf-8'))
			# Send the message to interface
			message = json.loads(message)

			code = message.get('Code', 'Chat')
			username = message.get('User', 'NULL')

			if code == 'Login':
				key = message['Key'] 
				queue = message['Queue']  
				if key == self.key:
					chars = 'abcdefghjABCDEFGHIJ123456789'
					password = ''.join(random.choice(chars) for _ in range(6))
					clientID = users.add_user(username, queue, password)
					if clientID == -1:
						message = {
							'Code' : 'Reject',
							'User' : 'Admin',
							'Message' : 'Multiple Logins are not allowed!'
						}
						
					else:	
						message2 = {
							'Code' : 'Login',
							'Queue': queue,
							'User' : username,
							'Message' : 'Joined'
						}
						self.task_queue.put(message2)
						self.broadcast(message2)

						message = {
							'Code' : 'Accept',
							'ID' : clientID,
							'User' : 'Admin',
							'Message' : 'Hello ' + username,
							'Password' : password
						}
						
				else:
					message = {
						'Code' : 'Reject',
						'User' : 'Admin',
						'Message' : 'Login Failed'
					}
					
				self.unicast(message, queue)
				return

			ID = message.get('ID', 0)
			password = message.get('Password', 'NULL')

			if code == 'Logout':
				if users.verify(ID, username, password):
					users.disconnect(ID)
					message2 = {
						'Code' : 'Logout',
						'User' : username,
						'Message' : message['Message']
					}
					self.task_queue.put(message2)
					self.broadcast(message2)
					
			elif code == 'Chat':
				if not users.verify(ID, username, password):
					return

				self.task_queue.put(message)
				# Broadcast this message to all clients
				self.broadcast(message)

			elif code == 'Alias':
				if users.verify(ID, username, password):
					queue = users.getQueue(username)
					newU = str(message.get('New', 'Noob'))
					status = users.alias(ID, newU)
					if status:
						message2 = {
							'User' : 'Admin',
							'Code' : 'Alias',
							'Status' : 1,
							'Message' : 'Alias Accepted!'
						}
						self.unicast(message2, queue)

						message2 = {
							'Code' : 'Alias',
							'New' : newU,
							'User' : username,
							'Message' : 'Changed alias to ' + newU
						}
						self.task_queue.put(message2)
						self.broadcast(message2)

					else:
						message2 = {
							'Code' : 'Alias',
							'User' : 'Admin',
							'Status' : 0,
							'Message' : 'Alias is already taken!'
						}
						self.unicast(message2, queue)


			elif code == 'DM':
				mTo = message.get('To', '')
				mContent = message.get('Message', '')

				if not users.verify(ID, username, password):
					return

				if mTo == '' or mContent == '':
					return

				print('DM from', username, 'to', mTo, ' : ', mContent)
				if mTo == 'Admin':
					queue = 'Admin'
				else:
					queue = users.getQueue(mTo)
					if queue == 'NULL':
						return
				
				message2 = {
					'Code' : 'SelfDM',
					'User' : username,
					'Message' : mContent
				}
				self.unicast(message2, queue)

			elif code == 'SelfDM':
				self.task_queue.put(message)
					
		except Exception as error:
			print('Error: ', error)

	def broadcast(self, message):
		message = json.dumps(message)
		self.channel.basic_publish(
			exchange = 'group_chat_manager', 
			routing_key = '', 
			body = message
		)

	def unicast(self, message, queue):
		message = json.dumps(message)
		self.channel.basic_publish(
			exchange = 'input_manager', 
			routing_key = queue, 
			body = message
		)
