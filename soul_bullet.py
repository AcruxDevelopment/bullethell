import pygame
from object import GameObject
from textures import Textures

small_image = None
big_image = None
def loadAssets():
    global small_image
    global big_image
    global souly_image
    global soulyh_image
    if not(small_image is None):
        return
    try:
        small_image = Textures.scaleToFit(Textures.load("soulbullet.webp"), 37, 37)
        big_image = Textures.scaleToFit(Textures.load("soul_rh.webp"), 37, 37)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        small_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(small_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class SoulBullet(GameObject):
    def __init__(self, x, y, degree, vel = 25, isBig = False):
        loadAssets()
        super().__init__(x, y, degree, small_image, True, 5)
        self.vel = vel
        self.size = 37
        self.isBig = isBig

    def update(self):
        self.move_in_direction(self.vel, self.degree)