import multiprocessing, os, signal, sys, time 
from UI.ui import *

sys.path.append('../')
sys.path.append('./UI/')

def main():
	####################################################################
	# Create variables/lists that will be shared between processes
	flags = multiprocessing.Array('i', 10)
	# This queue will be polled from core for handling tasks
	taskQueue = multiprocessing.Queue(maxsize = 1000)   
	####################################################################
	# Tasks:
	# Login Process
		# - Status 1 : Continue
		# - Status 0 : Exit

	# Subprocesses:
		# - Interface
		# - Communications

	# Initialize Interface handler
	try:
		initGUI()
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! Restart App." + str(error))


if __name__ == '__main__':
	main()