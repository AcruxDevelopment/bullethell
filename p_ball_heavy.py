import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_ball import BulletBall
from bullet_ball_fall import BulletBallFall
from pattern import Pattern
import random
import math

class PatternBallHeavy(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 20, acc = 0.1):
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
        if self.frame % self.interval != 0: return
        self.snd_spawn.play()
        vx = random.randint(-5, 5)
        vy = random.randint(1, 5)
        xoff = random.randint(-self.board.size//2, self.board.size//2)
        bullet = BulletBallFall(self.board.x + xoff, (self.board.y + self.board.size/2)+100, 0, self.board, .5, vy, vx, .3)
        self.bullets.append(bullet)



