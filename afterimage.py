import pygame
from object import GameObject
from textures import Textures

alpha_image = None
def loadAssets():
    global alpha_image
    if not(alpha_image is None):
        return
    try:
        alpha_image = Textures.scaleToFit(Textures.load("alpha.webp"), 1, 1)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soul_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soul_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Afterimage(GameObject):

    def __init__(self, image, time, x, y, vx = 0, vy = 0, ax = 0, ay = 0):
        loadAssets()
        super().__init__(x, y, 0, image)
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.time = time
        self.frame = 0
        self.og_image = image

    def new_from(object, time = 0.5, vx = 0, vy = 0, ax = 0, ay = 0):
        return Afterimage(object.image, time, object.x, object.y, vx, vy, ax, ay)

    def update(self):
        global alpha_image
        if self.frame == 0:
            self.morph_to(alpha_image, self.time)

        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay
        self.frame += 1

    def end(self):
        return self.image != self.og_image
