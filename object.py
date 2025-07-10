import pygame
import math

class GameObject:
    def __init__(self, x, y, degree, image, visible=True):
        self._x = x
        self._y = y
        self._degree = degree
        self.image = image
        self.original_image = image
        self.children = []
        self.visible = visible  # Control visibility
        self.lock_angle_to_world = False

    # --- Properties with child propagation ---
    @property
    def x(self): return self._x

    @x.setter
    def x(self, value):
        dx = value - self._x
        self._x = value
        for child in self.children:
            child.x += dx

    @property
    def y(self): return self._y

    @y.setter
    def y(self, value):
        dy = value - self._y
        self._y = value
        for child in self.children:
            child.y += dy

    @property
    def degree(self): return self._degree

    @degree.setter
    def degree(self, value):
        d_angle = value - self._degree
        self._degree = value % 360
        for child in self.children:
            child.rotate_around((self.x, self.y), d_angle, child.lock_angle_to_world)

    def add_child(self, child):
        self.children.append(child)

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_in_direction(self, distance, angle_deg):
        angle_rad = math.radians(angle_deg)
        dx = distance * math.cos(angle_rad)
        dy = distance * math.sin(angle_rad)
        self.move_by(dx, dy)


    def rotate_around(self, center, angle_deg, preserve_angle = False):
        rad = math.radians(angle_deg)
        dx = self.x - center[0]
        dy = self.y - center[1]

        new_dx = dx * math.cos(rad) - dy * math.sin(rad)
        new_dy = dx * math.sin(rad) + dy * math.cos(rad)

        self.x = center[0] + new_dx
        self.y = center[1] + new_dy
        if not preserve_angle:
            self.degree += angle_deg  # triggers children rotation

    def draw(self, surface):
        if self.visible:
            rotated_image = pygame.transform.rotate(self.original_image, self.degree)
            screen_height = surface.get_height()
            # Flip Y axis here:
            flipped_y = screen_height - self.y
            rect = rotated_image.get_rect(center=(self.x, flipped_y))
            surface.blit(rotated_image, rect)

        for child in self.children:
            child.draw(surface)

    def is_off_screen(self, screen_width, screen_height, margin=50):
        rotated_image = pygame.transform.rotate(self.original_image, -self.degree)
        rect = rotated_image.get_rect(center=(self.x, self.y))

        # Check if self is off-screen (with margin)
        off_left = rect.right < -margin
        off_right = rect.left > screen_width + margin
        off_top = rect.bottom < -margin
        off_bottom = rect.top > screen_height + margin

        self_off_screen = (off_left or off_right or off_top or off_bottom) or (not self.visible)

        # Check children recursively
        for child in self.children:
            if not child.is_off_screen(screen_width, screen_height, margin):
                # If any child is on-screen, parent is on-screen
                return False

        # If self off-screen/invisible AND all children off-screen → return True
        return self_off_screen