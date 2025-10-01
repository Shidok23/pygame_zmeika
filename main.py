import pygame
import random

# 1. Инициализация Pygame
pygame.init()

# 2. Определение констант
# Размеры окна
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
# Размер одного блока змейки и еды
BLOCK_SIZE = 20

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

# Шрифты
FONT_STYLE = pygame.font.SysFont('bahnschrift', 25)

# 3. Создание игрового окна и настройка FPS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка на Pygame')
clock = pygame.time.Clock()

# --- Вспомогательные функции ---

def show_score(current_score):
    """Отображает текущий счет на экране."""
    score_text = FONT_STYLE.render("Счет: " + str(current_score), True, WHITE)
    screen.blit(score_text, [10, 10])

# --- Начальные состояния игровых объектов ---

# Положение и тело змейки
snake_pos = [100, 60]
snake_body = [[100, 60], [80, 60], [60, 60]]
snake_direction = 'RIGHT'

# Положение еды
food_pos = [random.randrange(0, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

# --- Переменные состояния игры ---
score = 0
game_over = False

# --- Главный игровой цикл ---
while not game_over:
    # 1. ОБРАБОТКА ВВОДА (СОБЫТИЙ)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # 2. ОБНОВЛЕНИЕ СОСТОЯНИЯ ИГРЫ (ИГРОВАЯ ЛОГИКА)

    # Движение головы змейки
    if snake_direction == 'UP':
        snake_pos[1] -= BLOCK_SIZE
    elif snake_direction == 'DOWN':
        snake_pos[1] += BLOCK_SIZE
    elif snake_direction == 'LEFT':
        snake_pos[0] -= BLOCK_SIZE
    elif snake_direction == 'RIGHT':
        snake_pos[0] += BLOCK_SIZE

    # Логика роста и движения тела
    snake_body.insert(0, list(snake_pos))

    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawned = False
        while not food_spawned:
            new_food_pos = [random.randrange(0, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                            random.randrange(0, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            if new_food_pos not in snake_body:
                food_pos = new_food_pos
                food_spawned = True
    else:
        snake_body.pop()

    # Проверка на столкновения (условия проигрыша)
    if (snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT):
        game_over = True

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over = True
            break

    # 3. ОТРИСОВКА (РЕНДЕРИНГ)
    screen.fill(BLACK)

    # Рисуем змейку
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Рисуем еду
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Отображаем счет
    show_score(score)

    # Обновляем экран
    pygame.display.flip()

    # Устанавливаем FPS
    clock.tick(15)

# Корректное завершение работы
pygame.quit()
quit()