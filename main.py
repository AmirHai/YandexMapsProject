import os
import sys
import pygame
import requests


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
koordChanging = 1 * 2 ** (4 - map_params['z'])
btnPressed = [0] * 4
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
update_map()
text_focus = False
running = True

FPS = 60
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                map_params['z'] += 1 if map_params['z'] != 23 else 0
                koordChanging = 1 * 2 ** (4 - map_params['z'])
                update_map()
            if event.key == pygame.K_PAGEDOWN:
                map_params['z'] -= 1 if map_params['z'] != 0 else 0
                koordChanging = 1 * 2 ** (4 - map_params['z'])
                update_map()

            if event.unicode in symbols and text_focus:
                text += event.unicode
                text_r = font.render(start_text + text, True, 'Black')
                draw_texts()
            if event.key == pygame.K_BACKSPACE and text_focus:
                text = text[:-1]
                text_r = font.render(start_text + text, True, 'Black')
                draw_texts()

            if event.key == pygame.K_UP:
                btnPressed[0] = 1
            if event.key == pygame.K_DOWN:
                btnPressed[1] = 1
            if event.key == pygame.K_RIGHT:
                btnPressed[2] = 1
            if event.key == pygame.K_LEFT:
                btnPressed[3] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                btnPressed[0] = 0
            if event.key == pygame.K_DOWN:
                btnPressed[1] = 0
            if event.key == pygame.K_RIGHT:
                btnPressed[2] = 0
            if event.key == pygame.K_LEFT:
                btnPressed[3] = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_x - 5 <= event.pos[0] <= width - text_x - 5 and text_y - 5 \
                    <= event.pos[1] <= text_y + text_r.get_height():
                text_focus = True
            else:
                text_focus = False
            if search_text_x <= event.pos[0] <= search_text_x + search_text_r.get_width() and \
                    search_text_y <= event.pos[1] <= search_text_y + search_text_r.get_height():
                geo_params['geocode'] = text
                geo_response1 = requests.get(geo_server, params=geo_params).json()
                crds = geo_response1["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
                point = ','.join(crds.split())
                map_params['ll'] = point
                map_params['pt'] = f'{point},pm2ntm'
                map_params['z'] = 16
                update_map()

    changes = map_params['ll'].split(',')
    first = float(changes[0]) + koordChanging * (btnPressed[2] - btnPressed[3])
    if first >= 179:
        first = 178.999999
    elif first <= -179:
        first = -178.999999
    second = float(changes[1]) + koordChanging * (btnPressed[0] - btnPressed[1])
    if second >= 85:
        second = 84.999999
    elif second <= -85:
        second = -84.999999
    map_params['ll'] = f'{first},{second}'
    geo_params['ll'] = map_params['ll']
    update_map()
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
