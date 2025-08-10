import pygame
from object import GameObject
from soul import Soul
from board import Board

class Pattern:
    def __init__(self, soul, board, bullets, center):
        self.soul = soul
        self.board = board
        self.bullets = bullets
        self.frame = 0
        self.center = center
