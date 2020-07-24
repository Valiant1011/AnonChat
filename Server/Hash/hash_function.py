
class Hash:

	#function to return hash of a string 
	def hash_function(password):
		final_hash = ""                                    # will contain the final hash created

		ord_encryption = 0
		for i in range(len(password)):
			ord_encryption += ord(password[i])
			final_hash += str(ord(password[i])%len(password))

		value_encrypting = 0
		get_encrypted_value_string = ""
		for i in range(1,len(password)):
			value_encrypting += max(ord(password[i]),ord(password[i-1])) - min(ord(password[i]),ord(password[i-1]))
			temp = max(ord(password[i]),ord(password[i-1])) - min(ord(password[i]),ord(password[i-1]))
			value_temp = max(ord(password[i]),ord(password[i-1])) - min(ord(password[i]),ord(password[i-1]))
			if(value_temp > 32 and value_temp < 128):
				pass
			if(value_temp > 128):
				value_temp %= 128
			if(value_temp < 33):
				value_temp += 33
			get_encrypted_value_string += chr(value_temp)

		final_hash = str(ord_encryption) + final_hash + get_encrypted_value_string + str(value_encrypting)

		satisy_len = len(final_hash)
		if(satisy_len < 64):
			back = (64 - satisy_len)//2
			front = (64 - satisy_len) - back
			for i in range(1,front):
				final_hash = chr(128 - i) + final_hash
			for i in range(1,back):
				final_hash = final_hash + chr(32 + i)

		if(satisy_len > 64):
			print(satisy_len)
			if(satisy_len%2):
				final_hash = final_hash[:64]
			else:
				final_hash = final_hash[len(final_hash):len(final_hash)-65:-1]
			print(len(final_hash))

			
		return final_hash

