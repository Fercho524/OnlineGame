import socket
import pickle

from sys import argv


class Network:
    def __init__(self,server,port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.players = self.connect()

        print(f"[CONNECTED TO] : {self.addr[0]}:{self.addr[1]}")

    def get_players(self):
        print(f"[GETTING PLAYERS FROM] {self.addr[0]}:{self.addr[1]}")
        
        return self.players

    def connect(self):
        # Return players
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
