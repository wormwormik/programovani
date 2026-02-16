import pygame, random, sys

# spuštění knihovny pygame
pygame.init()

# Nastavení velikosti okna

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # vytvoří herní okno
clock = pygame.time.Clock()  # hlídá FPS (rychlost hry)
font = pygame.font.SysFont("Arial", 30)  # nastaví font textu

# Vytvoření herních objektů
# hráč = zelený obdélník dole
player = pygame.Rect(180, 350, 40, 40)

# padající červený blok nahoře
block = pygame.Rect(random.randint(0,360), 0, 40, 40)

score, speed = 0, 5  # skóre hráče a rychlost pádu
state = "menu"       # aktuální stav hry (menu nebo game)

# Tlačítka v menu
# vytvoření obdélníků pro tlačítka
start_btn = pygame.Rect(100,150,200,50)
quit_btn  = pygame.Rect(100,220,200,50)

# Hlavní smyčka programu
while True:

    # zjistí aktuální pozici myši
    mouse_pos = pygame.mouse.get_pos()

    # zjistí, jestli je stisknuté levé tlačítko myši
    mouse_click = pygame.mouse.get_pressed()[0]

    # kontrola událostí (zavření okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # ukončí program

    # MENU
    if state == "menu":

        screen.fill((0,0,0))  # vymaže obrazovku (černé pozadí)

        # vykreslení tlačítek
        pygame.draw.rect(screen,(0,150,0),start_btn)
        pygame.draw.rect(screen,(150,0,0),quit_btn)

        # vykreslení textu na tlačítka
        screen.blit(font.render("START", True,(255,255,255)), (150,160))
        screen.blit(font.render("QUIT", True,(255,255,255)), (165,230))

        pygame.display.flip()  # aktualizace obrazovky

        # pokud klikneš na START → přepne se do hry
        if start_btn.collidepoint(mouse_pos) and mouse_click:
            state = "game"
            score = 0          # vynuluje skóre
            block.y = 0        # blok se vrátí nahoru

        # pokud klikneš na QUIT → hra se ukončí
        if quit_btn.collidepoint(mouse_pos) and mouse_click:
            sys.exit()

    # HRA
    else:

        keys = pygame.key.get_pressed()  # zjistí stisk kláves

        # pohyb hráče doleva (pokud není u kraje)
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5

        # pohyb hráče doprava (pokud není u kraje)
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 5

        # blok padá dolů
        block.y += speed

        # Smrt hráče
        # pokud blok spadne pod obrazovku
        if block.y > HEIGHT:
            state = "menu"  # návrat do menu

            # reset bloku na začátek
            block.y = 0
            block.x = random.randint(0,360)

        # Chycení bloku
        # pokud se hráč dotkne bloku
        if player.colliderect(block):
            score += 1  # zvýší skóre

            # blok se vrátí nahoru na náhodnou pozici
            block.y = 0
            block.x = random.randint(0,360)

        # Vykreslování hry
        screen.fill((0,0,0))  # vymazání obrazovky

        pygame.draw.rect(screen,(0,255,0),player)  # hráč (zelený)
        pygame.draw.rect(screen,(255,0,0),block)   # blok (červený)

        pygame.display.set_caption(f"Score: {score}")  # zobrazí skóre nahoře

        pygame.display.flip()  # aktualizace obrazu
        clock.tick(30)  # hra běží na 30 FPS
