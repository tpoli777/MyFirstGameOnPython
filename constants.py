import os
import sys

import appdirs


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

APP_NAME = "SHMUP"
APP_AUTHOR = "EGG_INC"
VERSION = "1.0"
APP_DATA_PATH = appdirs.user_state_dir(APP_NAME, APP_AUTHOR, VERSION)
os.makedirs(APP_DATA_PATH, exist_ok=True)
print('APP_DATA_PATH', APP_DATA_PATH, os.path.exists(APP_DATA_PATH))

IMG_DIR = resource_path('img')
EXPLOSIONS_DIR = os.path.join(IMG_DIR, 'explosions')
METEORS_DIR = os.path.join(IMG_DIR, 'meteors')
POWERUPS_DIR = os.path.join(IMG_DIR, 'powerups')
snd_dir = resource_path('snd')
SCOREBOARD_PATH = os.path.join(APP_DATA_PATH, 'scores.csv')

FONT_PATH = resource_path('charybdis_font.ttf')
SMALL_TEXT_SIZE = 16
MAIN_TEXT_SIZE = 24
HEADER_TEXT_SIZE = 32
BIG_TEXT_SIZE = 64

METEOR_TYPES = ['grey', 'brown']
METEOR_CHANCES = [0.9, 0.1]
METEOR_HEALTH = {'grey': 1, 'brown': 2}
METEOR_MAX_SCORE = {'grey': 60, 'brown': 120}

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
INVISIBILITY_TIME = 3000
HIDE_TIME = 1000

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
