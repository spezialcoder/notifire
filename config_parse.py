import os,string
#Config Parser
#Developer: developermind405@gmail.com
#####################################################Exceptions#########################################################
class ParseError(Exception):
	def __init__(self,reason):
		self.reason = reason
	def __str__(self):
		return self.reason
nonas = ["-","_","+","*",",",":","(",")","&","$","!","[","]","%","0","1","2","3","4","5","6","7","8","9"]
#######################################################################################################################
class parse:
	def __init__(self,file):
		self.file = file
		self.values = {}
	
	def run(self):
		if os.path.isfile(self.file):
			with open(self.file,"r") as config:
				all_lines = config.readlines()
				for line in all_lines:
					line = line.strip()
					ok = False
					for parseme in line:
						if parseme in string.ascii_letters or parseme in nonas:
							ok = True
					if not  ok:
						continue
					if line.startswith("#"):	
						pass
					else:
						config_name = ""
						for name in line:
							if not name == " ":
								config_name += name
							else:
								break
						try:
							the_rest = line.split(config_name)[1]
							try:
								the_rest = the_rest.split("=")[1]
							except:
								pass
							whitespace = True
							while whitespace:
								try:
									the_rest = the_rest.split(" ")[1]
								except:
									whitespace = False
						except:
							raise ParseError("Error Parsing,invailed config")
							
						self.values[config_name] = the_rest
				config.close()
			return self.values
		else:
			raise IOError("File not exist")
						
		
