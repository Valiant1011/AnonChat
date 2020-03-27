import multiprocessing
import os
import signal
import sys, time, pika, random
from interface import *
from connections import connection_manager

sys.path.append('../')

def main():
	random.seed(time.time())
	username = get_name()
	superuser_username = 'chitchat'
	superuser_password = 'chitchat'
	host = 'localhost'
	key = 'a8a1W2yuAVJMdmASDc'
	print('Hello', username)
	####################################################################
	# Create variables/lists that will be shared between processes
	flags = multiprocessing.Array('i', 10)
	flags[0] = 0
	flags[1] = 0
	flags[2] = 0
	flags[3] = 0	# Login flag
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

		result = channel.queue_declare(queue = '', durable = False)
		queue_name = result.method.queue
		channel.queue_bind(exchange = 'group_chat_manager', queue = queue_name)
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
			)
	)
	listen_process.start()
	_pid = listen_process.pid
	
	# Initialize GUI handler
	try:
		init_gui(
			flags, 
			task_queue,
			username,
			channel2,
			queue_name, 
			key
		)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! Restart App." + str(error))

	# Shutdown server
	os.kill(_pid, signal.SIGINT)	
	while(flags[0] != 1):
		time.sleep(0.5)

	channel.queue_delete(queue_name)
	channel.close()
	channel1.close()
	channel2.close()
	connection.close()
	print('\nBella Ciao!')

def get_name():
	names = [
		'Kiara','Adam','Sinnerman',
		'Lucifer','Chloe','Tokio',
		'Denver','Berlin','Professor',
		'Rio','Nairobi','Sheldon',
		'Penny','Leonard','Punisher'
	]
	return names[random.randint(0, len(names) - 1)]

if __name__ == '__main__':
	main()