import pygame
from gobject import GameObject
from soul import Soul
from board import Board

def newSoulDegree(pattern):
    return 0

class Pattern(GameObject):
    def __init__(self, soul, board, bullets, center, soulmode = 'r', souldegree = None, set_battle_time = None):
        super().__init__(board.x, board.y, 0, None, False)
        self.soul = soul
        self.board = board
        self.bullets = bullets
        self.frame = 0
        self.center = center
        self.soulmode = soulmode
        self.souldegree = souldegree if souldegree is not None else newSoulDegree
        self.set_battle_time = set_battle_time

    def start(self):
        self.frame = 0
        self.soul.setMode(self.soulmode)
        self.soul.degree = self.souldegree(self)

    def update(self):
        self.soul.degree = self.souldegree(self)
