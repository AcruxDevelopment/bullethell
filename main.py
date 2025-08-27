import pygame
import random
import math
import subprocess
from gobject import GameObject
from textures import Textures
from bullet_rain import spade_image
from bullet_ball import BulletBall
from bullet_ball_fall import BulletBallFall
from bullet_heart_spinner import BulletHeartSpinner
from bullet_rain import BulletRain
from soul import Soul
from board import Board
from afterimage import Afterimage
from p_test_a import PatternTestA
from p_test_b import PatternTestB
from p_tunnel import PatternTunnel
from p_round import PatternRound
from ruddin_a import RuddinA
from ruddin_b import RuddinB
from p_forth import PatternForth
from p_forth2 import PatternForth2
from p_ruddin import PatternHathy
from p_line import PatternLine
from p_ball import PatternBall
from p_ball_heavy import PatternBallHeavy
from p_reverse_fall import PatternReverseFall
from p_spin import PatternSpin
from p_castle import PatternCastle
from p_pendulum import PatternPendulum
from graze import Graze
from gooner import Gooner
from soul_shard import SoulShard
from soul_shard_fall import SoulShardFall
from soul_bullet import SoulBullet

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
soul_img_Size = 37 #37
soulr_image = Textures.scaleToFit(Textures.load("soul_r.webp"), soul_img_Size, soul_img_Size)
soulrh_image = Textures.scaleToFit(Textures.load("soul_rh.webp"), soul_img_Size, soul_img_Size)
souly_image = Textures.scaleToFit(Textures.load("soul_y.webp"), soul_img_Size, soul_img_Size)
soulyh_image = Textures.scaleToFit(Textures.load("soul_yh.webp"), soul_img_Size, soul_img_Size)

# --- Sounds ---
snd_hurt = pygame.mixer.Sound("sfx/hurt.wav")
snd_graze = pygame.mixer.Sound("sfx/graze.wav")
snd_break1 = pygame.mixer.Sound("sfx/break1.wav")
snd_break2 = pygame.mixer.Sound("sfx/break2.wav")
snd_small_shot = pygame.mixer.Sound("sfx/small_shot.wav")
snd_break_denied = pygame.mixer.Sound("sfx/break_denied.wav")
snd_break = pygame.mixer.Sound("sfx/break.wav")
snd_break.set_volume(0.5)

# --- Create objects ---
soul = Soul(WIDTH//2, HEIGHT//2, 4)
graze = Graze(soul)
board = Board(WIDTH//2, HEIGHT//2)
root = GameObject(WIDTH//2, HEIGHT//2, 0, None)
bullets = []
soulbullets = []
afterimages = []
gooner = None #Gooner((root.x, root.y))

def set_battle_time(value):
    global pattern_change_delay
    pattern_change_delay = value

# --- Patterns ---
def p_test_a(): return PatternTestA(soul, board, bullets, center)
def p_test_b(): return PatternTestB(soul, board, bullets, center, 17)
def p_ruddin(): return RuddinA(soul, board, bullets, center)
def p_ruddin_b(): return RuddinB(soul, board, bullets, center)
def p_tunnel(): return PatternTunnel(soul, board, bullets, center)
def p_round(): return PatternRound(soul, board, bullets, center)
def p_forth(): return PatternForth(soul, board, bullets, center)
def p_forth2(): return PatternForth2(soul, board, bullets, center, 35, 0.7)
def p_hathy(): return PatternHathy(soul, board, bullets, center)
def p_line(): return PatternLine(soul, board, bullets, center)
def p_ball(): return PatternBall(soul, board, bullets, center)
def p_ball_heavy(): return PatternBallHeavy(soul, board, bullets, center)
def p_reverse_fall(): return PatternReverseFall(soul, board, bullets, center)
def p_spin(): return PatternSpin(soul, board, bullets, center, set_battle_time)
def p_spin_fast(): return PatternSpin(soul, board, bullets, center, set_battle_time, 80, 9, 0.05, 9, 0.05, 350)
def p_spin_slow(): return PatternSpin(soul, board, bullets, center, set_battle_time, 50, 3, 0.01, 3, 0.01, 500)
def p_castle(): return PatternCastle(soul, board, bullets, center, set_battle_time)
def p_pendulum(): return PatternPendulum(soul, board, bullets, center, set_battle_time)
patterns = [p_tunnel, p_ruddin, p_round, p_test_a, p_forth, p_forth2, p_hathy, p_ruddin_b, p_line, p_test_b, p_ball, p_ball_heavy, p_reverse_fall,
            [p_spin, p_spin_fast, p_spin_slow], p_pendulum, p_castle]
#patterns = [p_test_b]
#patterns = [p_forth2]
#patterns = [p_ball_heavy, p_ball]
#patterns = [p_reverse_fall, p_ball]
#patterns = [p_reverse_fall]
#patterns = [p_spin]
#patterns = [p_spin, p_spin_fast, p_spin_slow]
patterns = [p_castle, p_spin, p_spin_fast, p_spin_slow, p_reverse_fall, p_pendulum] #JUSTICE
#patterns = [p_castle]
#patterns = [p_pendulum]
#patterns = [p_reverse_fall]
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
shoot_delay_max = 9
shoot_delay = 0
play_graze = False
dbgpause = False
slowm_interval = 2
slowm_frame = 0
draw_hb = False
soul_shards = []
shards = []
evade_mode_evaded = False
push = False
#--- Util ---
bar_width = 200
bar_height = 30
bar_x = 50
bar_y = 50

def draw_health_bar(surface, x, y, width, height):
    # Draw background (red)
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height))
    # Calculate green part width
    health_ratio = soul.hp / soul.max_hp
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * health_ratio, height))

# --- Main Loop ---
while running:
    bullets_delete = []
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    slowm_frame += 1
    if not dbgpause: slowm_frame = 0

    # Controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_3] and not keys_old[pygame.K_3]:
        dbgpause = not dbgpause
    keys_old[pygame.K_3] = keys[pygame.K_3]
    if dbgpause and (not keys[pygame.K_4] and not (keys[pygame.K_5] and not keys_old[pygame.K_5]) and not(keys[pygame.K_6] and slowm_frame%slowm_interval==0)):
        keys_old[pygame.K_5] = keys[pygame.K_5]
        continue
    keys_old[pygame.K_5] = keys[pygame.K_5]

    if keys[pygame.K_7]:
        soul.hp = soul.max_hp

    if hurt_delay > 0 and not die:
        soul_image = soulr_image if soul.m == 'r' else souly_image
        soulh_image = soulrh_image if soul.m == 'r' else soulyh_image
        if hurt_delay % 6 == 0 and not hurt_delay % 12 == 0:
            soul.morph_to(soul_image, 0.01)
        if hurt_delay % 12 == 0:
            soul.morph_to(soulh_image, 0.01)

    # Die
    die = soul.hp <= 0
    if die:

        for i in soul_shards:
            i.update()

        die_timer += 1
        if die_timer == 1:
            pygame.mixer.music.set_volume(0)
        if die_timer == 130:
            snd_break1.play()
            soul_shards = [SoulShard(soul.x, soul.y, True, soul.degree, soul.m), SoulShard(soul.x, soul.y, False, soul.degree, soul.m)]
            soul.morph_to(alpha_image, 0.01)

        if die_timer == 200: #150
            soul_shards = [
                SoulShardFall(soul.x, soul.y, 0, 7, 0),
                SoulShardFall(soul.x, soul.y, -3, 5, 1),
                SoulShardFall(soul.x, soul.y, -7, 2, 0),
                SoulShardFall(soul.x, soul.y, -5, -2, 1),
                SoulShardFall(soul.x, soul.y, 7, -3, 1),
                SoulShardFall(soul.x, soul.y, 3, -5, 0)
            ] if soul.m == 'r' else [
                SoulShardFall(soul.x, soul.y, 0, 7, 4),
                SoulShardFall(soul.x, soul.y, -3, 5, 5),
                SoulShardFall(soul.x, soul.y, -7, 2, 4),
                SoulShardFall(soul.x, soul.y, -5, -2, 5),
                SoulShardFall(soul.x, soul.y, 7, -3, 5),
                SoulShardFall(soul.x, soul.y, 3, -5, 4)
            ]
            
            snd_break2.play()

        if die_timer > 90:
            screen.fill((0,0,0))
            soul.draw(screen)
            for i in soul_shards:
                i.draw(screen)

            pygame.display.flip()
        if die_timer > 200:
            pass

        if die_timer > 300:
            #os.system("python main.py")
            subprocess.Popen(["python", "main.py"])
            running = False
        continue

    # LOGIC
    
    if False:
        board.x = WIDTH//2 + math.cos(frame * 0.1) * 300
        board.y = HEIGHT//2 + math.sin(frame * 0.1) * 300
        if frame % 2 == 0:
            afterimages.append(Afterimage.new_from(board, .5))
    if pattern_change_delay == 0:
        pattern = patterns[random.randint(0, len(patterns)-1)]()
        if isinstance(pattern, list):
            pattern = pattern[random.randint(0, len(pattern)-1)]()

        try:
            pattern.start()
        except: pass
        pattern_pause = 50
        force_soul = True
        pattern_change_delay = pattern_interval
        pattern.start()
        for i in bullets:
            bullets_delete.append(i)
        bullets[:] = [b for b in bullets if not b in bullets_delete]

    if False:
        if frame % 5 == 0:
            afterimages.append(Afterimage.new_from(gooner, .5))

    # Updates
    if gooner is not None:
        gooner.update()

    if pattern_pause <= 0:
        pattern.update()
    else:
        pattern_pause -= 1

        if force_soul:
            soul.x += (board.x - soul.x) * 0.25
            soul.y += (board.y - soul.y) * 0.25
            if soul.distance(board) <= 5:
                soul.x = board.x
                soul.y = board.y
                force_soul = False

    for i in soulbullets:
        i.update()

    evade_mode_evaded = False
    if evade:
        evade_mode_evaded = evade_mode_evaded or soul.evade(bullets, root, board)
    for i in bullets:
        for soulbullet in soulbullets:
            if i.touches(soulbullet):
                if not soulbullet.isBig:
                    bullets_delete.append(soulbullet)
                breakable = True
                try:
                    breakable = i.breakable
                except: pass
                if breakable:
                    bullets_delete.append(i)
                    snd_break.play()
                    soul.hp += 0.5
                    soul.hp = min(soul.hp, soul.max_hp)
                    for shard in [
                        SoulShardFall(i.x, i.y, 0, 7, 3),
                        SoulShardFall(i.x, i.y, -3, 5, 2),
                        SoulShardFall(i.x, i.y, -7, 2, 3),
                        SoulShardFall(i.x, i.y, -5, -2, 3),
                        SoulShardFall(i.x, i.y, 7, -3, 2),
                        SoulShardFall(i.x, i.y, 3, -5, 3)
                    ]:
                        shards.append(shard)
                else: snd_break_denied.play()
        if i.touches(soul):
            if hurt_delay <= 0:
                try:
                    i.damage(soul)
                    snd_hurt.play()
                    hurt_delay = hurt_delay_max
                except: pass
            if soul.hp > 0:
                bullets_delete.append(i)
        if i.touches(graze) and not i.grazed and hurt_delay <= 0:
            play_graze = True
            graze.graze()
            i.grazed = True
            soul.hp += 1
            soul.hp = min(soul.hp, soul.max_hp)
        if frame % 4 == 0 and afterimage:
            rad = math.radians(i.degree)
            vx = math.cos(rad) * 1
            vy = math.sin(rad) * 1
            afterimages.append(Afterimage.new_from(i, 0.2, vx, vy))
        i.update()
    for i in afterimages:
        i.update()
    for i in shards:
        i.update()

    if evade:
        evade_mode_evaded = evade_mode_evaded or soul.evade(bullets, root, board)
    # Cleanup
    bullets[:] = [b for b in bullets if (not (b.is_off_screen(WIDTH, HEIGHT) and b.off_screen_del_cond(b))) and (not b in bullets_delete)]
    soulbullets[:] = [b for b in soulbullets if (not (b.is_off_screen(WIDTH, HEIGHT)) and b not in bullets_delete)]
    afterimages[:] = [a for a in afterimages if not a.end()]
    shards[:] = [s for s in shards if not s.is_off_screen(WIDTH, HEIGHT)]

    # Die Guard
    if die:
        continue

    # Controls
    if keys[pygame.K_1] and not keys_old[pygame.K_1]:
        pattern = patterns[random.randint(0, len(patterns)-1)]()
        if isinstance(pattern, list):
            pattern = pattern[random.randint(0, len(pattern)-1)]()
        pattern_change_delay = pattern_interval
        pattern.start()
        bullets[:] = []
        force_soul = True
        for i in bullets:
            bullets_delete.append(i)
        bullets[:] = [b for b in bullets if not b in bullets_delete]
    keys_old[pygame.K_1] = keys[pygame.K_1]

    if keys[pygame.K_2] and not keys_old[pygame.K_2]:
        evade = not evade
    keys_old[pygame.K_2] = keys[pygame.K_2]

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

#    if soul.m == 'y':
#        soul.point_to(center[0], center[1])
#        soul.degree += -90

    if soul.m == 'y' and shoot_delay <= 0 and ((keys[pygame.K_RETURN] and not keys_old[pygame.K_RETURN]) or evade_mode_evaded):
        soulbullets.append(SoulBullet(soul.x, soul.y, soul.degree - 90))
        shoot_delay = shoot_delay_max
        snd_small_shot.play()
    keys_old[pygame.K_RETURN] = keys[pygame.K_RETURN]
    if shoot_delay > 0:
        shoot_delay -= 1

    if soul.x - soul.size <  board.x - (board.size/2):
        soul.x = board.x - (board.size/2) + soul.size
        if push: board.x -= soul.vel
    elif soul.x + soul.size >  board.x + (board.size/2):
        soul.x = board.x + (board.size/2) - soul.size
        if push: board.x += soul.vel
    if soul.y - soul.size <  board.y - (board.size/2):
        soul.y = board.y - (board.size/2) + soul.size
        if push: board.y -= soul.vel
    elif soul.y + soul.size >  board.y + (board.size/2):
        soul.y = board.y + (board.size/2) - soul.size
        if push: board.y += soul.vel

    graze.update()

    #Render
    screen.fill((0, 0, 0))
    if gooner is not None: gooner.draw(screen)
    board.draw(screen)
    for i in afterimages:
        i.draw(screen)
    for i in bullets:
        i.draw(screen)
        if draw_hb: i.drawc(screen)
    for i in shards:
        i.draw(screen)
        if draw_hb: i.drawc(screen)
    for i in soulbullets:
        i.draw(screen)
        if draw_hb: i.drawc(screen)
    soul.draw(screen)
    if draw_hb: soul.drawc(screen)
    graze.draw(screen)
    if draw_hb: graze.drawc(screen)
    draw_health_bar(screen, WIDTH/2-(300/2), HEIGHT - 150, 300 , 25)
    if type(pattern) == PatternCastle and False:
        surface = screen
        angle_deg = soul.degree
        length = 999
        start_pos = [soul.x, HEIGHT - soul.y]
        color = (255, 0, 0)
        width = 3
        angle_rad = math.radians(angle_deg + 90 + 180)
        end_pos = (
            start_pos[0] + length * math.cos(angle_rad),
            start_pos[1] - length * math.sin(angle_rad)  # minus because pygame y-axis goes down
        )
        pygame.draw.line(surface, color, start_pos, end_pos, width)

    pygame.display.flip()
    frame += 1
    hurt_delay -= 1
    hurt_delay = max(hurt_delay, 0)
    pattern_change_delay -= 1

    # Sound
    if play_graze:
        snd_graze.play()
        play_graze = False

pygame.quit()
