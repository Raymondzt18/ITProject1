#Raymond Tan (rt503) Feiying Zheng (fz95)

#To run:python3 ./CLIENT.py $RSHOSNAME PROJ2-HNS.txt

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc

#creates socket that will communicate with RS server
#Hostname for RS server should be given in command
def client():
	inputFile=''
	RShostname=''
	
	if len(sys.argv)<3:
		print("Not enough arguments")
		exit()
	else:
		RShostname=sys.argv[1]
		inputFile=sys.argv[2]
	
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
	hostNameFile=open(inputFile, 'r')
	outputFile=open('RESOLVED.txt', 'w+')
	
	for line in hostNameFile.readlines():
		line=line.rstrip()
		print("[C]: Requesting IP for hostname:", line)
		cs.sendall(line.encode('utf-8'))
		data_from_server=cs.recv(200).decode('utf-8')
	
		#receive data from the server is in the form [Hostname IPaddress A/NS]
		
		print("\tData received from server:  ",data_from_server)
		
		outputFile.write(data_from_server+'\n')

	
client()
		
        
        
        
        
        
