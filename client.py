import socket
import random
import pygame
import argparse

from sys import argv

from Config import *
from Network import Network
from Player import Player
from Utils import *

pygame.init()

def draw_background(screen):
    # FONDO
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))


def handle_events(player):
    # DISPARA PROYECTIL
    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Shot
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.add_ball(event.pos[0], event.pos[1])


def draw_players(PLAYERS,SCREEN,user):
    users = []

    for player in PLAYERS:
        color = player.color if not player.state == "dead" else (255,255,255)
        pygame.draw.rect(SCREEN, color, [player.x, player.y, player.width, player.height])

        if check_colisions(user.x,user.y,user.width, user.height, player.x, player.y, player.width, player.height):
            if not player.state=="dead":
                user.damage(reason="player")

        users.append(player.username)

    print(f"[SHARING WITH]: {users}")


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


def main():
    # PYGAGME INITIALIZATION
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode(SIZE)
    # Cada jugador tiene 20 puntos, el jugador se los puede comer y gana salud, debe comérselos antes de que el otro jugador lo haga y luego debe perseguirlo
    BALLS = [ [random.randint(0,WIDTH-20),random.randint(60,HEIGHT-20)] for i in range(0,20) ]
    font = pygame.font.SysFont("Press_Start_2P", 20)


    # READING ARGUMENTS
    args = cli()

    # FETCHING INFO FROM SERVER
    game_server = Network(args.host,args.port)
    PLAYERS = game_server.get_players()

    # CREATING A PLAYER FOR THE USER
    player = Player(WIDTH/2, HEIGHT/2, 50, 50, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), args.username)

    while True:
        # BACKGROUND
        draw_background(SCREEN)
        
        # CLOSE EVENTS
        handle_events(player)

        # BALLS DRAWING
        for ball in BALLS:
            if not (ball in player.excluded):
                pygame.draw.rect(SCREEN,player.color,[ball[0],ball[1],20,20])
        
        # DRAW PLAYER
        player.draw(SCREEN)
        player.draw_hp(font,SCREEN)
        player.update()
        
        # PLAYER MOVING
        keys = pygame.key.get_pressed()
        player.move(keys)

        player.pickballs(BALLS)

        # GET OTHER PLAYERS AND SEND INFO
        PLAYERS = game_server.send(player)
        draw_players(PLAYERS,SCREEN,player)

        # DISPLAY UPDATE
        pygame.display.update()
        pygame.display.flip()

        CLOCK.tick(60)


if __name__ == "__main__":
    main()