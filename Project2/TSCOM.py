#Raymond Tan (rt503) Feiying Zheng (fz95)

#To run: python3 ./TSCOM.py PROJ2-DNSCOM.txt 

import numpy as mypy
import threading
import time
import random
import sys
import pprint
import socket as mysoc

def server():

    name_of_file = ""
    if len(sys.argv)<2:
        print("Not enough arguments")
        exit()
    else:
        name_of_file=sys.argv[1]

    f = open(name_of_file, 'r')
	
    DNS_table = {}
    
	#populates DNS table
    for line in f:
    
        triplet = line.split() #Name ip, IP, IPType

        if triplet: 
            DNS_table[triplet[0]]=((triplet[1], triplet[2]))

    pprint.pprint(DNS_table)
    
    try:
        socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[Server]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))


    server_binding = ('', 60002)
    socket.bind(server_binding)
    socket.listen(1) #parameter  is the maximum number of queued connections aka backlog
    host = mysoc.gethostname()
    print("[Server]: Server host name is: ",host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[Server]: Server IP address is ",localhost_ip)

    conn_id, addr = socket.accept()
    print("[Server]: Got a connection request from client at ",addr)
    
    while True:
        msg = conn_id.recv(100)
        msg = msg.decode('utf-8')
        if not msg:
            print("Client disconnected")
            print("Waiting for another ")
            conn_id, addr = socket.accept()
            print("[Server]: Got a connection request from client at ",addr)
            continue
        
        #Do DNS table lookup
        split_msg = msg.split()

        record = DNS_table.get(split_msg[0])
        return_msg = ''

        if record:
            return_msg = split_msg[0] + ' ' + record[0] + ' ' + record[1]
            return_msg = return_msg.encode('utf-8')
        else:
            return_msg = "Hostname - Error:HOST NOT FOUND".encode('utf-8')

        print("Message sent: "+return_msg.decode('utf-8'))
        conn_id.send(return_msg)

    socket.close()
    exit()
    
server()
