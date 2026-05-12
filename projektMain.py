import pygame, sys, random

from projektSettings import *
from projektPlayer import Player
from projektEnemy import FallingBlock

# HLAVNÍ HERNÍ LOGIKA
# pohyb
# kolize
# skóre
# power-upy
# menu

pygame.init()

# high score načtení

try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

player = Player()

# objekty

block = FallingBlock(0)
life_block = FallingBlock(-200)
power_block = FallingBlock(-300)
purple_block = FallingBlock(-500)

# herní proměnné

score = 0
speed = 5
lives = MAX_LIVES

power_active = None
power_timer = 0

freeze_end = 0

state = "menu"

start_btn = pygame.Rect(100,150,200,50)
quit_btn  = pygame.Rect(100,220,200,50)

# RESET HRY

def reset_game():
    global score, speed, lives, power_active, freeze_end

    score = 0
    speed = 5
    lives = MAX_LIVES
    power_active = None
    freeze_end = 0

    player.__init__()
    block.reset(0)
    life_block.reset(-200)
    power_block.reset(-300)
    purple_block.reset(-500)

# HLAVNÍ CYKLUS

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                if start_btn.collidepoint(event.pos):
                    state = "game"
                    reset_game()

                if quit_btn.collidepoint(event.pos):
                    sys.exit()

    # MENU
    
    if state == "menu":
        screen.fill((0,0,0))

        pygame.draw.rect(screen,(0,150,0),start_btn)
        pygame.draw.rect(screen,(150,0,0),quit_btn)

        screen.blit(font.render("START", True,(255,255,255)), (150,160))
        screen.blit(font.render("QUIT", True,(255,255,255)), (165,230))
        screen.blit(font.render(f"HIGH SCORE: {highscore}", True,(255,255,0)), (70,300))

        pygame.display.flip()
        clock.tick(FPS)

    # HRA
    
    else:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        player.move(keys, current_time, power_active, speed)

        frozen = current_time < freeze_end

        current_speed = speed
        if power_active == "slow":
            current_speed *= 0.35

        if not frozen:
            block.update(current_speed)
            life_block.update(current_speed)
            power_block.update(current_speed)
            purple_block.update(current_speed)

        # ČERVENÝ BLOK
        
        if player.rect.colliderect(block.rect):
            score += 1
            speed += 0.1
            block.reset(-100)

        if block.rect.top > HEIGHT:
            lives -= 1
            block.reset(-100)

            if lives <= 0:
                if score > highscore:
                    highscore = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(highscore))
                state = "menu"

        # ŽIVOTY
        
        if player.rect.colliderect(life_block.rect):
            if lives < MAX_LIVES:
                lives += 1
            life_block.reset(-200)

        if life_block.rect.top > HEIGHT:
            life_block.reset(-200)

        # POWER-UP ŽLUTÝ BLOK

        if player.rect.colliderect(power_block.rect):
            if not power_active:
                power_active = random.choice(["slow", "shield", "speed"])
                power_timer = current_time
            power_block.reset(-300)

        if power_block.rect.top > HEIGHT:
            power_block.reset(-300)

        # konec power-upu

        if power_active and current_time - power_timer > 3000:
            power_active = None

        # POWER-UP FIALOVÝ BLOK
        
        if player.rect.colliderect(purple_block.rect):
            effect = random.choice(["freeze", "explosion", "tiny"])

            if effect == "freeze":
                freeze_end = current_time + 2000

            if effect == "explosion":
                block.reset(-100)
                life_block.reset(-200)
                power_block.reset(-300)

            if effect == "tiny":
                player.set_tiny(current_time)

            purple_block.reset(-500)

        if purple_block.rect.top > HEIGHT:
            purple_block.reset(-500)

        # VYKRESLENÍ NA OBRAZOVKU
        
        screen.fill((0,0,0))

        player.draw(screen)
        block.draw(screen,(255,0,0))
        life_block.draw(screen,(0,0,255))
        power_block.draw(screen,(255,255,0))
        purple_block.draw(screen,(160,0,255))

        screen.blit(font.render(f"Score: {score}", True,(255,255,255)), (10,10))
        screen.blit(font.render(f"Lives: {lives}", True,(255,255,255)), (WIDTH-140,10))
        screen.blit(font.render(f"HS: {highscore}", True,(255,255,0)), (10,40))

        pygame.display.flip()
        clock.tick(FPS)