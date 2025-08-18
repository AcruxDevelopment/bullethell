import pygame
import math
from object import GameObject
from textures import Textures

spade_image = None
spade_spawn_image = None
def loadAssets():
	global spade_image
	global spade_spawn_image
	if not(spade_image is None) and not(spade_spawn_image is None):
		return
	try:
		spade_spawn_image = Textures.scaleToFit(Textures.load("alpha.webp"), 40, 40)
		spade_image = Textures.scaleToFit(Textures.load("ball.webp"), 50, 50)
	except Exception as e:
		print("Failed to load texture, using fallback polygon:", e)
		spade_image = pygame.Surface((40, 40), pygame.SRCALPHA)
		pygame.draw.polygon(spade_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class BulletBallFall(GameObject):
	def __init__(self, x, y, degree, board, bounce = 1, vy = 0, vx = 0, grav = 0.1, fric = 1):
		loadAssets()
		super().__init__(x, y, degree, spade_spawn_image, True, 20)
		self.frame = 0
		self.grazed = False
		self.board = board
		self.vx = vx
		self.vy = vy
		self.grav = grav
		self.bounce = bounce
		self.fric = fric
		self.clamp = False

	def damage(self, soul):
		soul.hp -= 25

	def move(self):
		prevx = self.x
		prevy = self.y
		self.x += self.vx
		self.y += self.vy
		board = self.board
		xl = self.x - self.radius * 2
		xr = self.x + self.radius * 2
		yt = self.y + self.radius * 2
		yd = self.y - self.radius * 2
		bxl = board.x - board.size/2
		bxr = board.x + board.size/2
		byt = board.y + board.size/2
		byd = board.y - board.size/2
		if xl < bxl:
			self.x = bxl + self.radius*2
			self.vx *= -self.bounce
		if xr > bxr:
			self.x = bxr - self.radius*2
			self.vx *= -self.bounce
		if self.clamp:
			if yd < byd:
				self.y = byd + self.radius*2
				self.vy *= -self.bounce
			if yt > byt + 1000:
				self.y = byt - self.radius*2
				self.vy *= -self.bounce

		if xl >= bxl and xr <= bxr and yd >= byd and yt <= byt: self.clamp = True

		self.vy -= self.grav
		self.vx *= self.fric
		self.vy *= self.fric

		self.point_to(prevx, prevy)
		self.degree += 180

	def update(self):
		if self.frame == 0:
			self.morph_to(spade_image, 0.1)
		self.move()
		self.frame += 1

