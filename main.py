import random
import socket

import pygame
import argparse

from Config import *
from Network import Network
from Player import Player
from Utils import *
from client import *

# ESCANEO DE SERVIDORES
myip = socket.gethostbyname(socket.gethostname())

with open("hosts.txt") as avaiables:
    hosts = avaiables.readlines()
    for i in range(len(hosts)):
        hosts[i] = hosts[i].replace("\n","")

    print(hosts)

print("FINDING IN SERVERS WITH IP:")
for ip in hosts: print(ip)

allowed_ports = [3000,4000,5555]

print("SCANNING IN ALLOWED PORTS:")
print(allowed_ports)

servers = []

# ESCANEO DE PUERTOS EN LOS HOSTS
for host in hosts:
    for port in allowed_ports:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = sock.connect_ex((host,port))
        
        if result == 0:
            print(f"Found server in {host};{port}")
            servers.append([host,port])

        sock.close()

# CONECTANDOSE A UN SERVIDOR ALEATORIO
args = cli()
elejido = random.sample(servers,1)[0]

cliente = Client(args.username,elejido[0],int(elejido[1]))
cliente.main()