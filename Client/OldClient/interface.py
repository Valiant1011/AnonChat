import time , sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from label import label
# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)

# This class handles the main window of server
class server_window(QMainWindow):
	def __init__(self, flags, task_queue, username, channel, queue, key):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('logo.png'))
		# Set window title
		self.setWindowTitle('AnonChat')
		self.setFixedSize(400, 600)
		self.setGeometry(700, 200, 400, 600) 

		self.flags = flags
		self.task_queue = task_queue
		self.username = username
		self.channel = channel
		self.number_of_chars_per_row = 25
		self.queue = queue
		self.key = key
		self.routing = 'Admin'
		self.ID = None
		self.password = None
		self.new_username = ''
		self.login()

		server_window.init_UI(self)

		# Timer to update GUI and broadcast scoreboard
		self.timer = QTimer()
		self.timer.timeout.connect(self.process_chats)
		self.timer.start(500)
		
		return

	def login(self):
		# Send joining message
		message = {
			'Code' : 'Login',
			'Key' : self.key,
			'Queue' : self.queue,
			'User' : self.username
		}
		message = json.dumps(message)
		self.channel.basic_publish(
			exchange = 'input_manager', 
			routing_key = self.routing, 
			body = message
		)
		
	def init_UI(self):
		try:
			self.head_widget = QWidget()
			self.head_layout = QHBoxLayout(self.head_widget)
			self.username_label = QLabel(self.username)
			self.username_label.setObjectName('h2')
			self.info_label = QLabel('?')
			self.info_label.setObjectName('h1')
			self.info_label.setToolTip(
				'Commands:\n' +
				'#dm Username Message : Send Private Message to Username\n' +
				'#clear : Clear the chat\n' + 
				'#exit : Exit\n' + 
				'#set Username : Set alias to Username\n' + 
				'Dev Profile: github.com/Valiant1011'

			)
			self.head_layout.addWidget(self.username_label)
			self.head_layout.addStretch(1)
			self.head_layout.addWidget(self.info_label)

			self.chat_widget = QWidget()
			self.chat_scroll_area = QScrollArea(self)
			self.chat_scroll_area.setMinimumSize(380, 480)
			self.chat_scroll_area.setWidgetResizable(True)
			self.chat_scroll_area.setWidget(self.chat_widget)
			self.scrollbar = self.chat_scroll_area.verticalScrollBar()
			self.scrollbar.rangeChanged.connect(self.move_scrollbar_to_bottom)
			self.chat_layout = QVBoxLayout(self.chat_widget)
			self.chat_layout.setAlignment(Qt.AlignBottom)
			
			self.reply_box = QLineEdit()
			self.reply_box.setReadOnly(True)
			self.reply_box.setText('Logging in...')
			self.reply_box.setPlaceholderText('What\'s on your mind?')
			self.reply_box.returnPressed.connect(self.user_input_handler)
			self.reply_box.setFixedSize(280, 30)
			self.reply_button = QPushButton('Send')
			self.reply_button.setObjectName('interior_button')
			self.reply_button.setFixedSize(75, 30)
			self.reply_button.clicked.connect(self.user_input_handler)
			self.reply_button.setDefault(True)
			self.bottom_layout = QHBoxLayout()
			self.bottom_layout.addWidget(self.reply_box)
			self.bottom_layout.addSpacing(5)
			self.bottom_layout.addWidget(self.reply_button)
			self.bottom_widget = QWidget()
			self.bottom_widget.setLayout(self.bottom_layout)
			
			self.top_layout = QVBoxLayout()
			self.top_layout.addStretch(1)
			self.top_layout.addWidget(self.head_widget)
			self.top_layout.addWidget(self.chat_scroll_area)
			self.top_layout.addStretch(90)
			self.top_layout.addWidget(self.bottom_widget)
			self.top_widget = QWidget()
			self.top_widget.setLayout(self.top_layout)
			self.top_widget.setObjectName("main_widget")

			# Set top_widget as our central widget
			self.setCentralWidget(self.top_widget)
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[ ERROR ] : ' , exc_type, fname, exc_tb.tb_lineno)
		return

	def move_scrollbar_to_bottom(self, min, max):
		self.chat_scroll_area.verticalScrollBar().setValue(max)
		return

	def clear_layout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

	@pyqtSlot()
	def user_input_handler(self):
		user_input = self.reply_box.text()
		if user_input == '':
			return

		self.reply_box.setText('')

		if user_input == '#clear':
			self.clear_layout(self.chat_layout)
			return
			
		elif user_input == '#exit':
			self.flags[2] = 1
			message = {
				'ID' : self.ID,
				'Password' : self.password,
				'Code' : 'Logout',
				'User' : self.username,
				'Message' : 'Left'
			}
			message = json.dumps(message)
			self.channel.basic_publish(
				exchange = 'input_manager', 
				routing_key = self.routing, 
				body = message
			)
			self.close()
			return
			
		elif len(user_input) > 5 and user_input[0:4] == '#set':
			old_username = self.username
			new_username = str(user_input[5:])
			self.new_username = new_username
			if(new_username == 'Admin'):
				return

			message = {
				'Code' : 'Alias',
				'User' : old_username,
				'ID' : self.ID,
				'Password' : self.password,
				'New' : new_username,
				'Message' : 'Changed alias to ' + self.username
			}
			message = json.dumps(message)
			self.channel.basic_publish(
				exchange = 'input_manager', 
				routing_key = self.routing, 
				body = message
			)
			return
			
			
		elif len(user_input) >len('#dm') and user_input[:3] == '#dm':
			try:
				rec = ''
				msg = ''
				new = user_input[4:]
				for i in range(len(new)):
					if new[i] != ' ':
						rec += new[i]
					else:
						msg = new[i:]
						break

				print('DM : ', msg, ':: TO ::', rec)
				if rec == '' or msg == '':
					print('Error: Improper usage of dm command')
					return

			except Exception as error:
				print('Error in dm: ', error)
				return
				
			else:
				message = {
					'Code' : 'DM',
					'ID' : self.ID,
					'To' : rec,
					'User' : self.username,
					'Password' : self.password,
					'Message' : msg
				}
				
				user_input = msg
				user_input = self.process_text(user_input)
				current_time = time.strftime('%H:%M:%S', time.localtime())
				user_input_label = label.get_widget(user_input, rec, current_time)
				user_input_label.setObjectName('user_input')

		else:	
			backup_text = user_input
			user_input = self.process_text(user_input)
			current_time = time.strftime('%H:%M:%S', time.localtime())
			user_input_label = label.get_widget(user_input, '', current_time)
			user_input_label.setObjectName('user_input')
		
			message = {
				'ID' : self.ID,
				'Password' : self.password,
				'Code' : 'Chat',
				'User' : self.username,
				'Message' : backup_text
			}

		message = json.dumps(message)
		self.channel.basic_publish(
			exchange = 'input_manager', 
			routing_key = self.routing, 
			body = message
		)

		self.chat_layout.addWidget(user_input_label)
		self.chat_layout.setAlignment(user_input_label, Qt.AlignRight)
		self.chat_layout.addSpacing(10)

		
	def process_chats(self):
		if self.flags[0] == 1:
			return

		while not self.task_queue.empty():
			data = self.task_queue.get()
			message = data['Message']
			sender = data['User']
			if sender == self.username:
				return

			if sender == 'Admin':
				code = data.get('Code', 'Chat')
				if code == 'Accept':
					self.flags[3] = 1
					self.ID = data['ID']
					self.password = data['Password']
					self.reply_box.setReadOnly(False)
					self.reply_box.setText('')

				elif code == 'Alias':
					print('Alias response received.')
					status = data['Status']
					if status == 1:
						self.username = self.new_username
						self.username_label.setText(self.username)
					else:
						pass

				elif code == 'Reject':
					self.flags[2] = 1
					print('[ LOGIN REJECTED ] :', message)
					self.close()
				elif code == 'Disc' and data['discUser'] == self.username:
					self.flags[2] = 1
					self.close()
				elif message == '#kill':
					self.flags[2] = 1
					self.close()

			reply = self.process_text(message)
			current_time = time.strftime('%H:%M:%S', time.localtime())
			reply_label = label.get_widget(reply, sender, current_time)
			
			if sender == 'Admin':
				reply_label.setObjectName('admin')	
			else:
				reply_label.setObjectName('response')

			self.chat_layout.addWidget(reply_label)
			self.chat_layout.setAlignment(reply_label, Qt.AlignLeft)
			self.chat_layout.addSpacing(10)

		number_of_widgets = self.chat_layout.count()
		if number_of_widgets > 100:
			child = self.chat_layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

	def process_text(self, text):
		new_text = ''
		words = list(text.split(' '))
		current_length = 0
		for word in words:
			word_length = len(word)
			if word_length > self.number_of_chars_per_row:
				for i in range(len(word)):
					if i % self.number_of_chars_per_row == 0:
						word = word[:i] + '\n' + word[i:]
				new_text += word
			elif word_length + current_length <= self.number_of_chars_per_row:
				new_text += ' ' + word
				current_length += word_length
			else:
				current_length = 0
				new_text += '\n' + word
				current_length += word_length
		return new_text[1:]

	def closeEvent(self, event):
		if self.flags[2] == 0:
			message = {
				'ID' : self.ID,
				'Password' : self.password,
				'Code' : 'Logout',
				'User' : self.username,
				'Message' : 'Left'
			}
			message = json.dumps(message)
			self.channel.basic_publish(
				exchange = 'input_manager', 
				routing_key = self.routing, 
				body = message
			)
		event.accept()
		
class init_gui(server_window):
	def __init__(self, flags, task_queue, username, channel, queue, key):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		server_app = server_window(flags, task_queue, username, channel, queue, key)
		server_app.show()
		server_app.reply_box.setFocus()
		# Execute the app mainloop
		app.exec_()
		return