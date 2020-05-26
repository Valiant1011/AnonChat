import json

class User():
	def __init__(self):
		self.userID = ''
		self.userAlias = ''
		self.userAvatar = ''
		self.userPrestige = 0
		self.userRep = 0
		self.userWallMessage = ''
		self.userMotto = ''
		self.memberSince = 'Eternity'
		self.aboutMe = ''
		self.badges = []

	def loadUser(self):
		fileName = 'profile.json'
		try:
			with open(fileName, "r") as file:
				data = json.load(file)
		except:
			pass
		else:
			self.userID = data.get('userID', 'NULL')
			self.userAlias = data.get('userAlias', 'Newbie')
			self.userAvatar = data.get('userAvatar', 'Default')
			self.userPrestige = data.get('userPrestige', 0)
			self.userRep = data.get('userRep', 0)
			self.userWallMessage = data.get('userWallMessage', '')
			self.userMotto = data.get('userMotto', '')
			self.memberSince = data.get('memberSince', 'Eternity')
			self.aboutMe = data.get('aboutMe', '')
			self.badges = data.get('badges', [])




	