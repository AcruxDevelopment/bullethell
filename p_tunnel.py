import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random
import math

class PatternTunnel(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 5):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/ultraswing.wav")
        self.snd_spawn.set_volume(0.5)

    def start(self):
        super().start()

    def update(self):
        super().update()
        self.frame += 1
        if self.frame % self.interval == 0:
            soul = self.soul

            yoff = math.sin(self.frame * 0.05) * 70
            yc = yoff + 150
            for i in range(6):
                yc -= 60
                if i == 2 or i == 3:
                    continue
                bullet = BulletRain(self.board.x - self.board.size, self.board.y + yc, 0, 0.1)
                self.bullets.append(bullet)

        if self.frame % 35 == 0 and not self.frame % (35*2) == 0:
                self.snd_spawn.play()
                board = self.board
                xc = board.x - board.size/2
                while(xc < board.x):
                    bullet = BulletRain(xc, board.y + board.size + 100, -90, 0.1)
                    self.bullets.append(bullet)
                    xc += 40

        if self.frame % (35*2) == 0:
                self.snd_spawn.play()
                board = self.board
                xc = board.x
                while(xc < board.x + board.size/2):
                    bullet = BulletRain(xc, board.y + board.size + 100, -90, 0.1)
                    self.bullets.append(bullet)
                    xc += 40
