import pygame
import math
from object import GameObject
from textures import Textures

gooner_image = None
def loadAssets():
    global gooner_image
    if not(gooner_image is None):
        return
    try:
        gooner_image = Textures.scaleToFit(Textures.load("hypergooner.png"), 550, 550)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        graze_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(graze_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Gooner(GameObject):
    def __init__(self, center):
        global gooner_image
        loadAssets()
        super().__init__(0, 0, 0, gooner_image, True, 35)
        self.frame = 0
        self.center = center

    def update(self):
        self.y = self.center[1] + math.sin(2*(self.frame * 0.03)) * 100
        self.x = self.center[0] + math.cos(self.frame * 0.03) * 200
        self.frame += 1
