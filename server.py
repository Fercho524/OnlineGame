import time
import socket
import pickle
import termcolor

from _thread import *
from sys import argv

from Player import *

# CREATING THE SERVER
host = socket.gethostbyname(socket.gethostname())
port = int(argv[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# STARTING THE SERVER
try:
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Waiting for a connection, Server Started at {host}:{port}")
except socket.error as e:
    str(e)

# CREATING PLAYER 0
players = [init_player(0,black=True)]
currentPlayer = 0


def threaded_client(conn:socket.socket, player_id):
    global currentPlayer
    global start

    # SEND THE PLAYER TO THE CORRESPONDING CLIENT
    conn.send(pickle.dumps(players[player_id]))
    addr = list(conn.getpeername())
    start = time.time()
    
    reply = ""

    while True:
        try:
            # GET THE SENT PLAYER FROM THE CLIENT
            recived_player = pickle.loads(conn.recv(2048))
            
            
            if not recived_player:
                print("Disconnected")
                print(currentPlayer)
                break
            else:
                reply = []

                # SEND ALL PLAYERS EXEPT THE PLAYER_ID
                for i in range(len(players)):
                    if i!=player_id:
                        reply.append(players[i])
                    else:
                        players[i] = recived_player
                    
                
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
    currentPlayer-=1
    
    if len(players)>0:
        players.pop()
        
    if len(players)==0:
        print("WAITING FOR PLAYERS")

while True:
    # ACCEPT NEW CONNECTIONS
    conn, addr = server_socket.accept()
    addr = list(addr)
    termcolor.cprint("CONNECTION FROM]","blue",end="")
    print(f" {addr[0]}:{addr[1]}")

    # MAKE A THREAD WITH THE CONNECTION
    start_new_thread(threaded_client, (conn, currentPlayer))
    
    # REMOVE THE PLAYER 0
    if currentPlayer == 0 and len(players)>0:
        players.remove(players[0])

    # ADD A NEW PLAYER
    currentPlayer += 1
    players.append(init_player(currentPlayer))