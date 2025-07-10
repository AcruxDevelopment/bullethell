import os
import pygame

class Textures:
    def load(name):
        path = os.path.join("assets", name)
        return pygame.image.load(path).convert_alpha()

    def scaleToFit(image, target_width, target_height):
        original_width, original_height = image.get_size()
        scale_w = target_width / original_width
        scale_h = target_height / original_height
        scale = min(scale_w, scale_h)  # scale uniformly to fit inside box

        new_size = (int(original_width * scale), int(original_height * scale))
        return pygame.transform.smoothscale(image, new_size)