Minecraft Server Manager
======================

####'quick and dirty' implementation of an easy to use server manager for Minecraft

Runs on Unix-like platforms, make sure you have Java and Python installed on your system.

####Description

The MinecraftServerManager is an easy to use interactive Python script for automatic management of your Minecraft servers. You won't have to download the minecraft_server.jar file or take care where your server data is saved on your hard disk by yourself. Just start the script like

	python mc_manager.py
	
from a command prompt and the MinecraftServerManager will create a 'MinecraftServer' directory in your home directory in which you can create and start your servers in an interactive way. After starting a server you can use it as you are used to.

####Todo
- exception handling
- Windows compatibility
- automatic snapshots to restore the world if necessary
- (done) progress bar while downloading the jar-file from minecraft.net
- (done) check for latest jar-file on server automatically instead of hard coded downloading 1.6.2
