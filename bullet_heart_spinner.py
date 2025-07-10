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
        spade_image = Textures.scaleToFit(Textures.load("spade.png"), 20, 20)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        spade_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(spade_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class BulletHeartSpinner(GameObject):
    def __init__(self, x, y, degree, vel = 5):
        loadAssets()
        super().__init__(x, y, degree, spade_image, False)
        self.offset = 30
        self.vel = vel
        self.frame = 0
        #self.spade1 = GameObject(x - self.offset, y - self.offset, -45, spade_image)
        #self.spade2 = GameObject(x + self.offset, y - self.offset, 45, spade_image)
        #self.spade3 = GameObject(x - self.offset, y + self.offset, -127, spade_image)
        #self.spade4 = GameObject(x + self.offset, y + self.offset, 127, spade_image)
        self.spade1 = GameObject(x - self.offset, y - self.offset, 0, spade_image)
        self.spade2 = GameObject(x + self.offset, y - self.offset, 0, spade_image)
        self.spade3 = GameObject(x - self.offset, y + self.offset, 0, spade_image)
        self.spade4 = GameObject(x + self.offset, y + self.offset, 0, spade_image)
        self.spades = [self.spade1, self.spade2, self.spade3, self.spade4]
        for spade in self.spades:
            spade.lock_angle_to_world = True
            self.add_child(spade)

    def update(self):
        self.move_by(self.vel, 0)
        self.rotate_around((self.x, self.y), -1.5)
        self.move_by(0, math.sin(self.frame/20)*3)
        self.frame += 1