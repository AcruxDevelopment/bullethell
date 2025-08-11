import pygame
import random
import math
from object import GameObject
from textures import Textures
from bullet_rain import spade_image
from bullet_heart_spinner import BulletHeartSpinner
from bullet_rain import BulletRain
from soul import Soul
from board import Board
from afterimage import Afterimage
from p_test_a import PatternTestA
from p_tunnel import PatternTunnel
from p_round import PatternRound
from ruddin_a import RuddinA
from ruddin_b import RuddinB
from p_forth import PatternForth
from p_forth2 import PatternForth2
from p_ruddin import PatternHathy
from p_line import PatternLine
from graze import Graze

# --- Setup ---
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music/rude_buster.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 800
center = (WIDTH//2, HEIGHT//2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
alpha_image = Textures.load("alpha.webp")
soul_image = Textures.scaleToFit(Textures.load("soul.webp"), 37, 37)
soulh_image = Textures.scaleToFit(Textures.load("soulh.webp"), 37, 37)

# --- Sounds ---
snd_hurt = pygame.mixer.Sound("sfx/hurt.wav")
snd_graze = pygame.mixer.Sound("sfx/graze.wav")
snd_break1 = pygame.mixer.Sound("sfx/break1.wav")
snd_break2 = pygame.mixer.Sound("sfx/break2.wav")

# --- Create objects ---
soul = Soul(WIDTH//2, HEIGHT//2, 4)
graze = Graze(soul)
board = Board(WIDTH//2, HEIGHT//2)
root = GameObject(WIDTH//2, HEIGHT//2, 0, None)
bullets = []
afterimages = []

# --- Patterns ---
p_test_a = PatternTestA(soul, board, bullets, center)
p_ruddin = RuddinA(soul, board, bullets, center)
p_ruddin_b = RuddinB(soul, board, bullets, center)
p_tunnel = PatternTunnel(soul, board, bullets, center)
p_round = PatternRound(soul, board, bullets, center)
p_forth = PatternForth(soul, board, bullets, center)
p_forth2 = PatternForth2(soul, board, bullets, center, 35, 0.4)
p_hathy = PatternHathy(soul, board, bullets, center)
p_line = PatternLine(soul, board, bullets, center)
patterns = [p_tunnel, p_ruddin, p_round, p_test_a, p_forth, p_forth2, p_hathy, p_ruddin_b]
#patterns = [p_line]
pattern = None
pattern_interval = 500
pattern_change_delay = 0
pattern_pause = 0
pattern_pause_move_tres = 20
force_soul = False

# --- Main Loop Vars ---
running = True
evade = False
afterimage = False
frame = 0
keys_old = {}
die = False
die_timer = 0
hurt_delay_max = 100
hurt_delay = 0

#--- Util ---

# --- Main Loop ---
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if hurt_delay > 0 and not die:
        if hurt_delay % 6 == 0 and not hurt_delay % 12 == 0:
            soul.morph_to(soul_image, 0.01)
        if hurt_delay % 12 == 0:
            soul.morph_to(soulh_image, 0.01)

    # Die
    die = soul.hp <= 0
    if die:
        die_timer += 1
        if die_timer == 1:
            pygame.mixer.music.set_volume(0)
        if die_timer == 90:
            snd_break1.play()
        if die_timer == 150:
            soul.morph_to(alpha_image, 0.01)
            snd_break2.play()

        if die_timer > 90:
            screen.fill((0,0,0))
            soul.draw(screen)
            pygame.display.flip()
        if die_timer > 150:
            pass

        if die_timer > 250:
            running = False
        continue

    # Logic
    if False:
        board.x = WIDTH//2 + math.cos(frame * 0.01) * 100
        board.y = HEIGHT//2 + math.sin(frame * 0.01) * 100
        if frame % 10 == 0:
            afterimages.append(Afterimage.new_from(board, .5))
    if pattern_change_delay == 0:
        pattern = patterns[random.randint(0, len(patterns)-1)]
        pattern_pause = 50
        force_soul = True
        pattern_change_delay = pattern_interval
        pattern.start()

    # Updates
    if pattern_pause <= 0:
        pattern.update()
    else:
        for i in bullets:
            i.x = 1000
        pattern_pause -= 1

        if force_soul:
            soul.x += (board.x - soul.x) * 0.25
            soul.y += (board.y - soul.y) * 0.25
            if soul.distance(board) <= 5:
                soul.x = board.x
                soul.y = board.y
                force_soul = False

    for i in bullets:
        if i.touches(soul):
            if hurt_delay <= 0:
                try:
                    i.damage(soul)
                    snd_hurt.play()
                    hurt_delay = hurt_delay_max
                except: pass
            if soul.hp > 0:
                i.move_by(0, 10000)
        if i.touches(graze) and not i.grazed and hurt_delay <= 0:
            snd_graze.play()
            graze.graze()
            i.grazed = True
        if frame % 4 == 0 and afterimage:
            rad = math.radians(i.degree)
            vx = math.cos(rad) * 1
            vy = math.sin(rad) * 1
            afterimages.append(Afterimage.new_from(i, 0.2, vx, vy))
        i.update()
    for i in afterimages:
        i.update()

    # Die Guard
    if die:
        continue

    # Cleanup
    bullets[:] = [b for b in bullets if not b.is_off_screen(WIDTH, HEIGHT)]
    afterimages[:] = [a for a in afterimages if not a.end()]

    # Controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_1] and not keys_old[pygame.K_1]:
        pattern = patterns[random.randint(0, len(patterns)-1)]
        pattern_change_delay = pattern_interval
        pattern.start()
        bullets[:] = []
        force_soul = True
    keys_old[pygame.K_1] = keys[pygame.K_1]

    soul.u, soul.l, soul.d, soul.r = False, False, False, False
    if keys[pygame.K_LEFT] and pattern_pause <= pattern_pause_move_tres:
        soul.move_by(-soul.vel, 0)
        soul.l = True
    if keys[pygame.K_RIGHT] and pattern_pause <= pattern_pause_move_tres:
        soul.move_by(soul.vel, 0)
        soul.r = True
    if keys[pygame.K_UP] and pattern_pause <= pattern_pause_move_tres:
        soul.move_by(0, soul.vel)
        soul.u = True
    if keys[pygame.K_DOWN] and pattern_pause <= pattern_pause_move_tres:
        soul.move_by(0, -soul.vel)
        soul.d = True

    if keys[pygame.K_a] and pattern_pause <= pattern_pause_move_tres:
        soul.move_in_direction(soul.vel, 180)
        soul.l = True
    if keys[pygame.K_d] and pattern_pause <= pattern_pause_move_tres:
        soul.move_in_direction(soul.vel, 0)
        soul.r = True
    if keys[pygame.K_s] and pattern_pause <= pattern_pause_move_tres:
        soul.move_in_direction(soul.vel, -90)
        soul.d = True
    if keys[pygame.K_w] and pattern_pause <= pattern_pause_move_tres:
        soul.move_in_direction(soul.vel, 90)
        soul.u = True
    if evade:
        soul.evade(bullets, root, board)

    if soul.x - soul.size <  board.x - (board.size/2):
        soul.x = board.x - (board.size/2) + soul.size
    elif soul.x + soul.size >  board.x + (board.size/2):
        soul.x = board.x + (board.size/2) - soul.size
    if soul.y - soul.size <  board.y - (board.size/2):
        soul.y = board.y - (board.size/2) + soul.size
    elif soul.y + soul.size >  board.y + (board.size/2):
        soul.y = board.y + (board.size/2) - soul.size

    graze.update()

    #Render
    screen.fill((0, 0, 0))
    for i in afterimages:
        i.draw(screen)
    board.draw(screen)
    for i in bullets:
        i.draw(screen)
    soul.draw(screen)
    graze.draw(screen)

    pygame.display.flip()
    frame += 1
    hurt_delay -= 1
    hurt_delay = max(hurt_delay, 0)
    pattern_change_delay -= 1

pygame.quit()
