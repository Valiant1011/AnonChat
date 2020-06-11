import sys

class Console():
	def __init__(self):
		print('Preparing console...')
		self.exitFlag = False
		self.beginConsole()


	def beginConsole(self):
		try:
			while not self.exitFlag:
				adminInput = sys.stdin.readline() 
				self.process(adminInput)

		except KeyboardInterrupt:
			pass
		except EOFError:
			print('EOFError')
		except:
			print('Oops, something went wrong!')



	def process(self, adminInput):
		print('Processing : ', adminInput)
		if adminInput == 'exit':
			self.exitFlag = True
