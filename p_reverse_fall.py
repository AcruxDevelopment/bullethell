import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random
import math

barriers = [
    "# ##  # ",
    "## #   #",
    "  ## # #",
    "   ##  #",
    "## #  ## ",
    "##  ##  ",
    " ## ##  ",
    "#   ## #",
    "     ###"
]

ebarriers = [
    "#  #  # ",
    "## #   #",
    "  #  # #",
    "    #  #",
    "#  #  ## ",
    " #  # #  ",
    " ## ##  ",
    "#   ## #",
    "   # # #"
]

barriers = [
    "# #   # ",
    "#  #   #",
    "   # # #",
    " # #  ##",
    "## #   # ",
    "##   #  ",
    " ##  #  ",
    "#   ## #",
    "#    # #",
    "# # # # ",
    " # # # #"
]
ebarriers = barriers

def off_screen_del_cond(self:BulletRain):
    return self.y < 0

def soulangle(pattern):
    return -180

class PatternReverseFall(Pattern):
    #def __init__(self, soul, board, bullets, center, count = 40, iacc = 3, sacc = 0.5, interval = 100):
    def __init__(self, soul, board, bullets, center, count = 40, iacc = 2, sacc = 0.6, interval = 100):
        super().__init__(soul, board, bullets, center, 'y', soulangle)
        self.frame = 0
        self.count = count
        self.acc = iacc
        self.sacc = sacc
        self.tick = 0
        self.xtransormer = math.sin if random.randint(0, 1) == 0 else math.cos
        #self.degree = 0
        #self.snd_spawn = pygame.mixer.Sound("sfx/hypnosis.wav")

    def start(self):
        super().start()
        self.frame = 0
        self.degree

    def update(self):
        super().update()
        bulletgap = 40
        self.frame += 1
        self.x = self.board.x + self.xtransormer(self.frame*0.01) * 30

        #self.x = -self.soul.x * 0.25
        #self.x += self.xtransormer(self.frame*0.01) * 30
        if self.frame != 1: return

        y = (self.board.y + self.board.size/2) + 0
        j = 1
        safen = random.randint(0, len(barriers)-1)
        for i in range(self.count):
            k = 0
            x = self.board.x - self.board.size/2 + bulletgap/2
            barrier = barriers[random.randint(0, len(barriers)-1)] if j < 9 else ebarriers[random.randint(0, len(ebarriers)-1)]
            for i in barrier:
                if i == '#' and not(j < 9 and k == safen):
                    bullet = BulletRain(x, y, -90, 0, 0, self.acc)
                    bullet.off_screen_del_cond = off_screen_del_cond
                    self.bullets.append(bullet)
                    self.add_child(bullet)
                x += bulletgap
                k += 1
            y += 80 + j*30
            j += 1 

            self.acc += self.sacc + (j*0.01)

