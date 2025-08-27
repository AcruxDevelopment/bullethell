import pygame
from object import GameObject
from textures import Textures

soulr_image = None
soulrh_image = None
souly_image = None
soulyh_image = None
soul_img_Size = 37
def loadAssets():
	global soulr_image
	global soulrh_image
	global souly_image
	global soulyh_image
	if not(soulr_image is None):
		return
	try:
		soulr_image = Textures.scaleToFit(Textures.load("soul_r.webp"), soul_img_Size, soul_img_Size)
		soulrh_image = Textures.scaleToFit(Textures.load("soul_rh.webp"), soul_img_Size, soul_img_Size)
		souly_image = Textures.scaleToFit(Textures.load("soul_y.webp"), soul_img_Size, soul_img_Size)
		soulyh_image = Textures.scaleToFit(Textures.load("soul_yh.webp"), soul_img_Size, soul_img_Size)
	except Exception as e:
		print("Failed to load texture, using fallback polygon:", e)
		soulr_image = pygame.Surface((40, 40), pygame.SRCALPHA)
		pygame.draw.polygon(soulr_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Soul(GameObject):
	def __init__(self, x, y, vel = 5, hp = 120):
		loadAssets()
		super().__init__(x, y, 0, soulr_image)
		self.vel = vel
		self.max_hp = hp
		self.hp = hp
		self.size = 37
		self.u, self.l, self.d, self.r = False, False, False, False
		self.m = 'r'

	def setMode(self, mode):
		self.m = mode
		soul_image = soulr_image if self.m == 'r' else souly_image
		self.original_image = soul_image

	def evade(self, bullets, center, board):
		everCollided = False
		xo = self.x
		yo = self.y
		do = self.degree
		dist = 0
		dist_max = 100
		dist_step = 10
		deg_step = 5
		while dist < dist_max:
			self.point_to(center.x, center.y)
			deg = self.degree
			self.degree = 0
			for i in range(360//deg_step):
				deg += deg_step
				self.x = xo
				self.y = yo
				self.move_in_direction(dist, deg)
				col = False
				col = self.x + self.size > board.x + board.size/2
				col = col or self.x - self.size < board.x - board.size/2
				col = col or self.y - self.size < board.y - board.size/2
				col = col or self.y + self.size > board.y + board.size/2
				for b in bullets:
					if b.touches(self):
						col = True
						everCollided = True
						break
				if not col:
					self.degree = do
					return everCollided
			dist += dist_step
		self.degree = do
		return everCollided
