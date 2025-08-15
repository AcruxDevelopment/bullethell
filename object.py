import pygame
import math
import time

class GameObject:
    def __init__(self, x, y, degree, image, visible=True, radius=5):
        self._x = x
        self._y = y
        self._degree = degree
        self.image = image
        self.original_image = image
        self.children = []
        self.visible = visible  # Control visibility
        self.lock_angle_to_world = False
	# Morph state
        self.morph_target_image = None
        self.morph_start_time = None
        self.morph_duration = 0
        self.morphing = False
        self.radius = radius

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

    def drawc(self, screen):
        flipped_y = screen.get_height() - self.y
        pygame.draw.circle(screen, (255, 0, 0), (self.x, flipped_y), self.radius, 2)

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
        if not self.visible:
            return

        current_image = self.original_image

        if self.morphing:
            elapsed = time.time() - self.morph_start_time
            progress = min(elapsed / self.morph_duration, 1.0)

            # Blend the two images
            current_image = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
            image1 = self.original_image.copy()
            image2 = self.morph_target_image.copy()

            image1.set_alpha(int(255 * (1.0 - progress)))
            image2.set_alpha(int(255 * progress))

            current_image.blit(image1, (0, 0))
            current_image.blit(image2, (0, 0))

            if progress >= 1.0:
                self.original_image = self.morph_target_image
                self.image = self.morph_target_image
                self.morphing = False

        rotated_image = pygame.transform.rotate(current_image, self.degree)
        screen_height = surface.get_height()
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

    def point_to(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        self.degree = angle_deg

    def morph_to(self, new_image, duration):
        self.morph_target_image = new_image.convert_alpha()
        self.morph_start_time = time.time()
        self.morph_duration = duration
        self.morphing = True

    def distance(self, other):
        # Center-to-center distance
        dx = other.x - self.x
        dy = other.y - self.y
        center_distance = math.sqrt(dx * dx + dy * dy)
        # Distance between edges (negative if overlapping)
        return center_distance - (self.radius + other.radius)

    def touches(self, other):
        # If edge-to-edge distance <= 0, they touch or overlap
        try:
            if self.nocollide or not self.nocollide:
                return False
        except:
            pass
        return self.distance(other) <= 0
