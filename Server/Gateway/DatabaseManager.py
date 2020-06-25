import sqlite3

class DatabaseManager():
	def __init__(self):
		self.allOKFlag = True
		try:
			self.dbConnection = sqlite3.connect(
					"clients.db",
					check_same_thread = False,
					timeout = 1
				)
		except Exception as error:
			print('[ DB ][ ERROR ] Could not connect to database:', error)
			self.allOKFlag = False

		self.cursor = self.dbConnection.cursor()
		self.initTables()


	def initTables(self):
		try:	
			self.dbConnection.execute(
				"CREATE TABLE IF NOT EXISTS accounts(userID INTEGER PRIMARY KEY, userName VARCHAR2(20), password VARCHAR2(100));"
				)
			self.dbConnection.commit()
		except Exception as error:
			print('[ DB ][ ERROR ] Could not initialise table:', error)
			self.allOKFlag = False


	def checkStatus(self):
		return self.allOKFlag


	def getNewUserID(self):
		try:
			self.cursor.execute("SELECT MAX(userID) FROM accounts;")
			data = self.cursor.fetchall()
			if data == None or len(data) == 0 or data[0][0] == None:
				userID = 1
			else:
				userID = int(data[0][0]) + 1
			return userID
		except:
			return 0


	def addUser(self, userID, userName, password):
		try:
			# Check if the username is unique:
			self.cursor.execute("SELECT userName FROM accounts WHERE userName = ?;", (userName,))
			data = self.cursor.fetchall()
			if not len(data) == 0:
				return False

			self.dbConnection.execute(
					"INSERT INTO accounts VALUES(?, ?, ?);", 
					(userID, userName, password,)
				)
			self.dbConnection.commit()
		except Exception as error:
			print('[ DB ][ ERROR ] Could not add db entry:', error)
			return False
		else:
			return True


	def authenticateUser(self, userID, userName, password):
		try:
			self.cursor.execute(
					"SELECT * FROM accounts WHERE userName = ? AND password = ?;", 
					(userName, password)
				)
			data = self.cursor.fetchall()
			if len(data):
				return True
			else:
				return False
		except Exception as e:
			print('[ DB ][ QUERY ][ ERROR ]:', e)
			return False


	def closeConnection(self):
		print('[ DB ] Closing connection.')
		self.dbConnection.close()


	def sayHi(self):
		print('Hiiiii!')