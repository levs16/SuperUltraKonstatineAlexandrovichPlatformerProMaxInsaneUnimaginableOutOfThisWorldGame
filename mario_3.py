import pygame
import os
import sys
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("map", type=str, nargs="?", default="map.map")
args = parser.parse_args()
map_file = args.map

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image

pygame.init()
screen_size = (1920, 1080)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50

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
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)

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
        for i in range(-3, 4):
            for j in range(-3, 4):
                target_x = x + i
                target_y = y + j
                if 0 <= target_y < max_y and 0 <= target_x < max_x and level_map[target_y][target_x] == '#':
                    level_map[target_y][target_x] = '.'  # Break the wall

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

sprite_group = SpriteGroup()
hero_group = SpriteGroup()
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
    pygame.draw.circle(screen, pygame.Color("red"), hero.rect.center, 3 * tile_width, 1)  # Visualize the radius
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()