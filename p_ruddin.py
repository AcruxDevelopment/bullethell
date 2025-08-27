import pygame
from gobject import GameObject
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

    def start(self):
        super().start()

    def update(self):
        super().update()
        soul = self.soul
        self.frame += 1
        if self.frame % self.interval == 0:
            rx = random.randint((-self.board.size//2)+30, (self.board.size//2)-30)
            ry = random.randint((-self.board.size//2)+30, (self.board.size//2)-30)
            bullet = BulletCircle(self.center[0]+rx, self.center[1]+ry, 10, 400, 3, self.bullets, False, 50, 3, 100) #50 -> 80
            bullet.setDist(bullet.distance(self.soul)+200)
            self.bullets.append(bullet)
