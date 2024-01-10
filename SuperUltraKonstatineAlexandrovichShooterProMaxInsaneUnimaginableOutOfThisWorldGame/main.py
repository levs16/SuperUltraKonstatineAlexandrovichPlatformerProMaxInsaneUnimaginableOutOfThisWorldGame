import pygame

# Window settings
FPS = 60
WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (25, 255, 0)
GRAY = (128, 128, 128)
VIOLET = (126, 8, 236)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
CYAN = (0, 255, 255)
LIGHTGRAY = (211, 211, 211)
NAVY = (0, 0, 128)
MEDIUMSLATEBLUE = (123, 104, 238)
SKYBLUE = (0, 191, 255)
HONEYDEW = (240, 255, 240)
SNOW = (255, 250, 250)
IVORY = (255, 255, 240)
YELLOWGREEN = (154, 205, 50)
DARKGREEN = (0, 100, 0)
INDIGO = (75, 0, 130)

# Text
def text(screen, text, size, color, textFont, x, y):
    fontName = pygame.font.match_font(textFont)
    font = pygame.font.Font(fontName, size)
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    screen.blit(textSurf, textRect)

# Player1 (with a smiley-face)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1Img, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)

    def update(self):
        self.speedx = 5
        self.speedy = 5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            self.speedx = -5
        if keys[pygame.K_l]:
            self.speedx = 5
        if keys[pygame.K_i]:
            self.speedy = -5
        if keys[pygame.K_k]:
            self.speedy = 5
        if keys[pygame.K_SEMICOLON]:
            self.speedx += 5
            self.speedy += 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 305:
            self.rect.left = 305

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        pygame.mixer.music.load('res/Shotgun.mp3')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=0)

        bullet = Player1Bullet(self.rect.centerx, self.rect.centery)
        sprites.add(bullet)
        bulletsPlayer1.add(bullet)

# Player2(a frowney-faced)
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player2Img, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (600, 0)

    def update(self):
        self.speedx = -5
        self.speedy = 5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -5
        if keys[pygame.K_d]:
            self.speedx = 5
        if keys[pygame.K_w]:
            self.speedy = -5
        if keys[pygame.K_s]:
            self.speedy = 5
        if keys[pygame.K_LSHIFT]:
            self.speedx -= 5
            self.speedy += 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x < 0 and self.rect.y > HEIGHT:
            self.rect.center = (600, 0)

        if self.rect.right > 295:
            self.rect.right = 295

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        pygame.mixer.music.load('res/Shotgun.mp3')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=0)

        bullet = Player2Bullet(self.rect.centerx, self.rect.centery)
        sprites.add(bullet)
        bulletsPlayer2.add(bullet)

# Player1's bullet
class Player1Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(p1b, (10, 5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = -15

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x < 0:
            self.kill()

# Player2's bullet
class Player2Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(p2b, (10, 5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 15

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x > WIDTH:
            self.kill()

# Window design
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('SuperUltraKonstatineAlexandrovichShooterProMaxInsaneUnimaginableOutOfThisWorldGame')
pygame.display.set_icon(pygame.image.load('res/icon.svg'))

# Textures
background = pygame.image.load('res/bg.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
backgroundImgState0 = pygame.image.load('res/game0.jpeg').convert()
backgroundImgState0 = pygame.transform.scale(backgroundImgState0, (WIDTH, HEIGHT))
backgroundImgState0_rect = backgroundImgState0.get_rect()
BackgroundImageState4 = pygame.image.load('res/menuESC.jpeg').convert()
BackgroundImageState4 = pygame.transform.scale(BackgroundImageState4, (WIDTH, HEIGHT))
BackgroundImageState4_rect = BackgroundImageState4.get_rect()
backgroundImgGameOver = pygame.image.load('res/endbg.jpeg').convert()
backgroundImgGameOver = pygame.transform.scale(backgroundImgGameOver, (WIDTH, HEIGHT))
backgroundImgGameOver_rect = backgroundImgGameOver.get_rect()
mainbg = pygame.image.load('res/mainbg.jpeg').convert()
mainbg = pygame.transform.scale(mainbg, (WIDTH, HEIGHT))
mainbg_rect = mainbg.get_rect()
player1Img = pygame.image.load('res/p1.png').convert()
player2Img = pygame.image.load('res/p2.png').convert()
p1b = pygame.image.load('res/p1b.jpeg')
p2b = pygame.image.load('res/p2b.jpeg')

# objects
player = Player()
sprites = pygame.sprite.Group()
sprites.add(player)
bulletsPlayer1 = pygame.sprite.Group()
bulletsPlayer2 = pygame.sprite.Group()
player2 = Player2()
enemies = pygame.sprite.Group()
enemies.add(player2)
s1 = 0
s2 = 0

# main cycle
game = 0
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and (game != 0 or game != 3 or game != 2 or game != 4):
                player.shoot()
            if event.key == pygame.K_e  and (game != 0 or game != 3 or game != 2 or game != 4):
                player2.shoot()
            if event.key == pygame.K_ESCAPE:
                if game != 0:
                    game = 4
            if event.key == pygame.K_n:
                game = 1
            if event.key == pygame.K_q:
                if game != 1:
                    run = False
            if event.key == pygame.K_c:
                if game != 0:
                    game = 1
            if event.key == pygame.K_m:
                if game != 1:
                    game = 0

    # bullets and their hits
    bulletHitP2 = pygame.sprite.spritecollide(player2, bulletsPlayer1, True)
    bulletHitP1 = pygame.sprite.spritecollide(player, bulletsPlayer2, True)

    if bulletHitP2:
        s1 += 1
        pygame.mixer.music.load('res/bruh.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    if bulletHitP1:
        s2 += 1
        pygame.mixer.music.load('res/bruh.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()


    # Bullet Hit Counter
    if s1 == 10:
        game = 3
    if s2 == 10:
        game = 2

    # Rendering
    if game == 0:
        window.blit(mainbg, mainbg_rect)
        text(window, 'Start <N>', 40, GRAY, 'Arial', WIDTH // 2, HEIGHT // 2)
        text(window, 'Quit <Q>', 40, GRAY, 'Arial', WIDTH // 2, HEIGHT // 2 + 50)
        text(window, 'Version 1.0', 20, LIGHTGRAY, 'Arial', 540, 580)
        text(window, 'Made by: Lev(levs16), Semyon(Sgk4, Yes)', 20, LIGHTGRAY, 'Arial', 185, 580)
        pygame.display.update()

    if game == 1:
        window.blit(background, background_rect)
        pygame.draw.rect(window, BLACK, (295, 0, 10, 600))
        sprites.draw(window)
        sprites.update()
        enemies.draw(window)
        enemies.update()
        text(window, str(s1), 30, SKYBLUE, 'Arial', 450, 100)
        text(window, str(s2), 30, SKYBLUE, 'Arial', 150, 100)
        pygame.display.update()
    if game == 3:
        window.blit(backgroundImgGameOver, backgroundImgGameOver_rect)
        text(window, 'Game Over!', 72, RED, 'Arial', WIDTH // 2, HEIGHT // 2)
        text(window, 'Player 1 is dead!', 40, RED, 'Arial', WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.update()
    if game == 2:
        window.blit(backgroundImgGameOver, backgroundImgGameOver_rect)
        text(window, 'Game Over!', 72, RED, 'Arial', WIDTH // 2, HEIGHT // 2)
        text(window, 'Player 2 is dead!', 40, RED, 'Arial', WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.update()
    if game == 4:
        window.blit(BackgroundImageState4, BackgroundImageState4_rect)
        text(window, 'Pause', 80, VIOLET, 'Arial', WIDTH // 2, HEIGHT // 2 - 100)
        text(window, 'Continue <C>', 40, INDIGO, 'Arial', WIDTH // 2, HEIGHT // 2)
        text(window, 'Main Menu <M>', 40, INDIGO, 'Arial', WIDTH // 2, HEIGHT // 2 + 50)
        text(window, 'Quit <Q>', 40, INDIGO, 'Arial', WIDTH // 2, HEIGHT // 2 + 100)
        pygame.display.update()

pygame.quit()
# V1.0
