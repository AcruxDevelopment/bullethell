import pygame
import random
import math
from object import GameObject
from textures import Textures
from bullet_heart_spinner import BulletHeartSpinner
from bullet_rain import BulletRain
from soul import Soul

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Create objects ---
soul = Soul(WIDTH//2, HEIGHT//2)
root = GameObject(WIDTH//2, HEIGHT//2, 0, None)
bullets = []

# --- Main Loop ---
running = True
frame = 0
deg = 0
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if frame % 8 == 0:
        x = math.cos(frame*0.005)*50
        #x = 0
        #bullets.append(BulletHeartSpinner(0, (HEIGHT // 2) + (random.randint(-2, 2) * 120), 0, random.randint(3, 4)))
        #bullets.append(BulletRain(random.randint(0,16) * 64, HEIGHT, 180, 0.05, random.randint(-10, 10)/10))
        #bullets.append(BulletRain(0, random.randint(0,8) * 64, 90, 0.05, random.randint(-10, 10)/10))
        bullets.append(BulletRain(WIDTH//2+x, HEIGHT//2, deg, 0.08))
        root.add_child(bullets[-1])
        bullets.append(BulletRain(WIDTH//2+x, HEIGHT//2, deg+127, 0.08))
        root.add_child(bullets[-1])
        bullets.append(BulletRain(WIDTH//2+x, HEIGHT//2, deg-127, 0.08))
        root.add_child(bullets[-1])
        root.x = x
        deg += 25


    # Remove bullets off screen
    bullets = [b for b in bullets if not b.is_off_screen(WIDTH, HEIGHT)]

    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)
        bullet.degree += 0.7

    if keys[pygame.K_LEFT]:
        soul.move_by(-soul.vel, 0)
    if keys[pygame.K_RIGHT]:
        soul.move_by(soul.vel, 0)
    if keys[pygame.K_UP]:
        soul.move_by(0, soul.vel)
    if keys[pygame.K_DOWN]:
        soul.move_by(0, -soul.vel)

    if keys[pygame.K_a]:
        soul.move_in_direction(soul.vel, 180)
    if keys[pygame.K_d]:
        soul.move_in_direction(soul.vel, 0)
    if keys[pygame.K_s]:
        soul.move_in_direction(soul.vel, -90)
    if keys[pygame.K_w]:
        soul.move_in_direction(soul.vel, 90)
    soul.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    frame += 4

pygame.quit()
