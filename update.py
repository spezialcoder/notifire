import urllib,json,sys,shutil,os,zipfile
try:
	with open("version.json","r") as cv:
		current = json.loads(cv.read())
		cv.close()
except:
	print "Missing version.json"
	sys.exit(0)
try:
	next = json.loads(urllib.urlopen("https://raw.githubusercontent.com/spezialcoder/notifire/master/version.json").read())[0]
except:
	print "No internet connection"
		
if float(next) > current[0]:
	print "New Version available"
	jn = raw_input("Download [j,n]")
	
	if jn.lower() == "j": 
		jbk = raw_input("Backup Config files? [j,n]")
		if jbk.lower() == "j":
			print "Init Backup..."
			os.mkdir("backup")
			shutil.copyfile("client/notifire_client.conf","backup/notifire_client.conf")
			shutil.copytree("user","backup/user")
			shutil.copyfile("secrets.db","backup/secrets.db")
			shutil.copyfile("notifire.conf","backup/notifire.conf")
			print "Backup finished"
			
		ls = os.listdir(os.getcwd())
		new_pack = urllib.urlopen("https://github.com/spezialcoder/notifire/archive/master.zip").read()
		print "Deleting old files..."
		gw = len(ls)
		count = 0
		for file in ls:
			count += 1
			prozent = str(int(float(100./gw)*count))+"%"
			if os.path.isdir(file) and not file == "backup":
				shutil.rmtree(file)
			else:
				if file != "backup":
					os.unlink(file)	
			print "Process: remove {0}   {1}".format(file,prozent)
		print "Finished"
		print "Installing new files"
		os.chdir("..")
		if jbk:
			os.mkdir("notibackup")
			shutil.copytree("notifire-master/backup","notibackup/backup")
		shutil.rmtree("notifire-master")
		with open("notifire.zip","w") as new:
			new.write(new_pack)
			new.close()
		zips = zipfile.ZipFile("notifire.zip")
		zips.extractall()
		print "Done"
		if jbk.lower() == "j":
			print "Configure"
			os.unlink("notifire-master/notifire.conf")
			os.unlink("notifire-master/client/notifire_client.conf")
			shutil.rmtree("notifire-master/user")
			shutil.copytree("notibackup/backup/user","notifire-master/user")
			shutil.copyfile("notibackup/backup/secrets.db","notifire-master/secrets.db")
			os.unlink("notifire-master/notifire.conf")
			shutil.copyfile("notibackup/backup/notfire.conf","notifire-master/notifire.conf")
			os.unlink("notifire-master/client/notifire_client.conf")
			shutil.copyfile("notibackup/backup/notifire_client.conf","notifire-master/client/notifire_client.conf")
			shutil.rmtree("notibackup")
			print "Done"
		shutil.rmtree("notibackup")
		os.unlink("notifire.zip")
		print 
		print "Sucessful installer notifire {0}".format(next)
else:
	print "No Update available"
		
	
