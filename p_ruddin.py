import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_circle import BulletCircle
from pattern import Pattern
import random

class PatternHathy(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 100):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/ultraswing.wav")
        self.snd_spawn.set_volume(0.5)

    def update(self):
        soul = self.soul
        self.frame += 1
        if self.frame % self.interval == 0:
            rx = random.randint(-self.board.size//2, self.board.size//2)
            ry = random.randint(-self.board.size//2, self.board.size//2)
            bullet = BulletCircle(self.center[0]+rx, self.center[1]+ry, 10, 400, 3, self.bullets, False, 80, 3, 100)
            self.bullets.append(bullet)
