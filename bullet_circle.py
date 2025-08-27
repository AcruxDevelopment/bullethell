import pygame
import math
from gobject import GameObject
from textures import Textures
from bullet_static import BulletStatic

def off_screen_del_cond(self:BulletStatic):
    return self.frame > 250

alpha_image = None
bullet_image = None
def loadAssets():
    global alpha_image
    global bullet_image
    if not(alpha_image is None):
        return
    try:
        alpha_image = Textures.scaleToFit(Textures.load("alpha.webp"), 40, 40)
        bullet_image = Textures.scaleToFit(Textures.load("spade.png"), 40, 40)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)

class BulletCircle(GameObject):
    def __init__(self, x, y, count, dist, vel, bullets, dorotate = True, destDist = None, distVel = 1, banish_delay = 20):
        loadAssets()
        super().__init__(x, y, 0, alpha_image, True, 20)
        self.dist = dist
        self.vel = vel
        self.frame = 0
        self.grazed = False
        self.destDist = destDist
        self.banish_delay = banish_delay
        if self.destDist is None:
            self.destDist = dist
        self.distVel = distVel
        degree_step = 360 / count
        degree = 0
        self.nocollide = True
        for i in range(0, count):
            bullet = BulletStatic(x, y, degree)
            bullet.off_screen_del_cond = off_screen_del_cond
            bullet.move_in_direction(dist, bullet.degree)
            bullet.degree = 90
            if not dorotate:
                bullet.lock_angle_to_world = True
            bullets.append(bullet)
            self.add_child(bullet)
            degree += degree_step

    def setDist(self, value):
        self.dist = value
        for i in self.children:
            if i.y > 1000: #for removal
                continue
            i.point_to(self.x, self.y)
            i.x = self.x
            i.y = self.y
            i.degree += 180
            i.move_in_direction(self.dist, i.degree)
            i.degree = 90

    def update(self):
        global alpha_image
        global bullet_image
        self.frame += 1
        self.degree += self.vel
        if self.dist > self.destDist:
            self.setDist(self.dist - self.distVel)

        if self.frame == self.banish_delay:
            for i in self.children:
                i.morph_to(alpha_image, 0.3)
        if self.frame > self.banish_delay + 14:
            self.x = 10000
