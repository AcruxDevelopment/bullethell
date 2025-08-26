import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_rain import BulletRain
from pattern import Pattern
import random
import math
from textures import Textures

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
    "##  ##  ",
    "# ## ## ",
    "  #  #  ",
    "##  ##  ",
    " # # # #",
    "  ###  #",
    " #  ### "
]
ebarriers = barriers

def off_screen_del_cond(self:BulletRain):
    return self.y < 0

def soulangle(pattern):
    return -180

nonbreak_bullet_image = None
break_bullet_image = None
def loadAssets():
    global nonbreak_bullet_image
    global break_bullet_image
    if not(break_bullet_image is None):
        return
    try:
        break_bullet_image = Textures.scaleToFit(Textures.load("break_wall_full.png"), 40, 40)
        nonbreak_bullet_image = Textures.scaleToFit(Textures.load("wall_full.png"), 40, 40)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        break_bullet_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(break_bullet_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class PatternReverseFall(Pattern):
    #def __init__(self, soul, board, bullets, center, count = 40, iacc = 3, sacc = 0.5, interval = 100):
    def __init__(self, soul, board, bullets, center, count = 40, iacc = 2, sacc = 0.6, interval = 90):
        super().__init__(soul, board, bullets, center, 'y', soulangle)
        loadAssets()
        self.frame = 0
        self.count = count
        self.acc = iacc
        self.sacc = sacc
        self.tick = 0
        self.barriers = []
        self.barrierSigns = []
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
        self.x = self.board.x

        #self.x = -self.soul.x * 0.25
        
        j = 0
        for i in self.barriers:
            i.x = (math.sin(self.frame*0.01) * 55) * self.barrierSigns[j]
            j += 1

        if self.frame != 1: return

        y = (self.board.y + self.board.size/2) + 0
        j = 1
        safen = random.randint(0, len(barriers)-1)
        for i in range(self.count):
            barrierobj = GameObject(0, 0, 0, None, False, 1, lambda x: False)
            k = 0
            x = self.board.x - self.board.size/2 + bulletgap/2
            barrier = barriers[random.randint(0, len(barriers)-1)] if j < 9 else ebarriers[random.randint(0, len(ebarriers)-1)]
            for i in barrier:
                breakable = i == ' ' and not(j < 9 and k == safen)
                image = break_bullet_image if breakable else nonbreak_bullet_image
                bullet = BulletRain(x, y, -90, 0, 0, self.acc, breakable, image)
                bullet.off_screen_del_cond = off_screen_del_cond
                self.bullets.append(bullet)
                self.add_child(bullet)
                x += bulletgap
                k += 1
                barrierobj.add_child(bullet)
            y += 280 + j*30
            j += 1 
            self.acc += self.sacc + (j*0.01)
            self.barriers.append(barrierobj)
            sign = 1 if random.randint(0, 1) == 0 else -1
            self.barrierSigns.append(sign)

