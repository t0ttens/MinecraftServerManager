'''
Created on 01.09.2013

@author: christopher
'''

import os
import sys
import urllib
import types



class MinecraftServerManager:

	def __init__(self):
		self.mainDirectory = os.path.expanduser("~") + os.sep + "MinecraftServer"
		self.serverDirectory = ""
		self.ramString = ""
		self.executablePath = ""
		
		self.servers = []
		
		self.currentServerVersion, self.serverURL = self.getVersion()

	'''
	creates a string like '[------         ] 35%' which shows progress
	'''
	def getProgressString(self, percent):
		length = 50
		out = "["
		ticks = int(percent/(float(100)/length))
		for i in range(ticks):
			out += "-"
		for i in range(length-ticks):
			out += " "
		out += "]\t" + str(percent) + "%"
		return out
	
	'''
	check the latest server version on minecraft.net and its download url
	'''
	def getVersion(self):
		lines = urllib.urlopen("https://minecraft.net/de-de/download/server").readlines()
		version = 0
		downloadUrl = ""
		for i in range(len(lines)):
			if lines[i].find("https://s3.amazonaws.com/Minecraft.Download/versions/") > 0:
				leftBound = lines[i].find("versions/") + 9
				rightBound = lines[i][leftBound:].find("/")
				version = lines[i][leftBound:leftBound + rightBound]
			if (lines[i].find(".jar") != -1) and (lines[i].find("minecraft_server") != -1) and (lines[i].find("nogui") == -1):
				downloadUrl = lines[i][lines[i].find("https://") : lines[i].find(".jar") + 4]
		return version, downloadUrl

	'''
	downloads a file from the internet via its URL
	'''
	def download(self, url):
		packetSize = 1024
		downloaded = 0
		
		dl_fileName = url.split('/')[-1]
		webFile = urllib.urlopen(url)
		localFile = open(self.mainDirectory + os.sep + dl_fileName, "w")
		
		totalSize = int(webFile.info().getheaders("Content-Length")[0])
		
		while downloaded < totalSize:
			percent = int(downloaded/float(totalSize)*100)+1
			localFile.write(webFile.read(packetSize))
			downloaded += packetSize
			sys.stdout.write("\r{0}".format(self.getProgressString(percent)))
			sys.stdout.flush()
		sys.stdout.write("\n")
		
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
	agree EULA
	'''
	def eula(self):
		# read eula file (if it exists) and change the agreement line
		eulaPath = "./eula.txt"
		lines = []
		if os.path.exists(eulaPath):
			eulaFile = open(eulaPath, "r")
			lines = eulaFile.readlines()
			for i in range(len(lines)):
				if lines[i].startswith("eula="):
					if lines[i] == "eula=true":
						# nothing to do
						eulaFile.close()
						return
					lines[i] = "eula=true"
			eulaFile.close()
		else:
			lines.append("eula=true")
		
		# write into file
		eulaFile = open(eulaPath, "w")
		eulaFile.writelines(lines)
		eulaFile.close()
		
	'''
	adapt RAM size for the small ARM processor
	'''
	def checkRaspberryPi(self):
		if os.uname()[1] != "raspberrypi":
			self.ramString = " -Xmx1024M -Xms1024M"
			
	

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
		self.eula()
		self.checkRaspberryPi()
		command = "java" + self.ramString + " -jar " + self.executablePath + " nogui"
		os.system(command)

	'''
	entry point
	'''
	def main(self):
		# checks if directory "MinecraftServer" exists in your home directory
		if not os.path.exists(self.mainDirectory):
			print "create server directory: " + self.mainDirectory
			os.mkdir(self.mainDirectory)
		
		# lists the content of your server directory
		dirContent = os.listdir(self.mainDirectory)
		serverFileExists = False
		
		# sorts entrys of your server directory by type
		serverVersions = []
		for entry in dirContent:
			if not entry.startswith(".") and not entry.endswith(".jar") \
											and not entry.endswith(".py"):
				self.servers.append(entry)
			if entry.endswith(".jar"):
				if entry.startswith("minecraft_server"):
					localVersion = str(entry)[str(entry).find(".") + 1 : str(entry).find("jar") - 1]
					serverVersions.append(localVersion)
		
		for entry in serverVersions:
			if entry == self.currentServerVersion:
				serverFileExists = True
				self.executablePath = self.mainDirectory + os.sep + "minecraft_server." + entry + ".jar"
				break
				
		if not serverFileExists:
			print "seems you haven't installed the latest server version, let me do that for you..."
			self.download(self.serverURL)
			self.executablePath = self.mainDirectory + os.sep + self.serverURL.split("/")[-1]
		
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
