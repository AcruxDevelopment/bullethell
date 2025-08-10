import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random

class PatternTestA(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 15):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/ultraswing.wav")
        self.snd_spawn.set_volume(0.5)

    def update(self):
        self.frame += 1
        if self.frame % self.interval == 0:
            soul = self.soul

            bullet = BulletRain(self.board.x - 300, self.board.y, 0, 0.2)
            self.bullets.append(bullet)
