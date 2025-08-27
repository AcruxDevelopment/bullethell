import pygame
from gobject import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random

class RuddinA(Pattern):
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

            bullet = BulletRain(self.board.x, self.board.y, 0, 0.2)
            bullet.degree = random.randint(0, 359)
            bullet.move_in_direction(300, bullet.degree)


            soul_pred = [soul.x, soul.y]
            if(soul.u): soul_pred[1] += soul.vel * (bullet.distance(soul)*0.15)
            if(soul.d): soul_pred[1] -= soul.vel * (bullet.distance(soul)*0.15)
            if(soul.l): soul_pred[0] -= soul.vel * (bullet.distance(soul)*0.15)
            if(soul.r): soul_pred[0] += soul.vel * (bullet.distance(soul)*0.15)
            if random.randint(0, 2) == 0:
                bullet.point_to(soul_pred[0], soul_pred[1])
            else:
                bullet.point_to(soul.x, soul.y)
            #self.snd_spawn.play()
            self.bullets.append(bullet)
