import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
from os import listdir
pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLUE = 0, 0, 255

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

# ball = pygame.Surface((20, 20))
# ball.fill(WHITE)
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs[0]
player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(),(150, 30)) # Малюємо гусака
player_rect = player.get_rect()
player_speed = 5

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(),(100, 20))
    #enemy = pygame.Surface((20, 20)) # розмір обекта
    #enemy.fill(GREEN)
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size()) #визначаемо його положення
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (100, 50))
    # bonus = pygame.Surface((20, 20)) # розмір обекта
    # bonus.fill(BLUE)
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size()) #визначаемо його положення
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load("background.png").convert(), screen)
# Щоб роозмістити картинку в розмір нашого екрану, модуль transform.scale
bgX = 0 # щоб картинка рухалась, визначаємо координати
bgX2 = bg.get_width() # щоб картинка рухалась, визначаємо координати
bg_speed = 3 # щоб картинка рухалась, визначаємо координати

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0
scores = 0

enemies = []
bonusys = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working == False
            exit()

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonusys.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    #main_surface.fill(BLACK)

    # main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    # Щоб картинка оновлювалась
    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0)) # Малюємо на екрані рухому картинку
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit (player, player_rect)

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0)) # Малюємо на екрані очки


    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonusys:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonusys.pop(bonusys.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonusys.pop(bonusys.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)


    pygame.display.flip()
