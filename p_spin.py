import pygame
from object import GameObject
from soul import Soul
from board import Board
from bullet_static import BulletStatic
from pattern import Pattern
import random
import math
from textures import Textures

barriers = [
    "# ### ##",
    "#  # ###",
    "## ## ##",
    "# ###   ",
    " ## ##  "
]

barriers = [
    "# ### ##",
    "## # ###",
    "## ## ##",
    "# ### # ",
    " ## ### "
]

def barrier_off_screen_del_cond(self:BulletStatic):
    return False

def off_screen_del_cond(self:BulletStatic):
    return self.x > 200

def souldir(board):
    return 90

nonbreak_bullet_image = None
break_bullet_image = None
alpha_image = None
spinedge_bullet_image = None
def loadAssets():
    global nonbreak_bullet_image
    global break_bullet_image
    global alpha_image
    global spinedge_bullet_image
    if not(break_bullet_image is None) and not(alpha_image is None):
        return
    try:
        alpha_image = Textures.scaleToFit(Textures.load("alpha.webp"), 40, 40)
        break_bullet_image = Textures.scaleToFit(Textures.load("break_wall_full.png"), 40, 40)
        nonbreak_bullet_image = Textures.scaleToFit(Textures.load("wall_full.png"), 40, 40)
        spinedge_bullet_image = Textures.scaleToFit(Textures.load("spin_edge.png"), 40, 40)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        break_bullet_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(break_bullet_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class PatternSpin(Pattern):
    def __init__(self, soul, board, bullets, center, set_battle_time, interval = 40, nvel = 6, nacc = 0.05, rvel = 7, racc = 0.05, reverseDelay = 250):
        super().__init__(soul, board, bullets, center, 'y', souldir, set_battle_time)
        global break_bullet_image
        loadAssets()
        self.interval = interval
        self.degree = 0
        self.nvel = nvel
        self.rvel = rvel
        self.nacc = nacc
        self.racc = racc
        self.reverseDelay = reverseDelay
        self.snd_spawn = pygame.mixer.Sound("sfx/hypnosis.wav")
        self.vel = -nvel / 2
        self.barriers = []
        self.prevAreOff = {}
        self.end = False

    def start(self):
        super().start()
        self.set_battle_time(100000)

    def barrier(self, barrier):
        global break_bullet_image
        global nonbreak_bullet_image
        x = self.board.x + self.board.size/2 + 300
        y = self.board.y + self.board.size/2
        gap = 40
        barrierobj = GameObject(0, 0, 0, None, False, 1, barrier_off_screen_del_cond)
        for i in barrier:
            breakable = i == ' '
            sprite = break_bullet_image if breakable else nonbreak_bullet_image
            bullet = BulletStatic(x, y, 180, sprite, breakable, 20)
            bullet.off_screen_del_cond = off_screen_del_cond
            self.bullets.append(bullet)
            self.prevAreOff[bullet] = True
            self.add_child(bullet)
            barrierobj.add_child(bullet)
            y -= gap
        for i in range(2):
            bullet = BulletStatic(x, y, 180, spinedge_bullet_image, False, 0)
            bullet.off_screen_del_cond = off_screen_del_cond
            self.bullets.append(bullet)
            barrierobj.add_child(bullet)
        self.barriers.append(barrierobj)

    def rbarrier(self):
        self.barrier(barriers[random.randint(0, len(barriers)-1)])

    def update(self):
        super().update()
        if len(self.barriers) > 0 and self.barriers[0].x > -50 and self.frame > self.reverseDelay and not self.end:
            self.set_battle_time(1)
            self.end = True

        if self.frame % self.interval == 0 and self.vel != self.rvel:
            self.rbarrier()
        if self.frame < self.reverseDelay:
            self.vel -= self.nacc
            if(self.vel < -self.nvel): self.vel = -self.nvel
        else:
            self.vel += self.racc
            if(self.vel > self.rvel): self.vel = self.rvel

        for i in self.barriers:
            i.x += self.vel
            i.y = 20 + math.sin(i.x * 0.005) * 70 # 20 = gap/2
            j = 0
            for bullet in i.children:
                if j == len(i.children)-1:
                    bullet.y = self.board.y + self.board.size/2 + 40
                if j == len(i.children)-2:
                    bullet.y = self.board.y - self.board.size/2 - 40
                j += 1

        for i in self.children:
            isOff = not((i.y-40 < (self.board.y + self.board.size/2)) and (i.y+40 > (self.board.y - self.board.size/2))) and i.radius != 1
            if self.prevAreOff[i] and not isOff:
                    i.morph_to(break_bullet_image, 0.01)
            if not self.prevAreOff[i] and isOff:
                    i.morph_to(alpha_image, 0.01)
            self.prevAreOff[i] = isOff

        self.frame += 1

