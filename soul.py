import pygame
from object import GameObject
from textures import Textures

soul_image = None
soulh_image = None
def loadAssets():
    global soul_image
    global soulh_image
    if not(soul_image is None):
        return
    try:
        soul_image = Textures.scaleToFit(Textures.load("soul.webp"), 37, 37)
        soulh_image = Textures.scaleToFit(Textures.load("soulh.webp"), 37, 37)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soul_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soul_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Soul(GameObject):
    def __init__(self, x, y, vel = 5, hp = 120):
        loadAssets()
        super().__init__(x, y, 0, soul_image)
        self.vel = vel
        self.max_hp = hp
        self.hp = hp
        self.size = 37
        self.u, self.l, self.d, self.r = False, False, False, False

    def evade(self, bullets, center, board):
         xo = self.x
         yo = self.y
         dist = 0
         dist_max = 800
         dist_step = 1
         deg_step = 10
         while dist < dist_max:
             self.point_to(center.x, center.y)
             deg = self.degree
             self.degree = 0
             for i in range(360//deg_step):
                 deg += deg_step
                 self.x = xo
                 self.y = yo
                 self.move_in_direction(dist, deg)
                 col = False
                 col = self.x + self.size > board.x + board.size/2
                 col = col or self.x - self.size < board.x - board.size/2
                 col = col or self.y - self.size < board.y - board.size/2
                 col = col or self.y + self.size > board.y + board.size/2
                 for b in bullets:
                     if b.touches(self):
                         col = True
                         break
                 if not col:
                     return
             dist += dist_step
