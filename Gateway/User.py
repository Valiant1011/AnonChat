import json, datetime
class User():
	def __init__(self, userID, userName):
		self.userID = userID
		self.userName = userName
		self.makeUser()

	def makeUser(self):
		try:
			self.data = self.makeDict()
			fileName = "Users/" + self.userName + '.json'
			with open(fileName, "w") as file:
				json.dump(self.data, file, indent = 4)

		except Exception as e:
			print('Error while creating file:', e)
			self.data = {}

	def getData(self):
		return self.data


	def makeDict(self):
		time = datetime.datetime.today()
		monthDict = {
			1:"January",
			2:"February",
			3:"March",
			4:"April",
			5:"May",
			6:"June",
			7:"July",
			8:"August",
			9:"September",
			10:"October",
			11:"November",
			12:"December"
		}
		memberSince = [str(time.day), monthDict[time.month], str(time.year)]

		data = {}
		data["userID"] = self.userID
		data["userAlias"] = self.userName
		data["userAvatar"] = 'Default'
		data["userProfileBG"] = 'Cyberpunk.jpeg'
		data["userPrestige"] = '1'
		data["userRep"] = '1'
		data["userMotto"] = "Hey, I'm new here!"
		data["memberSince"] = memberSince[1] + " " + memberSince[0] + ", " + memberSince[2] 
		data["aboutMe"] = ''
		data["badges"] = {}
		data["comments"] = []
		data["userAvatarFrame"] = 'Default.png'
		data["availableAvatars"] = ['Default']
		data["availableBG"] = ['Cyberpunk.jpeg']
		data["availableFrames"] = ['Default.png']
		data["friendData"] = []
		data["friendCount"] = 0
		return data
