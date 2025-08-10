import pygame
from object import GameObject
from textures import Textures

board_image = None
def loadAssets():
    global board_image
    if not(board_image is None):
        return
    try:
        board_image = Textures.scaleToFit(Textures.load("board.webp"), 320, 320)
    except Exception as e:
        print("Failed to load texture, using fallback polygon:", e)
        soul_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(soul_image, (0, 255, 0), [(20,0),(40,40),(0,40)])

class Board(GameObject):
    def __init__(self, x, y):
        loadAssets()
        super().__init__(x, y, 0, board_image)
        self.size = 320
