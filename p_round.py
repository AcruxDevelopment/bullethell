import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random

class PatternRound(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 7):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/ultraswing.wav")
        self.snd_spawn.set_volume(0.5)
        self.sound_delay = 5

    def update(self):
        soul = self.soul
        self.frame += 1
        if self.frame % self.interval == 0:
            for i in range(3):
                bullet = BulletRain(self.board.x, self.board.y, 0, 0.1)
                bullet.degree = self.degree
                bullet.move_in_direction(200 + (25 * i), bullet.degree)
                bullet.degree += 180
                self.bullets.append(bullet)
                self.degree += 10
            if self.sound_delay <= 0:
                self.snd_spawn.play()
            else:
                self.sound_delay -= 1
