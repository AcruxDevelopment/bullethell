import pygame
import math
from object import GameObject
from textures import Textures

spade_image = None
spade_spawn_image = None
def loadAssets():
    global spade_image
    global spade_spawn_image
    if not(spade_image is None) and not(spade_spawn_image is None):
        return
    try:
        spade_spawn_image = Textures.scaleToFit(Textures.load("alpha.webp"), 40, 40)
        spade_image = Textures.scaleToFit(Textures.load("spade.png"), 40, 40)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        spade_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(spade_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class BulletRain(GameObject):
    def __init__(self, x, y, degree, facc = 0.1, svel = 0, fvel = 0):
        loadAssets()
        super().__init__(x, y, degree, spade_spawn_image, True, 17)
        self.svel = svel
        self.fvel = fvel
        self.facc = facc
        self.frame = 0
        self.grazed = False

    def damage(self, soul):
        soul.hp -= 15

    def update(self):
        if self.frame == 0:
            self.morph_to(spade_image, 0.5)
        self.frame += 1
        self.fvel += self.facc
        self.move_in_direction(self.fvel, self.degree)
        self.move_in_direction(self.svel, self.degree+90)
