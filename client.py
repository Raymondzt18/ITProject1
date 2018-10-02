import numpy as mypy
import threading
import time
import random

import socket as mysoc

def client():
	outputFile=open('RESOLVED.txt', 'w+')
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[C]: Client socket created to connect to RS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))
	
	#Define the port on which you want to connect to the server
	port=56789
	sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())

	# connect to the RS server on local machine
	server_binding=(sa_sameas_myaddr,port)
	cs.connect(server_binding)

	#Read the file with all the hostnames. We want to get their IP addresses

	hostNameFile=open('PROJ1-HNS.txt', 'r')
	for line in hostNameFile.readlines():
		line=line.rstrip()
		print("sending", line.encode('utf-8'))
		cs.sendall(line.encode('utf-8'))
		data_from_server=cs.recv(200).decode('utf-8')
	
		#receive data from the server
		print("[C]: Data received from server:  ",data_from_server)
		
		dataArray=data_from_server.split()
		if dataArray[2]=='NS':
			print(line, "is not in RS Server. Check TS Server")
			data_from_server=findRecordIn_TS(line, dataArray[0])

		outputFile.write(data_from_server+'\n')
		
#Returns the record of the given hostname at the TS DNS
#Returns HOST NOT FOUND if is not in TS DNS
def findRecordIn_TS(hostname, TSserverIP):
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[C]: Client socket created to connect to TS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))

	#Define the port on which you want to connect to the server
	port=60001

	# connect to the TS server
	server_binding=(TSserverIP,port)
	cs.connect(server_binding)
	cs.sendall(hostname.encode('utf-8'))
	data_from_server=cs.recv(200).decode('utf-8')

	#receive data from the server
	print("[C]: Data received from server:  ",data_from_server)
	
	return data_from_server
	
		
	
client()
		
        
        
        
        
        
