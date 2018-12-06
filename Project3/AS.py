#Raymond Tan (rt503) Feiying Zheng (fz95)
#Client and AS server runs on same machine

import numpy as mypy
import threading
import time
import random
import sys
import hmac

import socket as mysoc



def AS_server():
	TS1="cpp.cs.rutgers.edu"
	TS2="java.cs.rutgers.edu"
	
	try:
		ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[S]: AS Server socket created")
	except mysoc.error as err:
		print('{} \n'.format("socket open error", err))
	
	#specifies that this socket is reachable by any address this machine happens to have
	server_binding=('', 56789)
	ss.bind(server_binding)
	ss.listen(1)
	host=mysoc.gethostname()
	
	print("[S]: Server host name is: ",host)
	localhost_ip=(mysoc.gethostbyname(host))
	print("[S]: Server IP address is  ",localhost_ip)
	
	csockid,addr=ss.accept()
	print ("[S]: Got a connection request from a client at", addr)
	
	#waits for request messages from client
	while True:
		data_from_client=csockid.recv(200).decode('utf-8')
		
		#client has disconnected from the server
		if not data_from_client:
			print("Client disconnected")
			print("Waiting for another")
			csockid, addr = ss.accept()
			print("[S]: Got a connection request from client at ",addr)
			continue
		
		print("[S]: Data received : ",data_from_client)
		dataArray=data_from_client.split()
		challenge=dataArray[0]
		digest=dataArray[1]
		
		#Get digests from the TS servers
		digestTS1=getTSDigest(challenge, TS1,60001)
		
		digestTS2=getTSDigest(challenge, TS2,60002)
		
		#Send back the TS Server name where the digests match
		if digestTS1==digest:
			print("[S]: Sending: " + TS1 + " to client")
			csockid.sendall(TS1.encode('utf-8'))
		elif digestTS2==digest:
			print("[S]: Sending: " + TS2 + " to client")
			csockid.sendall(TS2.encode('utf-8'))

	print("[S]: Server Closed")
	

#Contact the given TS server with a challenge to get its digest
def getTSDigest(challenge,TShostname, TSport):
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[S]: Client socket created to connect to TS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))

	#Define the port and IP to connect to the TS server
	port=TSport
	TSserverIP=mysoc.gethostbyname(TShostname)
	
	# connect to the TS server
	server_binding=(TSserverIP,port)
	cs.connect(server_binding)

	# "AS challenge" is sent to TS to identify Auth server message
	message="AS "+challenge

	cs.sendall(message.encode('utf-8'))
	digest=cs.recv(200).decode('utf-8')
	
	#receive data from the server
	print("Digest received from TS server:",digest)
	
	return digest		
	
AS_server()
