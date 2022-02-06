import os
import sys
import pygame
import requests


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, all_sprites, type):
        super().__init__(all_sprites)
        if type == 'scheme':
            self.image = load_image('scheme.png')
        elif type == 'gybrid':
            self.image = load_image('gybrid.png')
        elif type == 'spytnik':
            self.image = load_image('spytnik.png')
        self.image = pygame.transform.scale(self.image, (50, 25))
        self.rect = self.image.get_rect()

    def setCords(self, x, y):
        self.rect.topleft = x, y

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0] and \
                mouse[1] > self.rect.topleft[1] and \
                mouse[0] < self.rect.bottomright[0] and \
                mouse[1] < self.rect.bottomright[1]:
            return True
        return False


def update_map():
    screen.fill('Black')
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('Error')
        pygame.quit()
        os.remove(map_file)
        sys.exit()
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))

    all_sprites.draw(screen)
    pygame.display.flip()


map_api_server = 'http://static-maps.yandex.ru/1.x/'
map_params = {
    'll': input('Координаты точки: '),
    'l': 'map',
    'z': int(input('Масштаб: ')),
}
map_file = "map.png"
pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption('Maps API')

all_sprites = pygame.sprite.Group()
button_scheme = Button(all_sprites, 'scheme')
button_scheme.setCords(5, 5)
button_gybrid = Button(all_sprites, 'gybrid')
button_gybrid.setCords(5 + button_scheme.image.get_width() + 5, 5)
button_spytnik = Button(all_sprites, 'spytnik')
button_spytnik.setCords(5 + button_gybrid.image.get_width() +
                        5 + button_scheme.image.get_width() + 5, 5)

update_map()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                map_params['z'] += 1 if map_params['z'] != 24 else 0
                update_map()
            if event.key == pygame.K_PAGEDOWN:
                map_params['z'] -= 1 if map_params['z'] != 0 else 0
                update_map()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if button_scheme.pressed(mouse):  # Button pressed method is called
                map_params['l'] = 'map'
                update_map()
            elif button_gybrid.pressed(mouse):
                map_params['l'] = 'sat,skl'
                update_map()
            elif button_spytnik.pressed(mouse):
                map_params['l'] = 'sat'
                update_map()
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
# 37.519075,55.700381
# 'data',
