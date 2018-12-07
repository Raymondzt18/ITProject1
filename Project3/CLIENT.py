#Raymond Tan (rt503) Feiying Zheng (fz95)
#Client and AS server runs on same machine

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc
import hmac

#creates socket that will communicate with Auth server
def client():
	
	outputFile=open('RESOLVED.txt', 'w+')
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[C]: Client socket created to connect to Auth Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))
	
	#Define the port and IP address to connect to the RS server
	port=56789
	sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())

	# connect to the Auth server
	server_binding=(sa_sameas_myaddr,port)
	cs.connect(server_binding)

	#Read the file with all the hostnames. We want to get their IP addresses
	
	hostNameFile=open('PROJ3-HNS.txt', 'r')
	
	#Line is [key, challenge, ip]
	for line in hostNameFile.readlines():
		line=line.split()
		if len(line)<3:
			continue
		key = line[0].rstrip()
		challenge = line[1].rstrip()
		hostname = line[2].rstrip()
		digest = hmac.new(key.encode(), challenge.encode("utf-8"))

		print("[C]: Sending Challenge: " + challenge + " Digest: "+digest.hexdigest())
		
		msg = challenge + " " + digest.hexdigest()
		cs.sendall(msg.encode('utf-8'))

		#Response from Auth server with TS hostname
		TShostname = cs.recv(200).decode('utf-8')
		
		print("[C]: TSHostName Received: "+ TShostname)

		TSport=60011
		if TShostname == "cpp.cs.rutgers.edu":
			TSport = 60011
		elif TShostname == "java.cs.rutgers.edu":
			TSport = 60022

		data_from_server = findRecordInTS(hostname, TShostname, TSport)

		if data_from_server=='Error: HOST NOT FOUND':
			outputFile.write("Error: HOST NOT FOUND")
			continue 
		
		dataArray=data_from_server.split()
		
		if dataArray[2]=='NS':
			print(hostname + " is not found")
			outputFile.write("Error: HOST NOT FOUND")
			continue

		else:
			#Outputs response from TLDS server (even if is not found)
			outputMsg = TShostname + " " +data_from_server+"\n"
			outputFile.write(outputMsg)
		
#Given a hostName that we want the IP of and the hostname of the TS Server, find the IP
def findRecordInTS(hostname, TShostname, TSport):
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[C]: Client socket created to connect to TS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))
		
	print("[C]: Requesting IP for: ", hostname)
	#Define the port and IP to connect to the TS server
	port=TSport
	TSserverIP=mysoc.gethostbyname(TShostname)
	
	# connect to the TS server
	server_binding=(TSserverIP,port)
	cs.connect(server_binding)

	# "CLIENT hostname" is sent to TS to identify client message
	message="CLIENT "+hostname
	cs.sendall(message.encode('utf-8'))
	data_from_server=cs.recv(200).decode('utf-8')

	#receive data from the server
	print("Data received from server:",data_from_server)
	
	return data_from_server		
	
client()
		
        
        
        
        
        
