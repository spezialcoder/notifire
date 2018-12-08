#!/usr/lib/python
#Developer: developermind405@gmail.com
#Denied login: notifire request accept DENIED
#Accept login: notifire request accept OK
#Server available: notifire server OK
#Open Console session: notifire open session
#Open Session ok: notifire accept session
#Denied Session: notifire request session DENIED
#Close session: notifire close connection
import socket,sys,os,config_parse,hashlib,sqlite3,datetime,threading,useraccount,struct,time
require_config_tags = ["port","server_name","denied_user","listen","ip"]
connected = {}
################################################Functions####################################################
def write_fail(reason):
	with open("fail.log","a") as faillog:
			faillog.write("\n"+str(datetime.datetime.now())+"   "+reason)
			faillog.close()
################################################Loading Config###############################################
if os.path.isfile("notifire.conf"):
	try:
		config_values = config_parse.parse("notifire.conf").run()
		if not config_values["denied_user"].lower() == "none":
			duser = eval(config_values["denied_user"])
		else:
			duser = []
				
	except:
		with open("fail.log","a") as faillog:
			faillog.write("\n"+str(datetime.datetime.now())+"   Error parsing notifire.conf")
			faillog.close()
		print "Failed to start"
		sys.exit(0)
	for require in require_config_tags:
		if not require in config_values.keys():	
			with open("fail.log","a") as faillog:
				faillog.write("\n"+str(datetime.datetime.now())+"   Missing Data")
				faillog.close()
			print "Failed to start"
			sys.exit(0)	
else:
	
	with open("fail.log","a") as faillog:
				faillog.write("\n"+str(datetime.datetime.now())+"  Did not find notifire.conf")
				faillog.close()	
	print "Failed to start"
	sys.exit(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	sock.bind((config_values["ip"],int(config_values["port"])))
	sock.listen(int(config_values["listen"]))
except:	
	with open("fail.log","a") as faillog:
				faillog.write("\n"+str(datetime.datetime.now())+"  Server cannot start")
				faillog.close()	
	print "Failed to start"
	sys.exit(0)

def gvou(user):
	for i in user:
		with open("user/{0}".format(i),"r") as user_file:
			api_key = user_file.read()
			values = eval(api_key.decode("base64"))
			user_file.close()
		return values
if os.listdir("user/") == []:
	with open("fail.log","a") as faillog:
				faillog.write("\n"+str(datetime.datetime.now())+"  No Users created")
				faillog.close()	
	print "Failed to start"
	sys.exit(0)
user_list = map(gvou,[os.listdir("user/")])
def get_name(user):
	return user["name"]
raw_users = map(get_name,user_list)
secret_db = sqlite3.connect("secrets.db")
scursor = secret_db.cursor()
secrets_raw = eval(str(secret_db.execute("select * from secret").fetchall()))
secrets = {}
for secret in secrets_raw:
	secrets[str(secret[1])] = str(secret[0])
del secrets_raw
secret_db.close()
del secret_db
del scursor
cadmin = {}
def notify(message,user):
	len_str = struct.pack("!i",len(message))
	for client in connected.keys():
		client.send(len_str)
		time.sleep(0.1)
		client.send(message)
		client.send(user)

def session(c,a):
	session_run = True
	servern = config_values["server_name"]
	c.send(servern)
	while session_run:
		data = c.recv(1024).strip()
		if data == "notifire close connection":
			session_run = False
		elif data.startswith("send"):
			message = data.split("send ")[1]
			from_ = cadmin[c]
			notify(message,from_)
			c.send("\n\x1b[33m[+]Send Complete\x1b[39m")
		else:
			c.send("Command not found")
		
			
#####################################################Main-Loop########################################################
log_file = open("log/access.log","w")
while True:
	c,a = sock.accept()
	c.send("notifire server OK")
	log_file.write("\n"+str(datetime.datetime.now())+"    {0}      Connected to server".format(a[0]))
	log_file.flush()
	try:
		client_secret = c.recv(1024).strip()
		if client_secret == "notifire open session":
			name = c.recv(1024).strip()
			password = c.recv(1024).strip()
			if os.path.isfile("user/{0}".format(name)):
					with open("user/{0}".format(name),"r") as user_file:	
						try:
								request_user = eval(user_file.read().decode("base64"))	
								thep = request_user["password"]
								if password == thep:
									pass
									
								else:
									c.send("notifire request session DENIED")
									continue
						except:
							write_fail("Failed to find user")
							c.send("notifire request accept DENIED")
			else:
				c.send("notifire request session DENIED")
				continue
			
			
			if os.path.isfile("user/{0}".format(name)):
				with open("user/{0}".format(name),"r") as user_file:	
					try:
						request_user = eval(user_file.read().decode("base64"))	
						role = request_user["role"]
						if role["send"] == True and role["read"] == True and role["edit"] == True and not name in duser:
							c.send("notifire accept session")
							cadmin[c] = name
							cthread = threading.Thread(target=session,args=(c,a))
							cthread.daemon = True
							cthread.start()
						else:
							c.send("notifire request session DENIED")
					except:
						write_fail("Failed to find user")
						c.send("notifire request accept DENIED")
			else:
				c.send("notifire request accept DENIED")
					
		elif client_secret in secrets.keys():
			name = secrets[client_secret]
			connected[c] = name
			c.send("notifire request accept OK")
		else:
			c.send("notifire request accept DENIED")
	except:
		write_fail("Client broke the connection")
		
		
	
