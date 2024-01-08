import os
import random
import pygame
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("map", type=str, nargs="?", default="map.map")
args = parser.parse_args()
map_file = args.map

FPS = 60

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass

class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.original_image = tile_images[tile_type]
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)
        self.broken = False

    def update_image(self):
        if self.broken:
            self.image = tile_images['empty']
            self.broken = False

class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        self.direction = (1, 0)  # Initial direction: right

    def move(self, dx, dy):
        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy

        if 0 <= new_y < max_y and 0 <= new_x < max_x and level_map[new_y][new_x] != '#':
            camera.dx -= tile_width * (new_x - self.pos[0])
            camera.dy -= tile_height * (new_y - self.pos[1])
            self.pos = (new_x, new_y)
            for sprite in sprite_group:
                camera.apply(sprite)

            # Update direction based on movement
            self.direction = (dx, dy)

    def break_wall(self):
        x, y = self.pos
        for i in range(-1, 2):
            for j in range(-1, 2):
                target_x = x + i
                target_y = y + j
                if 0 <= target_y < max_y and 0 <= target_x < max_x and level_map[target_y][target_x] == '#':
                    level_map[target_y][target_x] = '.'  # Break the wall
                    for sprite in sprite_group:
                        if isinstance(sprite, Tile) and sprite.abs_pos == (tile_width * target_x, tile_height * target_y):
                            sprite.broken = True
                            sprite.update_image()

class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Hero movement", "", "", "Camera"]

    fon = pygame.transform.scale(load_image('fon.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
    return new_player, x, y

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                hero.move(0, -1)  # Move up
            elif event.key == pygame.K_s:
                hero.move(0, 1)  # Move down
            elif event.key == pygame.K_a:
                hero.move(-1, 0)  # Move left
            elif event.key == pygame.K_d:
                hero.move(1, 0)  # Move right
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            hero.break_wall()  # Break the wall

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 60

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

# Define screen here
screen_size = (1920, 1080)
screen = pygame.display.set_mode(screen_size)

all_sprites = pygame.sprite.Group()
hero_group = SpriteGroup()
sprite_group = SpriteGroup()
pygame.mouse.set_visible(0)

tile_width = tile_height = 50
player_image = load_image('mar.png')

clock = pygame.time.Clock()
start_screen()
camera = Camera()
level_map = load_level(map_file)
hero, max_x, max_y = generate_level(level_map)
camera.update(hero)

running = True
while running:
    handle_events()
    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    hero_group.draw(screen)

    # Get the cursor position
    cursor_pos = pygame.mouse.get_pos()

    # Draw an "X" over the cursor position
    pygame.draw.line(screen, pygame.Color("red"), (cursor_pos[0] - 10, cursor_pos[1] - 10), (cursor_pos[0] + 10, cursor_pos[1] + 10), 2)
    pygame.draw.line(screen, pygame.Color("red"), (cursor_pos[0] - 10, cursor_pos[1] + 10), (cursor_pos[0] + 10, cursor_pos[1] - 10), 2)

    # Display FPS in the window title
    pygame.display.set_caption(f"SuperUltraKonstatineAlexandrovichPlatformerProMaxInsaneUnimaginableOutOfThisWorldGame | v:0.4a | FPS: {int(clock.get_fps())}")

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
