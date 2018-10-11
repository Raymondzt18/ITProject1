#Raymond Tan (rt503) Feiying Zheng (fz95)

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc

#creates socket that will communicate with RS server
#Hostname for RS server should be given in command
def client():

	RShostname=''
	#Should have 1 argument (hostname running RS Server)
	if len(sys.argv)<2:
		print("Please enter host name of RS Server")
		exit()
	else:
		RShostname=sys.argv[1]
	
	outputFile=open('RESOLVED.txt', 'w+')
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[C]: Client socket created to connect to RS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))
	
	#Define the port and IP address to connect to the RS server
	port=56789
	sa_sameas_myaddr =mysoc.gethostbyname(RShostname)

	# connect to the RS server
	server_binding=(sa_sameas_myaddr,port)
	cs.connect(server_binding)

	#Read the file with all the hostnames. We want to get their IP addresses
	
	hostNameFile=open('PROJ1-HNS.txt', 'r')
	
	for line in hostNameFile.readlines():
		line=line.rstrip()
		print("[C]: Requesting IP for hostname:", line)
		cs.sendall(line.encode('utf-8'))
		data_from_server=cs.recv(200).decode('utf-8')
	
		#receive data from the server is in the form [Hostname IPaddress A/NS]
		
		print("\tData received from server:  ",data_from_server)
		
		dataArray=data_from_server.split()
		
		if dataArray[2]=='NS':
			print("\t",line, "is not in RS DNS. Please check TS DNS")
			data_from_server=findRecordIn_TS(line, dataArray[0])
		
		print("\tIP is:  ",data_from_server)
		outputFile.write(data_from_server+'\n')
		
		
#Creates socket that will communicate with TS server
#Returns the record of the given hostname at the TS DNS, or HOST NOT FOUND
def findRecordIn_TS(hostname, TShostname):
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("\t[C]: Client socket created to connect to TS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))

	#Define the port and IP to connect to the TS server
	port=60001
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
		
        
        
        
        
        
