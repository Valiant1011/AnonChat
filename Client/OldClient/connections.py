import sys, time, pika, json

class connection_manager():
	def __init__(self, flags, task_queue, username, channel, queue):
		self.flags = flags
		self.task_queue = task_queue
		self.username = username
		self.channel = channel
		self.queue = queue
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
		message = str(body.decode('utf-8'))
		message = json.loads(message)
		code = message.get('Code', 'Chat')
		self.task_queue.put(message)

