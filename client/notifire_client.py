#Developer: developermind405@gmail.com
import socket,struct,notify,config_parse,os,sys,hashlib,getpass
osession = False
if len(sys.argv) > 1:
	parameter = sys.argv[1]
	if parameter == "--session":
		osession = True

else:
	pass
if os.path.isfile("notifire_client.conf"):
	config_values = config_parse.parse("notifire_client.conf").run()
else:
	print "\x1b[31m[-]Failed to locate config file\x1b[39m"
	sys.exit(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	sock.connect((config_values["ip"],int(config_values["port"])))
except:
	print "\x1b[31m[-]Failed to connect with server\x1b[39m"
	sys.exit(0)
answer = sock.recv(1024).strip()
if answer == "notifire server OK":
	pass
else:
	print "\x1b[31[-]Server not support notifire\x1b[39m"
	sys.exit(0)
if not osession:
	secret = config_values["secret"]
	sock.send(secret)
	answer = sock.recv(1024).strip()
	if answer == "notifire request accept OK":
		pass
	else:
		print "\x1b[31m[-]Login failed\x1b[39m"
		sys.exit(0)
	nheader = notify.notify("notifire")
	while True:
		len_data = sock.recv(4)
		len_str = struct.unpack("!i",len_data)[0]
		message = sock.recv(int(len_str)).strip()
		user = sock.recv(1024).strip()
		nheader.send(user,message)
else:
	sock.send("notifire open session")
	usernam = raw_input("User: ")
	passwd = hashlib.new("sha512",getpass.getpass("Enter Password: ")).hexdigest()
	sock.send(usernam)
	sock.send(passwd)
	answer = sock.recv(1024)
	if answer == "notifire accept session":
		print "Successful logged in"
		server_name = sock.recv(1024)
		myuser = usernam
		print 
		print "Welcome to notifire server: {0}".format(server_name)
		print
		session = True
		while session:
			command = raw_input(myuser+"@"+server_name+"# ")
			if command == "exit":
				sock.send("notifire close connection")
				sock.close()
				session = False
				sys.exit(0)
			try:
				sock.send(command)
				answer = sock.recv(1024)
				print answer
			except:
				print "\n\x1b[31m[-]Server broke connection\x1b[39m"	
				sys.exit(0)
	else:
		print "Access Denied"
