from os import path

import pygame

from constants import *


# Загрузка всей игровой графики
background = pygame.image.load(path.join(IMG_DIR, "starfield.png")).convert()
background_rect = background.get_rect()
bullet_img = pygame.image.load(path.join(IMG_DIR, "laserRed16.png")).convert()

# Изображения метеоров
meteor_images = {}
meteor_list = [
    'meteor_big1.png', 'meteor_big2.png', 'meteor_big3.png',
    'meteor_big4.png', 'meteor_med1.png', 'meteor_med2.png',
    'meteor_small1.png', 'meteor_small2.png',
    'meteor_tiny1.png', 'meteor_tiny2.png'
]
for meteor_type in METEOR_TYPES:
    meteor_images[meteor_type] = []
    for img in meteor_list:
        meteor_images[meteor_type].append(pygame.image.load(path.join(METEORS_DIR, meteor_type, img)).convert())

# Изображения игрока
player_img_orig = pygame.image.load(path.join(IMG_DIR, "playerShip1_red.png")).convert()
player_img_orig.set_colorkey(BLACK)
PLAYER_SIZE = (50, 38)
player_img = pygame.transform.scale(player_img_orig, PLAYER_SIZE)
player_img.set_colorkey(BLACK)
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

BAR_LENGTH = 100
BAR_HEIGHT = 15
BAR_POSITION = (5, 5)
energy_img = pygame.image.load(path.join(IMG_DIR, "energy.png")).convert()
energy_img_size = energy_img.get_size()
energy_img_ratio = energy_img_size[0] / energy_img_size[1]
energy_img_width = BAR_HEIGHT*energy_img_ratio
energy_img = pygame.transform.scale(energy_img, (energy_img_width, BAR_HEIGHT))
energy_img.set_colorkey(BLACK)

# Изображение щита
SHIELD_SIDE = 10
SHIELD_OFFSET_Y = 10
SHIELD_SIZE = (PLAYER_SIZE[0]+SHIELD_SIDE*2, PLAYER_SIZE[1]+SHIELD_SIDE*2+SHIELD_OFFSET_Y)
shield_img_orig = pygame.image.load(path.join(IMG_DIR, "shield1.png")).convert()
shield_img = pygame.transform.scale(shield_img_orig, SHIELD_SIZE)
shield_img.set_colorkey(BLACK)

# Изображение игрока с щитом
player_with_shield_img = pygame.Surface(SHIELD_SIZE)
player_with_shield_img.blit(shield_img, (0, 0))
player_with_shield_img.blit(player_img, (SHIELD_SIDE, SHIELD_SIDE+SHIELD_OFFSET_Y))
player_with_shield_img.set_colorkey(BLACK)

# Изображения улучшений
powerup_images = {
    'health': pygame.image.load(path.join(POWERUPS_DIR, 'powerupYellow_bolt.png')).convert(),
    'gun': pygame.image.load(path.join(POWERUPS_DIR, 'powerupYellow_star.png')).convert(),
    'shield': pygame.image.load(path.join(POWERUPS_DIR, 'powerupYellow_shield.png')).convert(),
}

# Анимации взрывов
explosion_anim = {'lg': [], 'sm': [], 'player': []}
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(EXPLOSIONS_DIR, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(EXPLOSIONS_DIR, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
