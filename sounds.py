from os import path

import pygame

from constants import snd_dir


# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'Tenebre-Rosso-Sangue-(ULTRAKILL-Original-Game-Soundtrack)(MP3_320K).mp3'))
pygame.mixer.music.set_volume(0.8)
