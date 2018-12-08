#Developer: developermind405@gmail.com
import hashlib,os,random,string

class User:
	def __init__(self,name,role,password):
		self.name = name
		self.role = role
		self.secret = ""
		for i in range(0,30):
			rand = random.choice(string.ascii_letters)
			self.secret += rand
		self.secret = self.secret.encode("hex")
		if os.path.isfile("role/{0}".format(self.role)):
			with open("role/{0}".format(self.role),"r") as role_file:
				index = role_file.read()
				self.role = eval(index.strip().decode("hex"))
				role_file.close()
		self.password = hashlib.new("sha512",password).hexdigest()
		self.values = {"name" : self.name,"role" : self.role,"password" : self.password}

	def convert(self):
		return str(self.values).encode("base64")
class role:
	def __init__(self,send,read,edit):
		self.send = send
		self.read = read
		self.edit = edit
		self.result = {"send" : self.send,"read" : self.read,"edit" : self.edit}

	def convert(self):
		self.key = str(self.result).encode("hex")
		return self.key

	
		
