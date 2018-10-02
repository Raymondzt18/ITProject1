import numpy as mypy
import threading
import time
import random
import pprint

import socket as mysoc

RS_DNS_table={}
TShostname=populate_RS_DNS()
def RS_server():

	
	recordString=find_Record('www.gosogle.com')

	print("TS Hostname is", TShostname)
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
		data_from_client=csockid.recv(100).decode('utf-8')
		#client has disconnected from the server
		if not data_from_client:
			print("[S]: Client disconnected", addr)
			break

#Populates the RS DNS and returns the TS hostname
def populate_RS_DNS():

	RS_file=open('PROJ1-DNSRS.txt', 'r')
	TShostname=''
	#Read line by line from file and split the different parts
	#Each line contains [Hostname IPaddress A/NS]
	for line in RS_file.readlines():
		line=line.split()
		
		#store the hostname that is running the TS server
		if line[2]=='NS':
			TShostname=line[0]
		#populate the DNS
		else:
			RS_DNS_table[line[0]]=(line[1], line[2])
		#print(line)
		
		
	print("Printing RS DNS")
	pprint.pprint(RS_DNS_table)
	
	return TShostname

#Given hostname, returns the string record of that hostname [Hostname IPaddress A]
#Returns empty string if not found
def find_Record(hostname):
	record=''
	if hostname in RS_DNS_table:
		recordPair=RS_DNS_table.get(hostname)
		record=hostname+' '+recordPair[0]+' '+recordPair[1]
		print("record is",record)
		
	return record
	
RS_server()
