import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random

class RuddinB(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 25):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/ultraswing.wav")
        self.snd_spawn.set_volume(0.5)

    def update(self):
        self.frame += 1
        if self.frame % self.interval == 0:
            soul = self.soul
            for i in range(6):
                bullet = BulletRain(self.board.x-(60*(i-(6/2))), self.board.y-self.board.size/2, 90, 0.2)
                soul_pred = [soul.x, soul.y]
                if(soul.u): soul_pred[1] += soul.vel * (bullet.distance(soul)*0.01)
                if(soul.d): soul_pred[1] -= soul.vel * (bullet.distance(soul)*0.01)
                if(soul.l): soul_pred[0] -= soul.vel * (bullet.distance(soul)*0.01)
                if(soul.r): soul_pred[0] += soul.vel * (bullet.distance(soul)*0.01)
                bullet.point_to(soul_pred[0], soul_pred[1])
                #self.snd_spawn.play()
                self.bullets.append(bullet)
