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

class BulletStatic(GameObject):
    def __init__(self, x, y, degree, image = None, breakable = True, rad = 20):
        global spade_image
        global spade_spawn_image
        loadAssets()
        if image is None: image = spade_image
        self.eeeimage = image
        super().__init__(x, y, degree, spade_spawn_image, True, rad)
        self.frame = 0
        self.grazed = False
        self.breakable = breakable

    def damage(self, soul):
        soul.hp -= 25

    def update(self):
        if self.frame == 0:
            self.morph_to(self.eeeimage, 0.1)
        self.frame += 1
