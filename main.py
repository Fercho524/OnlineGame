import socket
import multiprocessing

from _thread import *
from sys import argv

from Player import *
from server import Server

hosts = []

with open("avaiables.txt") as addresses:
    hosts = addresses.readlines()

    for i,host in enumerate(hosts):
        ip,port = host.split(":")
        hosts[i] = [ip,int(port)]

print(hosts)

server = random.sample(hosts,1)[0]

print(server)

host = server[0]
port = server[1]


serv = Server(port,host)

serv.run()