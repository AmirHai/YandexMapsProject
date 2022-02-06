# import os
# import sys
# import pygame
# import requests


# def load_image(name, colorkey=None):
#     fullname = os.path.join(name)
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     image = pygame.image.load(fullname)
#     if colorkey is not None:
#         image = image.convert()
#         if colorkey == -1:
#             colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey)
#     else:
#         image = image.convert_alpha()
#     return image


# class Button(pygame.sprite.Sprite):
#     def __init__(self, all_sprites, type):
#         super().__init__(all_sprites)
#         if type == 'scheme':
#             self.image = load_image('scheme.png')
#         elif type == 'gybrid':
#             self.image = load_image('gybrid.png')
#         elif type == 'spytnik':
#             self.image = load_image('spytnik.png')
#         self.image = pygame.transform.scale(self.image, (50, 25))
#         self.rect = self.image.get_rect()

#     def setCords(self, x, y):
#         self.rect.topleft = x, y

#     def pressed(self, mouse):
#         if mouse[0] > self.rect.topleft[0] and \
#                 mouse[1] > self.rect.topleft[1] and \
#                 mouse[0] < self.rect.bottomright[0] and \
#                 mouse[1] < self.rect.bottomright[1]:
#             return True
#         return False


# def update_map():
#     screen.fill('Black')
#     response = requests.get(map_api_server, params=map_params)
#     if not response:
#         print('Error')
#         pygame.quit()
#         os.remove(map_file)
#         sys.exit()
#     with open(map_file, "wb") as file:
#         file.write(response.content)
#     screen.blit(pygame.image.load(map_file), (0, 0))

#     all_sprites.draw(screen)
#     pygame.display.flip()


# map_api_server = 'http://static-maps.yandex.ru/1.x/'
# map_params = {
#     'll': input('Координаты точки: '),
#     'l': 'map',
#     'z': int(input('Масштаб: ')),
# }
# map_file = "map.png"
# pygame.init()
# screen = pygame.display.set_mode((600, 450))
# pygame.display.set_caption('Maps API')

# all_sprites = pygame.sprite.Group()
# button_scheme = Button(all_sprites, 'scheme')
# button_scheme.setCords(5, 5)
# button_gybrid = Button(all_sprites, 'gybrid')
# button_gybrid.setCords(5 + button_scheme.image.get_width() + 5, 5)
# button_spytnik = Button(all_sprites, 'spytnik')
# button_spytnik.setCords(5 + button_gybrid.image.get_width() +
#                         5 + button_scheme.image.get_width() + 5, 5)

# update_map()
# running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_PAGEUP:
#                 map_params['z'] += 1 if map_params['z'] != 24 else 0
#                 update_map()
#             if event.key == pygame.K_PAGEDOWN:
#                 map_params['z'] -= 1 if map_params['z'] != 0 else 0
#                 update_map()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse = pygame.mouse.get_pos()
#             if button_scheme.pressed(mouse):  # Button pressed method is called
#                 map_params['l'] = 'map'
#                 update_map()
#             elif button_gybrid.pressed(mouse):
#                 map_params['l'] = 'sat,skl'
#                 update_map()
#             elif button_spytnik.pressed(mouse):
#                 map_params['l'] = 'sat'
#                 update_map()
#     pygame.display.flip()

# pygame.quit()
# os.remove(map_file)
# 37.519075,55.700381
# 'data',
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
    screen.fill('White')
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('Error')
        pygame.quit()
        os.remove(map_file)
        sys.exit()
    with open(map_file, "wb") as file:
        file.write(response.content)
    draw_texts()
    all_sprites.draw(screen)
    pygame.display.flip()


def draw_texts():
    screen.fill('White')
    screen.blit(pygame.image.load(map_file), (0, 0))
    screen.blit(text_r, (text_x, text_y))
    screen.blit(search_text_r, (search_text_x, search_text_y))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.draw.rect(screen, 'Black', (text_x - 5, text_y - 5,
                                       width - text_x - 10, text_r.get_height() + 5), width=1)


symbols = 'абвгдеёжзийклмнопрстуфхцчшщьъэюяыАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЭЮЯЫ1234567890,.:; '
map_api_server = 'http://static-maps.yandex.ru/1.x/'
geo_server = 'http://geocode-maps.yandex.ru/1.x/'
map_params = {
    'll': input('Координаты точки: '),
    'l': 'map',
    'z': int(input('Масштаб: ')),
}
geo_params = {
    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
    'geocode': '',
    'll': map_params['ll'],
    'format': 'json'
}
map_file = 'map.png'
pygame.init()
size = width, height = 600, 550
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Maps API')
font = pygame.font.Font(None, 25)
start_text = 'Введите запрос: '
text = ''
text_r = font.render(start_text, True, 'Black')
text_x, text_y = 10, 465
search_text = 'Искать'
search_text_r = font.render(search_text, True, 'Black')
search_text_x, search_text_y = 520, 495

all_sprites = pygame.sprite.Group()
button_scheme = Button(all_sprites, 'scheme')
button_scheme.setCords(5, 5)
button_gybrid = Button(all_sprites, 'gybrid')
button_gybrid.setCords(5 + button_scheme.image.get_width() + 5, 5)
button_spytnik = Button(all_sprites, 'spytnik')
button_spytnik.setCords(5 + button_gybrid.image.get_width() +
                        5 + button_scheme.image.get_width() + 5, 5)

update_map()
text_focus = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                map_params['z'] += 1 if map_params['z'] != 23 else 0
                update_map()
            if event.key == pygame.K_PAGEDOWN:
                map_params['z'] -= 1 if map_params['z'] != 0 else 0
                update_map()
            if event.unicode in symbols and text_focus:
                text += event.unicode
                text_r = font.render(start_text + text, True, 'Black')
                draw_texts()
            if event.key == pygame.K_BACKSPACE and text_focus:
                text = text[:-1]
                text_r = font.render(start_text + text, True, 'Black')
                draw_texts()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if text_x - 5 <= event.pos[0] <= width - text_x - 5 and text_y - 5 \
                    <= event.pos[1] <= text_y + text_r.get_height():
                text_focus = True
            else:
                text_focus = False
            if search_text_x <= event.pos[0] <= search_text_x + search_text_r.get_width() and \
                    search_text_y <= event.pos[1] <= search_text_y + search_text_r.get_height():
                geo_params['geocode'] = text
                geo_response1 = requests.get(
                    geo_server, params=geo_params).json()
                adress = geo_response1["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
                print(adress)  # нужно вывести и добавить сброс

                crds = geo_response1["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
                point = ','.join(crds.split())
                map_params['ll'] = point
                map_params['pt'] = f'{point},pm2ntm'
                map_params['z'] = 16
                update_map()

            if button_scheme.pressed(mouse):
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
