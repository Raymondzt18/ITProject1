#Raymond Tan (rt503) Feiying Zheng (fz95)

#To run: python3 ./RS.py $TSCOMHOSTNAME $TSEDUHOSTNAME  PROJ2-DNSRS.txt

import numpy as mypy
import threading
import time
import random
import pprint
import sys

import socket as mysoc

RS_DNS_table={}
COMhostname=""
EDUhostname=""
RS_input=""

def RS_server():
	global COMhostname
	global EDUhostname
	global RS_input
	
	if len(sys.argv)<4:
		print("Not enough arguments")
		exit()
	else:
		COMhostname=sys.argv[1]
		EDUhostname=sys.argv[2]
		RS_input=sys.argv[3]
	
	#When server first runs, populate the DNS
	populate_RS_DNS()
	pprint.pprint(RS_DNS_table)
	
	try:
		ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("[S]: RS Server socket created")
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
	
	#waits for IP request messages from client
	while True:
		data_from_client=csockid.recv(200).decode('utf-8')
		
		#client has disconnected from the server
		if not data_from_client:
			print("Client disconnected")
			print("Waiting for another")
			csockid, addr = ss.accept()
			print("[S]: Got a connection request from client at ",addr)
			continue
		
		print("Looking for ",data_from_client)
		recordString=find_Record(data_from_client)
	
		#if cannot find the given hostname, check to see if the hostname ends with .com or .edu and send hostname to the appropriate TS server
		if recordString=='':
			#split the hostname to find top level server
			if data_from_client.endswith('.com'):
				print('Connecting to TSCOM server')
				recordString=findRecordIn_TS(data_from_client, COMhostname,60002)
			elif data_from_client.endswith('.edu'):
				print('Connecting to TSEDU server')
				recordString=findRecordIn_TS(data_from_client, EDUhostname,60001)
			else:
				recordString="Hostname - Error:HOST NOT FOUND"
		
		print("Record Sent back:", recordString)
		csockid.sendall(recordString.encode('utf-8'))
		
	print("[S]: Server Closed")
	
#Populates the RS DNS
def populate_RS_DNS():
	RS_file=open(RS_input, 'r')
	#Read line by line from file and split the different parts
	#Each line contains [Hostname IPaddress A/NS]
	for line in RS_file.readlines():
		line=line.split()
		if line:
			#populate the DNS
			RS_DNS_table[line[0]]=(line[1], line[2])
	
#Given hostname, returns the string record of that hostname [Hostname IPaddress A]
#Returns empty string if not found
def find_Record(hostname):
	record=''
	if hostname in RS_DNS_table:
		recordPair=RS_DNS_table.get(hostname)
		record=hostname+' '+recordPair[0]+' '+recordPair[1]
		
	return record

#Creates socket that will communicate with one of the TS servers
#Returns the record of the given hostname at the TS DNS, or HOST NOT FOUND
def findRecordIn_TS(hostname, TShostname, port):
	
	try:
		cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print("\t[C]: RS socket created to connect to a TS Server")
	except mysoc.error as err:
		print('{} \n'.format("socket open error ",err))

	#Define the IP to connect to the TS server
	TSserverIP=mysoc.gethostbyname(TShostname)
	
	# connect to the TS server
	server_binding=(TSserverIP,port)
	cs.connect(server_binding)
	cs.sendall(hostname.encode('utf-8'))
	data_from_server=cs.recv(200).decode('utf-8')

	#receive data from the server
	print("\tData received from server:",data_from_server)
	
	return data_from_server
	
RS_server()
