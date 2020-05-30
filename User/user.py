import json

class User():
	def __init__(self):
		self.userID = ''
		self.userAlias = ''
		self.userPrestige = 0
		self.userMotto = ''
		self.memberSince = 'Eternity'
		self.userRep = 0
		self.userAvatar = 'Default'
		self.availableAvatars = []
		self.userProfileBG = ''
		self.availableBG = []
		self.userAvatarFrame = 'Default.png'
		self.availableFrames = []
		self.aboutMe = ''
		self.badges = {}
		self.comments = []	# List of dictionaries


		self.dictData = {}

	def loadUser(self):
		fileName = 'profile.json'
		try:
			with open(fileName, "r") as file:
				data = json.load(file)
				self.dictData = data
		except:
			pass
		else:
			self.loadDict(data)


	def loadDict(self, data):
		self.userID = data.get('userID', 'NULL')
		self.userAlias = data.get('userAlias', 'Newbie')
		self.userAvatar = data.get('userAvatar', 'Default')
		self.userProfileBG = data.get('userProfileBG', 'cyberpunk.jpeg')
		self.userPrestige = data.get('userPrestige', 0)
		self.userRep = data.get('userRep', 0)
		self.userMotto = data.get('userMotto', 'Am I Alive, or in an Illusion?')
		memberSince = data.get('memberSince', ['25', 'May', '2020'])
		self.memberSince = memberSince[1] + " " + memberSince[0] + ", " + memberSince[2] 
		self.aboutMe = data.get('aboutMe', '')
		self.badges = data.get('badges', [])
		self.comments = data.get('comments', [])
		self.userAvatarFrame = data.get('userAvatarFrame', 'Default.png')
		self.availableAvatars = data.get('availableAvatars', [])
		self.availableBG = data.get('availableBG', [])
		self.availableFrames = data.get('availableFrames', [])



	def saveChanges(self):
		fileName = 'profile.json'
		self.dictData['userMotto'] = self.userMotto
		self.dictData['aboutMe'] = self.aboutMe
		self.dictData['userAvatar'] = self.userAvatar
		self.dictData['userAvatarFrame'] = self.userAvatarFrame
		self.dictData['userProfileBG'] = self.userProfileBG
		try:
			with open(fileName, "w") as file:
				json.dump(self.dictData, file, indent = 4)
				
		except:
			pass
