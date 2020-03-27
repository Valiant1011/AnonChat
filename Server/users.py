class users:
	users_dict = {}
	user_id_dict = {}
	key = ''
	clientID = 1
	def __init__(self, key):
		users.key = key

	def add_user(username, queue, password):
		if users.user_id_dict.get(username, -1) != -1:
			return -1

		cid = users.clientID
		users.users_dict[cid] = [username, queue, password]
		users.user_id_dict[username] = cid
		users.clientID += 1
		return cid
			
	def verify(ID, username, password):
		print('Verify ', username, '@', password)
		ulist = users.users_dict.get(ID, [])
		if len(ulist) == 0:
			return False
		if ulist[0] == username and ulist[2] == password:
			return True
		return False

	def disconnect(ID):
		username = users.users_dict[ID][0]
		users.users_dict[ID] = ['NULL', 'NULL', 'NULL']
		users.user_id_dict[username] = -1

	def alias(ID, new):
		if users.user_id_dict.get(new, -1) == -1:
			print('Alias', new, 'is Free.')

			old_uname = users.users_dict[ID][0]
			users.user_id_dict[old_uname] = -1

			users.users_dict[ID][0] = new
			users.user_id_dict[new] = ID
			return 1
		else:
			print('Alias', new, 'is Taken.')
			return 0

	def getQueue(username):
		cid = users.user_id_dict.get(username, -1)
		if cid == -1:
			return 'NULL'
		else:
			return users.users_dict[cid][1]