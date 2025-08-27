import pygame
from gobject import GameObject
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
    "# ### ###  ",
    "## # ### ##",
    "## ## ## # ",
    "# ### # # #",
    " ## ### ## "
]

def barrier_off_screen_del_cond(self:BulletStatic):
    return False

def off_screen_del_cond(self:BulletStatic):
    return False

def souldir(pattern):
    soul:Soul = pattern.soul
    board:Board = pattern.board
    soul.point_to(board.x + board.size/2, board.y + board.size/2)
    return (soul.degree + 90) - 90

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

class PatternPendulum(Pattern):
    def __init__(self, soul, board, bullets, center, set_battle_time, deginterval = 25, nvel = .7, nacc = 0.05, rvel = .7, racc = 0.01, reverseDelay = 490):
        super().__init__(soul, board, bullets, center, 'y', souldir, set_battle_time)
        global break_bullet_image
        loadAssets()
        self.deginterval = deginterval
        self.degree = 0
        self.snd_spawn = pygame.mixer.Sound("sfx/hypnosis.wav")
        self.barriers = []
        self.prevAreOff = {}
        self.end = False
        self.nvel = nvel
        self.rvel = rvel
        self.nacc = nacc
        self.racc = racc
        self.vel = 0
        self.reverseDelay = reverseDelay
        self.timeOnMaxReverseVel = 0
        self.gap = 50
        self.rotated = 0
        self.rotationLeft = deginterval

    def start(self):
        super().start()
        self.set_battle_time(100000)

    def barrier(self, barrier):
        global break_bullet_image
        global nonbreak_bullet_image
        board:Board = self.board
        centerOffset = 100
        x = self.board.x + self.board.size/2 + centerOffset
        y = self.board.y + self.board.size/2 + centerOffset
        gap = self.gap
        barrierobj = GameObject(board.x + board.size/2 + centerOffset, board.y + board.size/2 + centerOffset, 0, None, False, 1, barrier_off_screen_del_cond)
        for i in barrier:
            breakable = i == ' '
            sprite = break_bullet_image if breakable else nonbreak_bullet_image
            bullet = BulletStatic(x, y, 180, sprite, breakable, 20)
            bullet.off_screen_del_cond = off_screen_del_cond
            self.bullets.append(bullet)
            self.prevAreOff[bullet] = False
            self.add_child(bullet)
            barrierobj.add_child(bullet)
            y -= gap
        for i in range(2):
            bullet = BulletStatic(x, y, 180, spinedge_bullet_image, False, 1)
            bullet.off_screen_del_cond = off_screen_del_cond
            self.bullets.append(bullet)
            self.prevAreOff[bullet] = False
            barrierobj.add_child(bullet)
            self.add_child(bullet)
        self.barriers.append(barrierobj)

    def rbarrier(self):
        self.barrier(barriers[random.randint(0, len(barriers)-1)])

    def update(self):
        super().update()
        if not self.end and self.timeOnMaxReverseVel > 380:
            self.set_battle_time(1)
            self.end = True

        if self.rotationLeft == self.deginterval and self.rotated < 360 and self.vel != self.rvel:
            self.rbarrier()
        if self.frame < self.reverseDelay:
            self.vel -= self.nacc
            if(self.vel < -self.nvel): self.vel = -self.nvel
        else:
            self.vel += self.racc
            if(self.vel > self.rvel): self.vel = self.rvel

        if self.vel < 0:
            self.rotationLeft += self.vel
        self.rotated += -self.vel
        if self.rotationLeft < 0: self.rotationLeft = self.deginterval

        barriers_to_remove = []
        for i in self.barriers:
            i.degree += self.vel
            j = 0
            for bullet in i.children:
                if j < 3:
                    bullet.visible = False
                j += 1
            #if i.degree < 90:
                #barriers_to_remove.append(i)
        
        for i in barriers_to_remove:
            self.barriers.remove(i)
            for bullet in i.children:
                self.bullets.remove(bullet)

        j = 0
        for i in self.children:
            # 12 = 11 bullets in barrier + 1 edge bullet
            visible_bullet_image = break_bullet_image if i.breakable else nonbreak_bullet_image if j % 13 != 12 else spinedge_bullet_image
            isOff = (i.y > self.board.y + self.board.size/2 + 50)
            if self.prevAreOff[i] and not isOff:
                    i.morph_to(visible_bullet_image, 0.15)
            if not self.prevAreOff[i] and isOff:
                    i.morph_to(alpha_image, 0.3)
            self.prevAreOff[i] = isOff
            j += 1

        if self.vel == self.rvel:
            self.timeOnMaxReverseVel += 1
        else:
            self.timeOnMaxReverseVel = 0

        self.frame += 1

