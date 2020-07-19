#!/usr/bin/python3
import os
import socket
def listener():
    port = input("Enter a port to start listener : ")
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    print("Your IP Address is : " + ipaddr)
    print("Port " + port)
    cmd = "nc -l "+port
    os.system(cmd)
def connect():
    defaulthost = '127.0.0.1'
    defaultport = 4444
    host = input("Enter your host ip address (default: 127.0.0.1): ")
    port = input("Enter your port (deafult:4444): ")
    if(len(host) == 0):
      host = defaulthost
    if(len(port) == 0):
      port = defaultport
    cmd = "nc " + host + " " + str(port)
    os.system(cmd)
