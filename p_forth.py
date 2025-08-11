import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random
import math

class PatternForth(Pattern):
    def __init__(self, soul, board, bullets, center, interval = 20, acc = 0.1):
        super().__init__(soul, board, bullets, center)
        self.interval = interval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/ultraswing.wav")
        self.snd_spawn.set_volume(0.5)
        self.phase = -1
        self.acc = acc

    def update(self):
        ac = self.acc
        self.frame += 1
        if self.frame % self.interval != 0: return
        self.phase += 1
        if self.phase > 3: self.phase = 0

        if self.phase == 0:
                self.snd_spawn.play()
                board = self.board
                xc = board.x
                while(xc > board.x - board.size/2):
                    bullet = BulletRain(xc, board.y + board.size + 100, -90, ac)
                    self.bullets.append(bullet)
                    xc -= 40

        if self.phase == 1:
                self.snd_spawn.play()
                board = self.board
                yc = board.y
                while(yc < board.y + board.size/2):
                    bullet = BulletRain(board.x + board.size + 100, yc, 180, ac)
                    self.bullets.append(bullet)
                    yc += 40

        if self.phase == 2:
                self.snd_spawn.play()
                board = self.board
                xc = board.x
                while(xc < board.x + board.size/2):
                    bullet = BulletRain(xc, board.y - board.size - 40, 90, ac)
                    self.bullets.append(bullet)
                    xc += 40

        if self.phase == 3:
                self.snd_spawn.play()
                board = self.board
                yc = board.y
                while(yc < board.y + board.size/2):
                    bullet = BulletRain(board.x - board.size - 100, yc, 0, ac)
                    self.bullets.append(bullet)
                    yc += 40
