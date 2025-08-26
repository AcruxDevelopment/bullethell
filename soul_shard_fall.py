import pygame
from object import GameObject
from textures import Textures
import random

soulr1_image = None
soulr2_image = None
soulb1_image = None
soulb2_image = None
souly1_image = None
souly2_image = None
alpha_image = None
def loadAssets():
    global soulr1_image
    global soulr2_image
    global soulb1_image
    global soulb2_image
    global souly1_image
    global souly2_image
    global alpha_image
    if not(soulr2_image is None):
        return
    try:
        soulr1_image = Textures.scaleToFit(Textures.load("soulbs1.webp"), 37, 37)
        soulr2_image = Textures.scaleToFit(Textures.load("soulbs2.webp"), 37, 37)
        soulb1_image = Textures.scaleToFit(Textures.load("soulbs1_blue.webp"), 37, 37)
        soulb2_image = Textures.scaleToFit(Textures.load("soulbs2_blue.webp"), 37, 37)
        souly1_image = Textures.scaleToFit(Textures.load("soulbs1_yellow.webp"), 37, 37)
        souly2_image = Textures.scaleToFit(Textures.load("soulbs2_yellow.webp"), 37, 37)
        alpha_image = Textures.scaleToFit(Textures.load("alpha.webp"), 37, 37)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soulr2_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr2_image, (0, 255, 0), [(20,0),(40,40),(0,40)])
        soulr2_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr2_image, (0, 255, 0), [(20,0),(40,40),(0,40)])
        alpha_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(alpha_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class SoulShardFall(GameObject):
    def __init__(self, x, y, vx, vy, num):
        loadAssets()
        super().__init__(x, y, random.randint(0, 8) * 45, alpha_image)
        self.frame = 0
        self.vx = vx
        self.vy = vy
        self.grav = 0.3
        self.fric = 1
        self.num = num
        self.pick_color()

    def pick_color(self):
        if self.num == 1:
            self.morph_to(soulr1_image, 0.01)
            self.num = 0
        elif self.num == 0:
            self.morph_to(soulr2_image, 0.01)
            self.num = 1

        if self.num == 2:
            self.morph_to(soulb1_image, 0.01)
            self.num = 3
        elif self.num == 3:
            self.morph_to(soulb2_image, 0.01)
            self.num = 2

        if self.num == 4:
            self.morph_to(souly1_image, 0.01)
            self.num = 5
        elif self.num == 5:
            self.morph_to(souly2_image, 0.01)
            self.num = 4

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
            self.pick_color()
        self.frame += 1

    