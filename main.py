import pygame
import random
import sys

from constants import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

from textures import *
from sounds import *
from player import Player
from mob import Mob
from explosion import Explosion
from power_ups import PowerUp
from scoreboard import ScoreBoard


# Создаем игру и окно
pygame.display.set_icon(player_img_orig)
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
pygame.mixer.music.play(loops=-1)


def draw_text(surf, text, size, x=None, left=None, y=None, color=WHITE):
    assert x is not None or left is not None, 'Передай либо x, либо left'
    assert y is not None, 'Передай y'
    font = pygame.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if x is not None:
        text_rect.midtop = (x, y)
    else:
        text_rect.midleft = (left, y)
    surf.blit(text_surface, text_rect)


def newmobs(num_mobs=1):
    for _ in range(num_mobs):
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    img_rect = pygame.Rect(x, y, BAR_HEIGHT, BAR_HEIGHT)
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x+BAR_HEIGHT, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x+BAR_HEIGHT, y, fill, BAR_HEIGHT)
    surf.blit(energy_img, img_rect)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", BIG_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 4)
    draw_text(screen, "Arrow keys move", MAIN_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 2)
    draw_text(screen, "Arrow Up to fire", MAIN_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 2 + MAIN_TEXT_SIZE)
    draw_text(screen, "Esc to exit", MAIN_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 2 + MAIN_TEXT_SIZE*2)
    draw_text(screen, "Press any key to begin", MAIN_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT * 3 / 4)
    draw_text(screen, "Made using pygame, by Elisei & Vlad", SMALL_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT*0.9)
    pygame.display.flip()
    pygame.time.wait(2000)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def show_add_scoreboard(scoreboard, score):
    MAX_LENGTH = 15
    font = pygame.font.Font(None, HEADER_TEXT_SIZE)
    min_rect_width = WIDTH / 5
    input_box = pygame.Rect(WIDTH / 2 - min_rect_width / 2, HEIGHT / 4 + HEADER_TEXT_SIZE*2.5, min_rect_width, HEADER_TEXT_SIZE)
    is_done = False
    player_name = ""
    while not is_done:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    is_done = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        player_name = player_name[:MAX_LENGTH]

        # Render the current text.
        txt_surface = font.render(player_name, True, BLACK)
        # Resize the box if the text is too long.
        text_width = max(min_rect_width, txt_surface.get_width() + 10)
        input_box.left = WIDTH / 2 - text_width / 2
        input_box.w = text_width
        screen.blit(background, background_rect)
        draw_text(screen, f"Your score: {score}", HEADER_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 4)
        draw_text(screen, f"Enter name:", HEADER_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 4 + HEADER_TEXT_SIZE)
        pygame.draw.rect(screen, WHITE, input_box, 0, 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()
    scoreboard.add_score(player_name, score)

def show_scoreboard(scoreboard):
    SCOREBOARD_LEFT = WIDTH * 0.1
    screen.blit(background, background_rect)
    draw_text(screen,"SCOREBOARD", BIG_TEXT_SIZE, x=WIDTH / 2, y=HEIGHT / 4 - MAIN_TEXT_SIZE * 3)
    scoreboard_rect = pygame.Rect(SCOREBOARD_LEFT, HEIGHT / 4, WIDTH * 0.8, HEIGHT * 0.65)
    pygame.draw.rect(screen, WHITE, scoreboard_rect, 0, 10)
    cursor_height = HEIGHT / 4 - MAIN_TEXT_SIZE / 2
    for player_name, score in scoreboard.get_scores()[:15]:
        cursor_height += MAIN_TEXT_SIZE
        draw_text(
            screen, f'{player_name: <16} {score: >16}',
            MAIN_TEXT_SIZE, left=SCOREBOARD_LEFT + MAIN_TEXT_SIZE / 2, y=cursor_height, color=BLACK
        )
    pygame.display.flip()
    key_pressed = False
    while not key_pressed:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                key_pressed = True


# Цикл игры
start_game = True
game_over = False
running = True
score = 0
while running:
    if start_game:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        group_dict = {
            'all': all_sprites,
            'bullets': bullets,
            'mobs': mobs,
            'powerups': powerups
        }
        player = Player()
        all_sprites.add(player)
        newmobs(8)
        score = 0
        start_game = False
    if game_over:
        with ScoreBoard(SCOREBOARD_PATH) as scoreboard:
            show_add_scoreboard(scoreboard, score)
            show_scoreboard(scoreboard)
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        group_dict = {
            'all': all_sprites,
            'bullets': bullets,
            'mobs': mobs,
            'powerups': powerups
        }
        player = Player()
        all_sprites.add(player)
        newmobs(8)
        score = 0
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Обновление
    all_sprites.update(group_dict)

    # проверьте, не попала ли пуля в моб
    hitted_mobs = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit_mob in hitted_mobs:
        hit_mob.health -= 1
        if hit_mob.health <= 0:
            score += hit_mob.score
            random.choice(expl_sounds).play()
            mobs.remove(hit_mob)
            all_sprites.remove(hit_mob)
            expl = Explosion(hit_mob.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.95:
                power_up = PowerUp(hit_mob.rect.center)
                all_sprites.add(power_up)
                powerups.add(power_up)
            newmobs()

    #  Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        if not player.invinsible:
            player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmobs()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.death()

    # Если игрок умер, игра окончена
    if player.lives <= 0 and not death_explosion.alive():
        game_over = True


    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'health':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
        if hit.type == 'shield':
            player.enable_invinsibility()
        newmobs(2)

    # Удаляем мобов за экраном
    for mob in mobs:
        if mob.rect.top > HEIGHT + 10 or mob.rect.right < -5 or mob.rect.left > WIDTH + 5:
            all_sprites.remove(mob)
            mobs.remove(mob)
            newmobs()

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), SMALL_TEXT_SIZE, x=WIDTH / 2, y=10)
    draw_shield_bar(screen, BAR_POSITION[0], BAR_POSITION[1], player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives,
               player_mini_img)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
