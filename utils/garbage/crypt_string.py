from cryptography.fernet import Fernet

message = "u_giudimax"
fernet = Fernet('sJVhwvkUBwDaaZC014FEDQ0VXxA2ofZP0ZA8SCxmIOM=')
encMessage = fernet.encrypt(message.encode('utf8'))
print(encMessage)
decMessage = fernet.decrypt(encMessage).decode('utf8')
print(decMessage)