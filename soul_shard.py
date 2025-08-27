import pygame
from gobject import GameObject
from textures import Textures

soull_image = None
soulr_image = None
soull_y_image = None
soulr_y_image = None
def loadAssets():
    global soull_image
    global soulr_image
    global soull_y_image
    global soulr_y_image
    if not(soulr_image is None):
        return
    try:
        soull_image = Textures.scaleToFit(Textures.load("soulbl.webp"), 37, 37)
        soulr_image = Textures.scaleToFit(Textures.load("soulbr.webp"), 37, 37)
        soull_y_image = Textures.scaleToFit(Textures.load("soulbl_yellow.webp"), 37, 37)
        soulr_y_image = Textures.scaleToFit(Textures.load("soulbr_yellow.webp"), 37, 37)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])
        soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class SoulShard(GameObject):
    def __init__(self, x, y, isLeft, deg, color = 'r'):
        loadAssets()
        super().__init__(x, y, deg, None)
        self.isLeft = isLeft
        self.frame = 0
        self.color = color
        self.original_image = self.pick_sprite()

    def pick_sprite(self):
        global soull_image
        global soulr_image
        global soull_y_image
        global soulr_y_image
        if self.color == 'r': return soull_image if self.isLeft else soulr_image
        if self.color == 'y': return soull_y_image if self.isLeft else soulr_y_image

    def update(self):
        vel = -3 if self.isLeft else 3
        self.frame += 1
        if self.frame < 3:
            self.move_in_direction(vel, self.degree)

    