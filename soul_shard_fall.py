import pygame
from object import GameObject
from textures import Textures
import random

soull_image = None
soulr_image = None
alpha_image = None
def loadAssets():
    global soull_image
    global soulr_image
    global alpha_image
    if not(soulr_image is None):
        return
    try:
        soull_image = Textures.scaleToFit(Textures.load("soulbs1.webp"), 37, 37)
        soulr_image = Textures.scaleToFit(Textures.load("soulbs2.webp"), 37, 37)
        alpha_image = Textures.scaleToFit(Textures.load("alpha.webp"), 37, 37)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])
        soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])
        alpha_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(alpha_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class SoulShardFall(GameObject):
    def __init__(self, x, y, vx, vy, num):
        loadAssets()
        super().__init__(x, y, random.randint(0, 8) * 45, soull_image if num == 0 else soulr_image)
        self.frame = 0
        self.vx = vx
        self.vy = vy
        self.grav = 0.3
        self.fric = 1
        self.num = num

    def update(self):
        if self.frame == 0:
            #self.morph_to(alpha_image, 1)
            pass

        self.x += self.vx
        self.y += self.vy
        self.vy -= self.grav
        self.vx *= self.fric
        self.vy *= self.fric
        if self.frame % 10 == 0:
            self.degree += 45
            if self.num == 1:
                self.morph_to(soull_image, 0.01)
                self.num = 0
            else:
                self.morph_to(soulr_image, 0.01)
                self.num = 1
        self.frame += 1

    