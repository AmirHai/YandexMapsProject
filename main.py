import os
import sys
import pygame
import requests


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
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
