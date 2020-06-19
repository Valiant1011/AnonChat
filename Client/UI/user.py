import json

class hasNotBeenLoadedError():
	def __init__(self):
		print('Error: The requested entity has not been loaded yet.')
		pass

class User():
	def __init__(self):
		self.userLoadedFlag = False
		self.friendsLoadedFlag = False
		self.userDataDict = {}
		self.friendDataDict = {}

	def loadUser(self):
		fileName = 'profile.json'
		try:
			with open(fileName, "r") as file:
				data = json.load(file)
				self.userDataDict = data
		except:
			data = {}
		finally:
			self.loadDict(data)


	def loadDict(self, data):
		self.userLoadedFlag = True
		self.friendsLoadedFlag = True

		self.userID = data.get('userID', 'NULL')
		self.userAlias = data.get('userAlias', 'Newbie')
		self.userAvatar = data.get('userAvatar', 'Default')
		self.userProfileBG = data.get('userProfileBG', 'cyberpunk.jpeg')
		self.userPrestige = data.get('userPrestige', '1')
		self.userRep = data.get('userRep', '1')
		self.userMotto = data.get('userMotto', 'Am I Alive, or in an Illusion?')
		memberSince = data.get('memberSince', ['25', 'May', '2020'])
		self.memberSince = memberSince[1] + " " + memberSince[0] + ", " + memberSince[2] 
		self.aboutMe = data.get('aboutMe', '')
		self.badges = data.get('badges', {})
		self.comments = data.get('comments', [])
		self.userAvatarFrame = data.get('userAvatarFrame', 'Default.png')
		self.availableAvatars = data.get('availableAvatars', [])
		self.availableBG = data.get('availableBG', [])
		self.availableFrames = data.get('availableFrames', [])
		self.friendData = data.get('friends', [])
		self.friendCount = len(self.friendData) 


	def saveChanges(self):
		fileName = 'profile.json'
		self.userDataDict['userMotto'] = self.userMotto
		self.userDataDict['aboutMe'] = self.aboutMe
		self.userDataDict['userAvatar'] = self.userAvatar
		self.userDataDict['userAvatarFrame'] = self.userAvatarFrame
		self.userDataDict['userProfileBG'] = self.userProfileBG
		try:
			with open(fileName, "w") as file:
				json.dump(self.userDataDict, file, indent = 4)
				
		except:
			pass

	# Getter functions
	def getFriendCount(self):
		if self.friendsLoadedFlag == True:
			return self.friendCount
		else:
			raise hasNotBeenLoadedError()

	def getFriends(self):
		if self.friendsLoadedFlag == True:
			return self.friendData
		else:
			raise hasNotBeenLoadedError()

	def getID(self):
		if self.userLoadedFlag == True:
			return self.userID
		else:
			raise hasNotBeenLoadedError()
			
	def getAlias(self):
		if self.userLoadedFlag == True:
			return self.userAlias
		else:
			raise hasNotBeenLoadedError()
	
	def getMotto(self):
		if self.userLoadedFlag == True:
			return self.userMotto
		else:
			raise hasNotBeenLoadedError()

	def setMotto(self, Motto):
		self.userMotto = Motto

	def getAvatar(self):
		if self.userLoadedFlag == True:
			return self.userAvatar
		else:
			raise hasNotBeenLoadedError()

	def setAvatar(self, Avatar):
		self.userAvatar = Avatar
		
	def getProfileBG(self):
		if self.userLoadedFlag == True:
			return self.userProfileBG
		else:
			raise hasNotBeenLoadedError()

	def setProfileBG(self, ProfileBG):
		self.userProfileBG = ProfileBG

	def getPrestige(self):
		if self.userLoadedFlag == True:
			return self.userPrestige
		else:
			raise hasNotBeenLoadedError()

	def getRep(self):
		if self.userLoadedFlag == True:
			return self.userRep
		else:
			raise hasNotBeenLoadedError()

	def getMemberSince(self):
		if self.userLoadedFlag == True:
			return self.memberSince
		else:
			raise hasNotBeenLoadedError()

	def getAboutMe(self):
		if self.userLoadedFlag == True:
			return self.aboutMe
		else:
			raise hasNotBeenLoadedError()

	def setAboutMe(self, AboutMe):
		self.aboutMe = AboutMe
			
	def getBadges(self):
		if self.userLoadedFlag == True:
			return self.badges
		else:
			raise hasNotBeenLoadedError()
	
	def getComments(self):
		if self.userLoadedFlag == True:
			return self.comments
		else:
			raise hasNotBeenLoadedError()
	
	def getAvatarFrame(self):
		if self.userLoadedFlag == True:
			return self.userAvatarFrame
		else:
			raise hasNotBeenLoadedError()

	def setAvatarFrame(self, AvatarFrame):
		self.userAvatarFrame = AvatarFrame

	def getAvailableAvatars(self):
		if self.userLoadedFlag == True:
			return self.availableAvatars
		else:
			raise hasNotBeenLoadedError()
	
	def getAvailableBG(self):
		if self.userLoadedFlag == True:
			return self.availableBG
		else:
			raise hasNotBeenLoadedError()
	
	def getAvailableFrames(self):
		if self.userLoadedFlag == True:
			return self.availableFrames
		else:
			raise hasNotBeenLoadedError()	