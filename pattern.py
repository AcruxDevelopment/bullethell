import pygame
from object import GameObject
from soul import Soul
from board import Board

class Pattern(GameObject):
    def __init__(self, soul, board, bullets, center):
        super().__init__(board.x, board.y, 0, None, False)
        self.soul = soul
        self.board = board
        self.bullets = bullets
        self.frame = 0
        self.center = center

    def start(self):
        self.frame = 0
