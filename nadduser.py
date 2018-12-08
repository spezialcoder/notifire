import sys,sqlite3,useraccount,os
print len(sys.argv)
if len(sys.argv) == 3 and sys.argv[1] == "--delete":
	user = sys.argv[2]
	if os.path.isfile("user/{0}".format(user)):
		jn = raw_input("Really Delete? [j,n]")
		if jn.lower() == "j":
			if os.path.isfile("secrets.db"):
				db = sqlite3.connect("secrets.db")
				cursor = db.cursor()
				cursor.execute("delete from secret where User='{0}';".format(user))
				db.commit()
				db.close()
			os.unlink("user/{0}".format(user))
			print "Successful Delete"
		else:
			pass
elif len(sys.argv) == 4:
	name = sys.argv[1]
	role = sys.argv[2]
	password = sys.argv[3]
	new_user = useraccount.User(name,role,password)	
	jn = raw_input("Save? [j,n]")
	if jn.lower() == "j":
		if os.path.isfile("secrets.db"):
			db = sqlite3.connect("secrets.db")
			cursor = db.cursor()
			cursor.execute("insert into secret values('{0}','{1}')".format(name,new_user.secret))
			db.commit()
			db.close()
		with open("user/{0}".format(name),"w") as file:
			file.write(new_user.convert())
			file.close()
		print "Successful Created"
		print "Secret:",new_user.secret
	else:
		pass
else:
	print "Missing parameter: python nadduser.py <name> <role> <password>"
