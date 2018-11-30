#Raymond Tan (rt503) Feiying Zheng (fz95)

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc
import hmac

#creates socket that will communicate with Auth server
#Hostname for Auth server should be given in command
def client():

	AShostname=''
	#Should have 1 argument (hostname running Auth Server)
	if len(sys.argv)<2:
		print("Please enter host name of Auth Server")
		exit()
	else:
		AShostname=sys.argv[1]
	
	outputFile=open('RESOLVED.txt', 'w+')
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[C]: Client socket created to connect to Auth Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))
	
	#Define the port and IP address to connect to the RS server
	port=56789
	sa_sameas_myaddr =mysoc.gethostbyname(AShostname)

	# connect to the Auth server
	server_binding=(sa_sameas_myaddr,port)
	cs.connect(server_binding)

	#Read the file with all the hostnames. We want to get their IP addresses
	
	hostNameFile=open('PROJ3-HNS.txt', 'r')
	
	#Line is [key, challenge, ip]
	for line in hostNameFile.readlines():
		line=line.split()
		key = line[0].rstrip()
		challenge = line[1].rstrip()
		hostname = line[2].rstrip()
		digest = hmac.new(key.encode(), challenge.encode("utf-8"))

		print("[C]: Sending challenge " + challenge + " and digest "+digest.hexdigest())
		
		msg = challenge + " " + digest.hexdigest()
		cs.sendall(msg.encode('utf-8'))

		#Response from Auth server with TS hostname
		TShostname = cs.recv(200).decode('utf-8')
		
		print("[C]: TSHostName Received "+ TShostname)

		TSport
		if TShostname == "null.cs.rutgers.edu":
			TSport = 60001
		elif TShostname == "pascal.cs.rutgers.edu":
			TSport = 60002

		data_from_server = findRecordInTS(hostname, TSHostname, TSport)

		dataArray=data_from_server.split()
		
		if dataArray[2]=='NS':
			print(hostname + " is not found")
			outputFile.write("Error: HOST NOT FOUND")
			continue
		else:
			outputMsg = TShostname + " " data_from_server
			outputFile.write(outputMsg)
		
#Given a hostName that we want the IP of and the hostname of the TS Server, find the IP
def findRecordInTS(hostname, TShostname, TSport):
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("\t[C]: Client socket created to connect to TS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))

	#Define the port and IP to connect to the TS server
	port=TSport
	TSserverIP=mysoc.gethostbyname(TShostname)
	
	# connect to the TS server
	server_binding=(TSserverIP,port)
	cs.connect(server_binding)
	cs.sendall(hostname.encode('utf-8'))
	data_from_server=cs.recv(200).decode('utf-8')

	#receive data from the server
	print("\tData received from server:",data_from_server)
	
	return data_from_server		
	
client()
		
        
        
        
        
        
