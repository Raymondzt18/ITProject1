#Raymond Tan (rt503) Feiying Zheng (fz95)

import numpy as mypy
import threading
import time
import random
import sys
import hmac

import socket as mysoc

TS1=""
TS2=""

def RS_server():
	global TS1
	global TS2
	
	if len(sys.argv)<3:
		print("Not enough arguments")
		exit()
	else:
		TS1=sys.argv[1]
		TS2=sys.argv[2]
	
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
		
		digestTS1=getTSDigest(challenge, TS1,60001)
		
		digestTS2=getTSDigest(challenge, TS2,60002)
		
		if digestTS1==digest:
			csockid.sendall(TS1.encode('utf-8'))
		elif digestTS2==digest:
			csockid.sendall(TS2.encode('utf-8'))

	print("[S]: Server Closed")
	

#Given a hostName that we want the IP of and the hostname of the TS Server, find the IP
def getTSDigest(challenge,TShostname, TSport):
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("\t[S]: Client socket created to connect to TS Server")
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
	print("\tDigest received from TS server:",digest)
	
	return digest		
	
RS_server()
