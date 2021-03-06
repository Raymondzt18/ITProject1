#Raymond Tan (rt503) Feiying Zheng (fz95)

import numpy as mypy
import threading
import time
import random

import socket as mysoc

RS_DNS_table={}

def RS_server():
	
	#When server first runs, populate the DNS and get the TS hostname
	TShostname=populate_RS_DNS()

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
			
		recordString=find_Record(data_from_client)
	
		#if cannot find the given hostname, send the TS host record back to client
		if recordString=='':
			recordString=find_Record(TShostname)
		
		print("Record Sent back:", recordString)
		csockid.sendall(recordString.encode('utf-8'))
		
	print("[S]: Server Closed")
	
#Populates the RS DNS and returns the TS hostname
def populate_RS_DNS():

	RS_file=open('PROJ1-DNSRS.txt', 'r')
	TShostname=''
	
	#Read line by line from file and split the different parts
	#Each line contains [Hostname IPaddress A/NS]
	for line in RS_file.readlines():
		line=line.split()
		
		#populate the DNS
		RS_DNS_table[line[0]]=(line[1], line[2])
		#store the hostname that is running the TS server
		if line[2]=='NS':
			TShostname=line[0]
	
	return TShostname

#Given hostname, returns the string record of that hostname [Hostname IPaddress A]
#Returns empty string if not found
def find_Record(hostname):
	record=''
	if hostname in RS_DNS_table:
		recordPair=RS_DNS_table.get(hostname)
		record=hostname+' '+recordPair[0]+' '+recordPair[1]
		
	return record
	
	
RS_server()
