import pygame
from object import GameObject
from textures import Textures

soull_image = None
soulr_image = None
def loadAssets():
    global soull_image
    global soulr_image
    if not(soulr_image is None):
        return
    try:
        soull_image = Textures.scaleToFit(Textures.load("soulbl.webp"), 37, 37)
        soulr_image = Textures.scaleToFit(Textures.load("soulbr.webp"), 37, 37)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])
        soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class SoulShard(GameObject):
    def __init__(self, x, y, isLeft):
        loadAssets()
        super().__init__(x, y, 0, soull_image if isLeft else soulr_image)
        self.isLeft = isLeft
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame < 3:
            self.x += -3 if self.isLeft else 3

    