'''
Created on 01.09.2013

@author: christopher
'''

import os
import sys
import urllib
import types

serverURL = "https://s3.amazonaws.com/Minecraft.Download/versions/1.6.2/minecraft_server.1.6.2.jar"

class MinecraftServerManager:

	def __init__(self):
		self.mainDirectory = os.path.expanduser("~") + os.sep + "MinecraftServer"
		self.serverDirectory = ""
		self.executablePath = ""
		
		self.servers = []

	'''
	downloads a file from the internet via its URL
	'''
	def download(self, url):
		dl_fileName = url.split('/')[-1]
		webFile = urllib.urlopen(url)
		localFile = open(self.mainDirectory + os.sep + dl_fileName, "w")
		localFile.write(webFile.read())
		webFile.close()
		localFile.close()

	'''
	creates a new server subdirectory in ~/MinecraftServer
	'''
	def createNewServerDir(self):
		dirName = raw_input("Prompt a name > ")
		self.serverDirectory = self.mainDirectory + os.sep + dirName
		os.mkdir(self.serverDirectory)

	'''
	main dialog
	'''  
	def chooseServer(self):
		choice = raw_input("miner's choice > ")
		try:
			choice = int(choice)
		except:
			pass
		if type(choice) == types.IntType:
			if choice in range(len(self.servers)):
				name = self.servers[choice]
				self.serverDirectory = self.mainDirectory + os.sep + name
			else:
				print "the selected server does not exist, try again"
				self.chooseServer()
		elif type(choice) == types.StringType:
			if choice == "n":
				self.createNewServerDir()
			elif choice == "x":
				print "okay, bye"
				sys.exit(0)
			else:
				print "invalid input, try again"
				self.chooseServer()

	'''
	starts the minecraft server in directory ~/MinecraftServer/[serverDirectory]
	'''
	def startServer(self):
		os.chdir(self.serverDirectory)
		os.system("java -Xmx1024M -Xms1024M -jar " + self.executablePath + " nogui")

	def main(self):
		# checks if directory "MinecraftServer" exists in your home directory
		if not os.path.exists(self.mainDirectory):
			print "create server directory: " + self.mainDirectory
			os.mkdir(self.mainDirectory)
		
		# lists the content of your server directory
		dirContent = os.listdir(self.mainDirectory)
		serverFileExists = False
		
		# sorts entrys of your server directory by type
		for entry in dirContent:
			if not entry.startswith(".") and not entry.endswith(".jar") \
											and not entry.endswith(".py"):
				self.servers.append(entry)
			if entry.endswith(".jar"):
				serverFileExists = True
				self.executablePath = self.mainDirectory + os.sep + entry
				
		if not serverFileExists:
			print "seems you have no server installed, let me do that for you..."
			self.download(serverURL)
			self.executablePath = self.mainDirectory + os.sep + serverURL.split("/")[-1]
		
		if len(self.servers) > 0:
			print "Hello Miner! Which server should I start for you?"
			for i in range(len(self.servers)):
				print "[" + str(i) + "] " + self.servers[i]
			print "[n] create a new one"
			print "[x] exit"
			self.chooseServer()
		else:
			print "Hello Miner! Just create a new server and get started!"
			self.createNewServerDir()
		
		self.startServer()
	
if __name__ == "__main__":
	MinecraftServerManager().main()