import multiprocessing
import os
import signal
import sys, time, pika, random
from interface import *
from connections import connection_manager

sys.path.append('../')

def main():
	random.seed(time.time())
	username = 'Admin'
	superuser_username = 'AnonChatAdmin'
	superuser_password = '$W_FNLU7Hp2-_dh'
	host = 'localhost'
	key = 'a8a1W2yuAVJMdmASDc'

	print('Hello', username)
	username = 'Admin'
	####################################################################
	# Create variables/lists that will be shared between processes
	flags = multiprocessing.Array('i', 10)
	flags[0] = 0
	flags[1] = 0
	flags[2] = 0
	# This queue will be polled from core for handling tasks
	task_queue = multiprocessing.Queue(maxsize = 1000)   
	####################################################################
	
	try:
		creds = pika.PlainCredentials(superuser_username, superuser_password)
		params = pika.ConnectionParameters(
			host = host, 
			virtual_host = 'chitchat',
			credentials = creds, 
			heartbeat=0, 
			blocked_connection_timeout=0
		)
		connection = pika.BlockingConnection(params)
		channel = connection.channel()
		channel1 = connection.channel()
		channel2 = connection.channel()

		channel.exchange_declare(
			exchange = 'group_chat_manager', 
			exchange_type = 'fanout', 
			durable = True
		)
		channel.exchange_declare(
			exchange = 'input_manager', 
			exchange_type = 'direct', 
			durable = True
		)
		queue_name = 'Admin'
		result = channel.queue_declare(queue = queue_name, durable = True)
		channel.queue_bind(exchange = 'input_manager', queue = queue_name)


	except Exception as error:
		print('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
		sys.exit()

	listen_process = multiprocessing.Process(
		target = connection_manager, 
		args = (
				flags, 
				task_queue, 
				username,
				channel1,
				queue_name,
				key, 
			)
	)
	listen_process.start()
	_pid = listen_process.pid
	
	# Initialize GUI handler
	try:
		init_gui(
			flags, 
			task_queue,
			channel2,
			key
		)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! Restart App." + str(error))

	# Shutdown server
	os.kill(_pid, signal.SIGINT)	
	while(flags[0] != 1):
		time.sleep(0.5)

	channel.close()
	channel1.close()
	channel2.close()
	connection.close()
	print('\nBella Ciao!')

if __name__ == '__main__':
	main()