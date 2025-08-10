import pygame
import math
from object import GameObject
from textures import Textures

spade_image = None
def loadAssets():
    global spade_image
    if not(spade_image is None):
        return
    try:
        spade_image = Textures.scaleToFit(Textures.load("spade.png"), 40, 40)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        spade_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(spade_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class BulletRain(GameObject):
    def __init__(self, x, y, degree, facc = 0.1, svel = 0):
        loadAssets()
        super().__init__(x, y, degree, spade_image, True, 15)
        self.svel = svel
        self.fvel = 0
        self.facc = facc
        self.frame = 0
        self.grazed = False

    def update(self):
        self.frame += 1
        self.fvel += self.facc
        self.move_in_direction(self.fvel, self.degree)
        self.move_in_direction(self.svel, self.degree+90)
