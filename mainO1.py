import pygame
import random
import math
from gobject import GameObject
from textures import Textures
from bullet_rain import spade_image
from bullet_heart_spinner import BulletHeartSpinner
from bullet_rain import BulletRain
from soul import Soul

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Create objects ---
soul = Soul(WIDTH//2, HEIGHT//2)
root = GameObject(WIDTH//2, HEIGHT//2, 0, None)
bullets = []
goner = Textures.scaleToFit(Textures.load("spade2.png"), 40, 40)

# --- Main Loop ---
running = True
frame = 0
deg = 0
LIMIT = 3000
stage = False
spade_image = Textures.scaleToFit(Textures.load("spade2.png"), 40, 40)
pauseTime = 0
safeTime = 0
hitBullet = None

while running:
    clock.tick(60)
    if pauseTime > 0:
        pauseTime -= 1
        hitBullet = None
        continue

    safeTime -= 1
    if safeTime < 0: safeTime = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if frame % 8 == 0:
        if(frame < LIMIT - 250):
            x = math.cos(frame*0.003)*100
            y = -math.sin(frame*0.003)*100
            #x = 0
            #bullets.append(BulletHeartSpinner(0, (HEIGHT // 2) + (random.randint(-2, 2) * 120), 0, random.randint(3, 4)))
            #bullets.append(BulletRain(random.randint(0,16) * 64, HEIGHT, 180, 0.05, random.randint(-10, 10)/10))
            #bullets.append(BulletRain(0, random.randint(0,8) * 64, 90, 0.05, random.randint(-10, 10)/10))
            bullets.append(BulletRain(WIDTH//2+x, HEIGHT//2+y, deg, 0.08))
            root.add_child(bullets[-1])
            bullets.append(BulletRain(WIDTH//2+x, HEIGHT//2+y, deg+127, 0.08))
            root.add_child(bullets[-1])
            bullets.append(BulletRain(WIDTH//2+x, HEIGHT//2+y, deg-127, 0.08))
            root.add_child(bullets[-1])

            root.x = x
            root.y = y
            deg += 25
        elif (frame > LIMIT + 400) and not stage:
            stage = True
            for bullet in bullets:
                bullet.degree += 90
                #bullet.point_to(WIDTH//2, HEIGHT//2)
                #bullet.degree += 180
                bullet.fvel = 0
                bullet.facc = 0.1
        elif (frame > LIMIT + 400):
            for bullet in bullets:
                bullet.degree += 1
        elif (frame > LIMIT + 300):
            for bullet in bullets:
                bullet.start_morph(spade_image, 1)
        elif frame == LIMIT:
            for bullet in bullets:
                bullet.facc = 0
                bullet.fvel = 0


    # Remove bullets off screen
    if not stage:
        bullets = [b for b in bullets if not b.is_off_screen(WIDTH, HEIGHT)]

    screen.fill((30, 30, 30))
    for bullet in bullets:
        bullet.update()
        if(frame < LIMIT):
            bullet.degree += 1
        if bullet.touches(soul):
            if safeTime <= 0:
                pauseTime = 40
                safeTime = 100
                hitBullet = bullet

    for bullet in bullets:
        if hitBullet is None or hitBullet == bullet:
            bullet.draw(screen)
            if hitBullet == bullet:
                bullet.move_by(1000, 0)

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
    frame += 4

pygame.quit()
