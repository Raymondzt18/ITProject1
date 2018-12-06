#Raymond Tan (rt503) Feiying Zheng (fz95)
#Running on java.cs.rutgers.edu

import numpy as mypy
import threading
import time
import random
import hmac
import pprint
import socket as mysoc

def server():
    name_of_keyFile = "PROJ3-KEY2.txt"
    f = open(name_of_keyFile, 'r')

    key=""
    for line in f:
        key=line.strip()
        break

    name_of_DNSFile="PROJ3-TLDS2.txt"
    f=open(name_of_DNSFile, 'r')

    #[hostname, IP, A/NS]
    DNS_table = {}
    
	#populates DNS table
    for line in f:
    
        triplet = line.split()

        if triplet and triplet[2]!="NS":
            DNS_table[triplet[0]]=((triplet[1], triplet[2]))

    pprint.pprint(DNS_table)
    
    try:
        socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))


    server_binding = ('', 60002)
    socket.bind(server_binding)
    socket.listen(1) #parameter  is the maximum number of queued connections aka backlog
    host = mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is ",localhost_ip)

    conn_id, addr = socket.accept()
    print("[S]: Got a connection request from ",addr)
    
    while True:
        msg = conn_id.recv(100)
        msg = msg.decode('utf-8')
        if not msg:
            print("Client disconnected")
            print("Waiting for another ")
            conn_id, addr = socket.accept()
            print("[Server]: Got a connection request from client at ",addr)
            continue
        
        
        split_msg = msg.split()
        identify=split_msg[0]
        if identify=="CLIENT":

            #Do DNS table lookup
            print("Looking for IP of ", split_msg[1].strip())
            record = DNS_table.get(split_msg[1].strip())
            return_msg = ''

            if record:
                return_msg = split_msg[1] + ' ' + record[0] + ' ' + record[1]
                return_msg = return_msg.encode('utf-8')
            else:
                return_msg = "Error:HOST NOT FOUND".encode('utf-8')

            print("Message sent: "+return_msg.decode('utf-8'))
            conn_id.send(return_msg)
        elif identify=="AS":
            challenge=split_msg[1]
            digest = hmac.new(key.encode(), challenge.encode("utf-8"))
            print("Digest sent: "+digest.hexdigest())

            conn_id.send(digest.hexdigest().encode('utf-8'))


    socket.close()
    exit()
    
server()
