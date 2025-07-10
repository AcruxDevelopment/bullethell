import pygame
from object import GameObject
from textures import Textures

soul_image = None
def loadAssets():
    global soul_image
    if not(soul_image is None):
        return
    try:
        soul_image = Textures.scaleToFit(Textures.load("soul.webp"), 30, 30)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soul_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soul_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Soul(GameObject):
    def __init__(self, x, y, vel = 5):
        loadAssets()
        super().__init__(x, y, 0, soul_image)
        self.vel = vel