import pygame

clock = pygame.time.Clock()

# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Tailwind")

# Загрузка иконки окна
icon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# Загрузка фона
bg = pygame.image.load("images/bg.jpg").convert_alpha()

# Загрузка изображений для анимации персонажа
walk_left = [
    pygame.image.load("images/player_left/1.png").convert_alpha(),
    pygame.image.load("images/player_left/2.png").convert_alpha(),
    pygame.image.load("images/player_left/3.png").convert_alpha(),
    pygame.image.load("images/player_left/4.png").convert_alpha(),
]
walk_right = [
    pygame.image.load("images/player_right/5.png").convert_alpha(),
    pygame.image.load("images/player_right/6.png").convert_alpha(),
    pygame.image.load("images/player_right/7.png").convert_alpha(),
    pygame.image.load("images/player_right/8.png").convert_alpha(),
]

# Отрисовка всех привидений на экране
def draw_ghosts():
    for ghost_rect in ghost_list_in_game:
        screen.blit(ghost, ghost_rect)

# Загрузка изображения призрака
ghost = pygame.image.load("images/ghost.png").convert_alpha()
ghost_list_in_game = []

# Переменные для анимации персонажа
player_anim_count = 0
bg_x = 0

# Настройки игрока
player_speed = 5
player_x = 150
player_y = 250

# Настройки прыжка
is_jump = False
jump_count = 7

# Звуковые настройки
bg_sound = pygame.mixer.Sound("sounds/bg.mp3")
# bg_sound.play()

# Таймер для появления привидений
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

# Настройки текстовых меток
label = pygame.font.Font('fonts/RobotoSlab-ExtraLight.ttf', 40)
lose_label = label.render("Вы проиграли !", False, (193, 196, 199))
restart_label = label.render("Играть снова", False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))

# Загрузка изображения пули
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []
bullets_left = 5

# Флаг состояния игры
gameplay = True

# Цикл игры
running = True
while running:
    # Отрисовка фона
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 640, 0))

    if gameplay:
        # Получение прямоугольника игрока для проверки столкновений
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

# Отрисовка привидений и их перемещение
        draw_ghosts()
        for (i, el) in enumerate(ghost_list_in_game):
            el.x -= 10

            if el.x < -10:
                ghost_list_in_game.pop(i)

            if player_rect.colliderect(el):
                gameplay = False

# Обработка клавиш управления игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -7:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 7

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 600:
            player_x += player_speed

# Анимация игрока
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

# Перемещение фона
        bg_x -= 2
        if bg_x == -640:
            bg_x = 0

# Обработка пуль
        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 660:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(642, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_w and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

    clock.tick(12)