import socket
import random
import pygame
import argparse

from Config import *
from Network import Network
from Player import Player
from Utils import *

pygame.init()

class Client:
    def __init__(self,username,host,port):
        self.width = 500
        self.height = 500

        self.player = Player(
            x=self.width/2, 
            y=self.height/2, 
            width=50, 
            height=50, 
            color =(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
            username = username
        )

        # PYGAGME INITIALIZATION
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SIZE)
        # Cada jugador tiene 20 puntos, el jugador se los puede comer y gana salud, debe comérselos antes de que el otro jugador lo haga y luego debe perseguirlo
        self.balls = [ [random.randint(0,WIDTH-20),random.randint(60,HEIGHT-20)] for i in range(0,20) ]


        self.font = pygame.font.SysFont("Press_Start_2P", 20)

        # FETCHING INFO FROM SERVER
        self.game_server = Network(host,port)
        self.players = self.game_server.get_players()


    def draw_background(self,screen):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.width, self.height))


    def handle_events(self):
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


    def draw_players(self):
        users = []

        for player in self.players:
            color = player.color if not player.state == "dead" else (255,255,255)
            pygame.draw.rect(self.screen, color, [player.x, player.y, player.width, player.height])

            if check_colisions(self.player.x,self.player.y,self.player.width, self.player.height, player.x, player.y, player.width, player.height):
                if not player.state=="dead":
                    self.player.damage(reason="player")

            users.append(player.username)


    def main(self):
        while True:
            # BACKGROUND
            self.draw_background(self.screen)
            self.handle_events()

            # BALLS DRAWING
            for ball in self.balls:
                if not (ball in self.player.excluded):
                    pygame.draw.rect(self.screen,self.player.color,[ball[0],ball[1],20,20])
            
            # DRAW PLAYER
            self.player.draw(self.screen)
            self.player.draw_hp(self.font,self.screen)
            self.player.update()
            
            # PLAYER MOVING
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.pickballs(self.balls)

            # GET OTHER PLAYERS AND SEND INFO
            self.players = self.game_server.send(self.player)
            self.draw_players()

            # DISPLAY UPDATE
            pygame.display.update()
            pygame.display.flip()

            self.clock.tick(60)

def cli():
    parser = argparse.ArgumentParser(
        prog="Simple Network Position on Board",
        description="A simple program that only log visualy the users position on an 'online game'"
    )
    
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        action="store",
        default=socket.gethostbyname(socket.gethostname()),
        help="Use the server host to connect"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        action="store",
        default=5555,
        help="Use the server port to connect"
    )

    parser.add_argument(
        "-u",
        "--username",
        type=str,
        action="store",
        default=socket.gethostbyname(socket.gethostname()),
        help="Use the server host to connect"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = cli()
    client = Client(args.username,args.host,args.port)
