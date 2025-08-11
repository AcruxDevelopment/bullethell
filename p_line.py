import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random
import math

class PatternLine(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 5):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/hypnosis.wav")

    def start(self):
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame == 1:
            self.snd_spawn.play()
        self.degree += 1
        if self.frame % self.interval == 0:
            soul = self.soul
            board = self.board

            bullet = BulletRain(board.x - board.size - 20, self.board.y, 0)
            self.bullets.append(bullet)
            bullet.rotate_around((self.x, self.y), self.degree)

            bullet = BulletRain(self.board.x, board.y + board.size + 20, -90)
            self.bullets.append(bullet)
            bullet.rotate_around((self.x, self.y), self.degree)


            bullet = BulletRain(board.x - board.size - 20, board.y + board.size + 20, -45)
            self.bullets.append(bullet)
            bullet.rotate_around((self.x, self.y), self.degree)


            bullet = BulletRain(board.x + board.size + 20, board.y + board.size + 20, 45*5)
            self.bullets.append(bullet)
            bullet.rotate_around((self.x, self.y), self.degree)

