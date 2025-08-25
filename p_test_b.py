import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random
import math

class PatternTestB(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 20):
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
            rnd = random.randint(-15, 15)
            bullet = BulletRain(self.board.x - 300, rnd + self.board.y - -math.sin(self.frame * 0.1)*120, 0, 0.05)
            self.bullets.append(bullet)
            bullet = BulletRain(rnd + self.board.x - math.sin(self.frame * 0.1)*120, self.board.y + 300,-90, 0.05)
            self.bullets.append(bullet)
