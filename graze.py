import pygame
from object import GameObject
from textures import Textures

graze_image = None
def loadAssets():
    global graze_image
    if not(graze_image is None):
        return
    try:
        graze_image = Textures.scaleToFit(Textures.load("graze.webp"), 37 + 30, 37 + 30)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        graze_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(graze_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Graze(GameObject):
    def __init__(self, soul):
        global graze_image
        loadAssets()
        super().__init__(0, 0, 0, graze_image, True, 35)
        self.soul = soul
        self.showGraze = 0

    def graze(self):
        self.showGraze = 10

    def update(self):
        self.x = self.soul.x
        self.y = self.soul.y
        self.showGraze -= 1
        self.visible = self.showGraze > 0
