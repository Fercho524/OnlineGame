import pygame
import random

import numpy as np

from Config import *
from Utils import *


class Player:
    def __init__(self, x, y, width, height, color, username):
        # Identification
        self.color = color
        self.username = username

        # Position
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Live
        self.state = "live"
        self.hp = DEFAULT_HP

        # Balls
        self.balls = []

        self.excluded = []

        # Damage Animation
        self.step_animation = 0

    def add_ball(self, target_x, target_y):
        direction = np.array([target_x - self.x, target_y - self.y])
        direction = BALL_SPEED * (direction / np.linalg.norm(direction))
        self.balls.append([self.x + 1, self.y + 1, BALL_WIDTH, BALL_WIDTH, direction[0], direction[1]])

    def pickballs(self,balls):

        for i,ball in enumerate(balls):
            if check_colisions(ball[0],ball[1],20,20,self.x,self.y,self.width,self.height) and not (ball in self.excluded):
                self.width += 2
                self.height += 2
                self.hp += 10

                self.excluded.append(ball)


    def update(self):
        # Si choca rebota y se daña
        if self.x <= 0:
            self.x += self.width
            self.damage(reason="wal")
        elif self.x >= WIDTH:
            self.x -= self.width
            self.damage(reason="wal")
        elif self.y <= 0:
            self.y += self.height
            self.damage(reason="wal")
        elif self.y >= HEIGHT:
            self.y -= self.height
            self.damage(reason="wal")
        else:
            self.state = "live"

        # Dibuja las balas y elimina las que ya no están en el escenario
        for ballBounds in self.balls:
            if not is_out(ballBounds[0], ballBounds[1]):
                self.balls.remove(ballBounds)
            else:
                ballBounds[0] += ballBounds[4]
                ballBounds[1] += ballBounds[5]

        # Si muere
        if self.hp <= 0:
            self.hp = 0
            self.state = "dead"

    def move(self, keys):
        # Control
        if not self.state == "dead":
            self.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
            self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * PLAYER_SPEED

    def damage(self,reason="player"):
        
        if self.hp >= 0:
            if reason=="wal":
                self.state = "damage"
                self.hp -= 10
            
            if reason=="player":
                self.state = "damage"
                self.hp -= 2

                if (self.width >= 50 and self.height>= 50):
                    self.width -= 1
                    self.height -= 1

    def draw_hp(self,font,SCREEN):        
        text_img = font.render(f"Live : {self.hp}", True, self.color)
        text_img.get_rect()
        xt0 = text_img.get_rect().x
        wt0 = text_img.get_rect().w
        
        SCREEN.blit(text_img, (WIDTH/2 - wt0/2,20))

    def draw(self, screen):
        # Balls
        for ballBounds in self.balls:
            pygame.draw.rect(
                screen,
                self.color,
                [ballBounds[0], ballBounds[1], ballBounds[2], ballBounds[3]],
            )

        # Player
        if self.state == "live":
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        elif self.state == "damage":
            if self.step_animation <= DAMAGE_ANIMATION_DURATION:
                pygame.draw.rect(screen, DAMAGE_COLOR, [self.x, self.y, self.width, self.height])
                self.step_animation += 1
            else:
                self.step_animation = 0
        elif self.state == "dead":
            pygame.draw.rect(screen, DEATH_COLOR, [self.x, self.y, self.width, self.height])



def init_player(id,black=False):
    color = (0,0,0) if black else (random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))

    return Player(
        x=random.randint(0,100),
        y=random.randint(0,100),
        width=50,
        height=50,
        color=color,
        username=str(id)
    )