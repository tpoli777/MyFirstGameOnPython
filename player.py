import pygame

from constants import *
from textures import player_img, player_with_shield_img, SHIELD_SIDE
from sounds import shoot_sound
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.invinsible = False
        self.invinsible_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.enable_invinsibility()

    def update(self, group_dict):
        current_time = pygame.time.get_ticks()
        # timeout for powerups
        if self.power >= 2 and current_time - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = current_time

        # показать, если скрыто
        if self.hidden and current_time - self.hide_timer > HIDE_TIME:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.enable_invinsibility()

        # Проверить неуязвимость
        if self.invinsible and current_time - self.invinsible_timer > INVISIBILITY_TIME:
            self.disable_invisibility()

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            if not self.hidden:
                self.shoot(group_dict)
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self, group_dict):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                group_dict['all'].add(bullet)
                group_dict['bullets'].add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                group_dict['all'].add(bullet1)
                group_dict['all'].add(bullet2)
                group_dict['bullets'].add(bullet1)
                group_dict['bullets'].add(bullet2)
                shoot_sound.play()

    def death(self):
        self.hide()
        self.lives -= 1
        self.shield = 10

    def enable_invinsibility(self):
        self.invinsible = True
        self.invinsible_timer = pygame.time.get_ticks()
        self.image = player_with_shield_img
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x - SHIELD_SIDE
        self.rect.y = y
        self.rect.bottom = HEIGHT

    def disable_invisibility(self):
        self.invinsible = False
        self.image = player_img
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x + SHIELD_SIDE
        self.rect.y = y
        self.rect.bottom = HEIGHT - 10

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
