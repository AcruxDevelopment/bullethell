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

def barrier_off_screen_del_cond(self:BulletRain):
    return False

def off_screen_del_cond(self:BulletRain):
    return False

def souldir(pattern):
#def unused(pattern):
    pass
    soul:Soul = pattern.soul
    board:Board = pattern.board
    soul.point_to(board.x, board.y)
    return (soul.degree - 90)+180 + math.sin(pattern.frame * 0.1) * 15

def __souldir(pattern):
    closest = None
    dist = 99999999999
    for i in pattern.bullets:
        idist = i.distance(pattern.soul)
        if idist < dist:
            dist = idist
            closest = i
    if closest is None: return 0
    pattern.soul.point_to(closest.x, closest.y)
    return (pattern.soul.degree - 90)+ (180*0)

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

class PatternCastle(Pattern):
    def __init__(self, soul, board, bullets, center, set_battle_time, interval = 22):
        super().__init__(soul, board, bullets, center, 'y', souldir, set_battle_time)
        global break_bullet_image
        loadAssets()
        self.interval = interval

    def start(self):
        super().start()

    def update(self):
        super().update()
        self.frame += 1

        for i in self.bullets:
            i.point_to(self.soul.x, self.soul.y)
            mxvel = 5
            minvel = 2.6
            i.fvel = max(min(mxvel, mxvel * i.distance(self.soul)/700), minvel)

        if self.frame % self.interval != 1: return
        bullet = BulletRain(self.board.x, self.board.y, 0, 0, 0, 0, breakable=True, image=break_bullet_image)
        #bullet.degree = random.randint(0, 359)
        bullet.point_to(self.soul.x, self.soul.y)
        bullet.degree += random.randint(-50, 50)
        if random.randint(0, 2) == 0: bullet.degree += 180
        bullet.move_in_direction(500, bullet.degree)
        bullet.degree += 180
        bullet.off_screen_del_cond = off_screen_del_cond
        self.bullets.append(bullet)

