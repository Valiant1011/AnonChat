from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from editableLineEdit import editableLineEdit
from editableTextEdit import editableTextEdit
from prestigeWidget import prestigeWidget
from comment import Comment
from datetime import datetime

class ProfileWidget(QWidget):
	def __init__(self, userObject, viewer = ''):
		super().__init__()
		self.layout = self.getCentralLayout(userObject, viewer)
		self.layout.setContentsMargins(5, 5, 5, 5)
		self.setLayout(self.layout)
		

	def getCentralLayout(self, userObject, viewer):
		mainLayout = QVBoxLayout()

		header = self.makeHeader(userObject)
		badge = self.makeBadges(userObject)
		aboutMe = self.makeAboutMe(userObject)
		comments = self.makeComments(userObject, viewer)

		mainLayout.addWidget(header)
		mainLayout.addWidget(badge)
		mainLayout.addWidget(aboutMe)
		mainLayout.addWidget(comments)

		mainLayout.setAlignment(Qt.AlignTop)
		mainLayout.addStretch(1)
		mainLayout.setSpacing(10)
		mainLayout.setContentsMargins(0, 10, 0, 10)
		return mainLayout


	def makeHeader(self, userObject):
		# nameBox contains Prestige, Alias, Motto, Member Since and Reputation
		nameBox = QWidget()
		nameLayout = QVBoxLayout(nameBox)
		# Prestige Icon
		prestigeIcon = prestigeWidget(userObject.userPrestige)
		# User Alias label
		userAliasLabel = QLabel(userObject.userAlias)
		userAliasLabel.setObjectName('userAlias')
		userAliasWidget = self.getComboWidget(prestigeIcon, userAliasLabel)
		# User Motto label
		userMottoLabel = QLabel("' " + userObject.userMotto[:100] + " '")
		userMottoLabel.setObjectName('userMotto')
		# User Reputation label
		repLabel = QLabel('Reputation:')
		repLabel.setObjectName('repLabel')
		repContent = QLabel(userObject.userRep)
		repContent.setObjectName('repContent')
		repWidget = self.getComboWidget(repLabel, repContent)
		# User Member since label
		memberSinceLabel = QLabel('Member Since:')
		memberSinceLabel.setObjectName('memberSinceLabel')
		memberSinceContent = QLabel(userObject.memberSince)
		memberSinceContent.setObjectName('memberSinceContent')
		memberSinceWidget = self.getComboWidget(memberSinceLabel, memberSinceContent)
		# Add all these widgets into nameBox
		nameLayout.addWidget(userAliasWidget)
		nameLayout.addWidget(userMottoLabel)
		nameLayout.addStretch(1)
		nameLayout.addWidget(repWidget)
		nameLayout.addWidget(memberSinceWidget)
		nameLayout.setAlignment(userAliasWidget, Qt.AlignTop)
		nameLayout.setAlignment(userMottoLabel, Qt.AlignTop)
		nameLayout.setAlignment(repWidget, Qt.AlignBottom)
		nameLayout.setAlignment(memberSinceWidget, Qt.AlignBottom)

		# Edit Profile button
		editProfileButton = QPushButton('Edit Profile')
		editProfileButton.setFixedSize(100, 40)
		editContainer = QWidget()
		editContainerLayout = QHBoxLayout(editContainer)
		editContainerLayout.setContentsMargins(0, 0, 0, 0)
		editContainerLayout.setAlignment(Qt.AlignRight)
		editContainerLayout.addWidget(editProfileButton)
		# Avatar Image + Avatar Frame
		avatarImage = QLabel()
		avatarImage.setObjectName('avatarImage')
		avatarImage.setFixedSize(180, 180)
		avatarImageName = userObject.userAvatar
		avatar = QPixmap("Resources/Avatars/" + avatarImageName);
		scaled = avatar.scaled (180, 180)
		avatarImage.setPixmap(scaled)

		avatarBox = QWidget()
		avatarBox.setFixedSize(210, 210)
		avatarBox.setObjectName('avatarBox')
		avatarLayout = QVBoxLayout(avatarBox)
		avatarLayout.addWidget(avatarImage)
		avatarImage.lower()
		avatarLayout.setContentsMargins(15, 15, 15, 15)
		avatarLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
		try:
			userFrame = userObject.userAvatarFrame
			style = "QWidget#avatarBox{border-image : url(Resources/Frames/" + userFrame + ") 0 0 0 0 stretch stretch}"
			avatarBox.setStyleSheet(style)
		except:
			pass
		# Edit Button + Avatar Widget
		avatarContainer = QWidget()
		avatarContainerLayout = QVBoxLayout(avatarContainer)
		avatarContainerLayout.setContentsMargins(0, 0, 0, 0)
		avatarContainerLayout.addWidget(avatarBox)
		avatarContainerLayout.addWidget(editContainer)
		avatarContainerLayout.setAlignment(Qt.AlignTop)
		
		headerWidget = QWidget()
		headerWidget.setObjectName('headerBox')
		headerLayout = QHBoxLayout(headerWidget)
		headerLayout.addWidget(nameBox)
		headerLayout.addWidget(avatarContainer)
		headerLayout.setAlignment(nameBox, Qt.AlignLeft)
		headerLayout.setAlignment(avatarContainer, Qt.AlignRight)
		headerLayout.setStretch(0, 70)
		headerLayout.setStretch(1, 30)

		return headerWidget


	def makeBadges(self, userObject):
		overlayWidget = QWidget()
		overlayWidget.setObjectName('contentBox')
		overlayLayout = QHBoxLayout(overlayWidget)
		
		badgesLabelImage = QWidget()
		badgesLabelImage.setObjectName('badgesBox')
		badgesLabelImage.setFixedHeight(130)

		badgeWidget = QWidget()
		badgeLayout = QHBoxLayout(badgeWidget)
		badgeLayout.setContentsMargins(0, 0, 0, 0)

		badgeCount = 0
		for badgeName, badgeDesc in userObject.badges.items():
			newBadge = QLabel()
			try:
				badgeImage = QPixmap('Resources/Badges/' + badgeName + '.png')
				newBadge.setPixmap(badgeImage)
				newBadge.setToolTip(badgeDesc)
			except:
				pass
			else:
				badgeCount += 1
				badgeLayout.addWidget(newBadge)

		while badgeCount < 6:
			badgeCount += 1
			newBadge = QLabel()
			try:
				badgeImage = QPixmap('Resources/Badges/Empty.png')
				newBadge.setPixmap(badgeImage)
				badgeLayout.addWidget(newBadge)
			except:
				pass

		scrollableWidget = QScrollArea()
		scrollableWidget.setWidgetResizable(True)
		scrollableWidget.setWidget(badgeWidget)

		overlayLayout.addWidget(badgesLabelImage)
		overlayLayout.addWidget(scrollableWidget)
		overlayLayout.setStretch(0, 5)
		overlayLayout.setStretch(1, 95)
		overlayLayout.setContentsMargins(0, 0, 0, 0)

		return overlayWidget


	def makeAboutMe(self, userObject):
		overlayWidget = QWidget()
		overlayWidget.setObjectName('contentBox')
		overlayLayout = QHBoxLayout(overlayWidget)

		aboutImage = QWidget()
		aboutImage.setObjectName('aboutBox')
		aboutImage.setMinimumHeight(170)

		aboutLoopImage = QWidget()
		aboutLoopImage.setObjectName('aboutBoxLoop')
		aboutLoopImage.setMinimumHeight(0)

		aboutImageContainer = QWidget()
		aboutImageContainerLayout = QVBoxLayout(aboutImageContainer)
		aboutImageContainerLayout.addWidget(aboutImage)
		aboutImageContainerLayout.addWidget(aboutLoopImage)
		aboutImageContainerLayout.setContentsMargins(0, 0, 0, 0)
		aboutImageContainerLayout.setStretch(0, 10)
		aboutImageContainerLayout.setStretch(1, 90)
		aboutImageContainerLayout.setSpacing(0)
		
		aboutMeContent = QLabel(userObject.aboutMe)
		aboutMeContent.setAlignment(Qt.AlignTop)
		aboutMeContent.setObjectName('h4')

		overlayLayout.addWidget(aboutImageContainer)
		overlayLayout.addWidget(aboutMeContent)
		overlayLayout.setStretch(0, 5)
		overlayLayout.setStretch(1, 95)
		overlayLayout.setContentsMargins(0, 0, 0, 0)
		overlayLayout.setAlignment(Qt.AlignTop)
		return overlayWidget


	def makeComments(self, userObject, viewer):
		commentsHeading = QLabel('Comments')
		commentsHeading.setObjectName('commentsHeading')
		commentsHeading.setFixedHeight(40)
		commentsHeadingContainer = QWidget()
		commentsHeadingLayout = QHBoxLayout(commentsHeadingContainer)
		commentsHeadingLayout.addWidget(commentsHeading)
		commentsHeadingLayout.setAlignment(Qt.AlignCenter)
		commentsHeadingLayout.setContentsMargins(0, 10, 0, 0)

		comments = userObject.comments		
		commentWidget = QWidget()
		commentWidget.setMinimumHeight(380)
		self.commentLayout = QVBoxLayout(commentWidget)
		self.commentLayout.setAlignment(Qt.AlignTop)
		for comment in comments:
			commentItem = Comment(comment)
			self.commentLayout.addWidget(commentItem)

		self.addCommentEditor = QTextEdit()
		self.addCommentEditor.setPlaceholderText('Post a comment...')
		self.addCommentEditor.setMinimumHeight(50)
		self.addCommentEditor.setObjectName('addComment')
		addCommentButton = QPushButton('Post')
		addCommentButton.setFixedSize(50, 40)
		addCommentButton.clicked.connect(
			lambda:self.processNewComment(self.addCommentEditor.toPlainText(), viewer)
		)
		addCommentWidget = QWidget()
		addCommentLayout = QHBoxLayout(addCommentWidget)
		addCommentLayout.setContentsMargins(0, 0, 0, 0)
		addCommentLayout.addWidget(self.addCommentEditor)
		addCommentLayout.addWidget(addCommentButton)
		
		mainWidget = QWidget()
		mainLayout = QVBoxLayout(mainWidget)
		mainLayout.setContentsMargins(0, 0, 10, 0)
		mainLayout.addWidget(commentsHeadingContainer)
		mainLayout.addWidget(commentWidget)
		mainLayout.addWidget(addCommentWidget)
		mainLayout.setAlignment(addCommentWidget, Qt.AlignBottom)
		mainLayout.setStretch(0, 10)
		mainLayout.setStretch(1, 70)
		mainLayout.setStretch(2, 10)
		
		return mainWidget


	def processNewComment(self, text, viewer):
		time = datetime.today()
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
		fTime = [str(time.day), monthDict[time.month], str(time.year)]
		comment = {
			"commentUser" : viewer,
			"commentMessage" : text,
			"commentDate" : fTime
		}
		commentItem = Comment(comment)
		self.commentLayout.addWidget(commentItem)
		self.addCommentEditor.setText('')
		
		

		# TODO : Inform server of this event
		

	def getComboWidget(self, widget1, widget2, align = 'H'):
		widget = QWidget()
		if align == 'H':
			layout = QHBoxLayout(widget)
			layout.setAlignment(Qt.AlignLeft)
		else:
			layout = QVBoxLayout(widget)
			layout.setAlignment(Qt.AlignTop)
		layout.addWidget(widget1)
		layout.addWidget(widget2)
		layout.setContentsMargins(0, 0, 0, 0)
		return widget