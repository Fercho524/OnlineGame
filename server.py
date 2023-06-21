import time
import socket
import pickle
import termcolor

from _thread import *
from sys import argv

from Player import *

class Server:
    def __init__(self,host,port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.bind((host, port))
            self.server_socket.listen()
            print(f"Waiting for a connection, Server Started at {host}:{port}")
        except socket.error as e:
            str(e)

    # CREATING PLAYER 0
        self.players = [init_player(0,black=True)]
        self.currentPlayer = 0


    def threaded_client(self,conn:socket.socket, player_id):
        global start

        # SEND THE PLAYER TO THE CORRESPONDING CLIENT
        conn.send(pickle.dumps(self.players[player_id]))
        addr = list(conn.getpeername())
        start = time.time()
        
        reply = ""

        while True:
            try:
                # GET THE SENT PLAYER FROM THE CLIENT
                recived_player = pickle.loads(conn.recv(2048))
                
                if not recived_player:
                    print("Disconnected")
                    print(self.currentPlayer)
                    break
                else:
                    reply = []

                    # SEND ALL PLAYERS EXEPT THE PLAYER_ID
                    for i in range(len(self.players)):
                        if i!=player_id:
                            reply.append(self.players[i])
                        else:
                            self.players[i] = recived_player
                    
                    #PRINT EACH 3 SECONDS
                    dif = time.time() - start
                    if dif >3:
                        start = time.time()

                        termcolor.cprint("RECIVING FROM]","green",end="")
                        print(f" {addr[0]}:{addr[1]} => {recived_player.username}")
                        termcolor.cprint("[SENDING TO]","yellow",end="")
                        print(f" {addr[0]}:{addr[1]}")

                conn.sendall(pickle.dumps(reply))
            except:
                break

        termcolor.cprint("[LOST CONNECTION]","red",end="")
        print(f" {addr[0]}:{addr[1]} Say Goodbye")

        conn.close()
        self.currentPlayer-=1
        
        if len(self.players)>0:
            self.players.pop()
            
        if len(self.players)==0:
            print("WAITING FOR PLAYERS")

    def run(self):
        while True:
            # ACCEPT NEW CONNECTIONS
            conn, addr = self.server_socket.accept()
            addr = list(addr)
            termcolor.cprint("CONNECTION FROM]","blue",end="")
            print(f" {addr[0]}:{addr[1]}")

            # MAKE A THREAD WITH THE CONNECTION
            start_new_thread(self.threaded_client, (conn, self.currentPlayer))
            
            # REMOVE THE PLAYER 0
            if self.currentPlayer == 0 and len(self.players)>0:
                self.players.remove(self.players[0])

            # ADD A NEW PLAYER
            self.currentPlayer += 1
            self.players.append(init_player(self.currentPlayer))



if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = int(argv[1])
    
    serv = Server(host,port)
    serv.run()