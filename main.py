import pygame
import random
import json
import os

from save_system import load_best_score, save_best_score # type: ignore


pygame.init()

CELL = 20

# get real screen size and make window size divisible by CELL
info = pygame.display.Info()
WIDTH = (info.current_w // CELL) * CELL
HEIGHT = (info.current_h // CELL) * CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# colors
BG = (14, 16, 22)
GRID = (26, 30, 42)
SNAKE = (90, 230, 130)
HEAD = (150, 255, 190)
FOOD = (255, 90, 100)
TEXT = (235, 235, 245)
SUBTEXT = (180, 185, 205)

font = pygame.font.SysFont(None, 42)
big_font = pygame.font.SysFont(None, 86)

# file used to save the best score
SAVE_FILE = "save.json"

def load_best_score():
    # return 0 if there is no save file
    if not os.path.exists(SAVE_FILE):
        return 0
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return int(data.get("best_score", 0))
    except (json.JSONDecodeError, OSError, ValueError):
        # if file is corrupted or unreadable, return 0
        return 0

def save_best_score(best_score):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"best_score": int(best_score)}, f, ensure_ascii=False, indent=2)
    except OSError:
        # ignore save errors
        pass

def new_food(snake_set):
    # generate food not on the snake
    while True:
        x = random.randint(0, (WIDTH // CELL) - 1) * CELL
        y = random.randint(0, (HEIGHT // CELL) - 1) * CELL
        if (x, y) not in snake_set:
            return x, y

def reset_game():
    # start snake in the center
    x = (WIDTH // 2) // CELL * CELL
    y = (HEIGHT // 2) // CELL * CELL
    snake = [(x, y), (x - CELL, y), (x - 2 * CELL, y)]
    snake_set = set(snake)  # set for fast collision checks
    prev_snake = snake.copy()

    dx, dy = CELL, 0
    next_dx, next_dy = dx, dy  # buffer direction for better controls

    grow = 0
    score = 0

    food_x, food_y = new_food(snake_set)
    game_over = False
    move_delay = 200
    last_step_time = pygame.time.get_ticks()

    return snake, snake_set, prev_snake, dx, dy, next_dx, next_dy, grow, score, food_x, food_y, game_over, move_delay, last_step_time

snake, snake_set, prev_snake, dx, dy, next_dx, next_dy, grow, score, food_x, food_y, game_over, move_delay, last_step_time = reset_game()
best_score = load_best_score()
paused = False
running = True

while running:
    # handle input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r:
                snake, snake_set, prev_snake, dx, dy, next_dx, next_dy, grow, score, food_x, food_y, game_over, move_delay, last_step_time = reset_game()
                paused = False

            # handle WASD control (read current key states)
        keys = pygame.key.get_pressed()

        if not game_over and not paused:
    # A = move left, but not directly opposite to current x
         if keys[pygame.K_a] and dx != CELL:
           next_dx, next_dy = -CELL, 0
      # D = move right
         elif keys[pygame.K_d] and dx != -CELL:
           next_dx, next_dy = CELL, 0
    # W = move up
         elif keys[pygame.K_w] and dy != CELL:
           next_dx, next_dy = 0, -CELL
    # S = move down
         elif keys[pygame.K_s] and dy != -CELL:
           next_dx, next_dy = 0, CELL


    # movement logic
    now = pygame.time.get_ticks()
    if not game_over and not paused and now - last_step_time >= move_delay:
        prev_snake = snake.copy()
        last_step_time = now

        # apply buffered direction
        dx, dy = next_dx, next_dy

        hx, hy = snake[0]
        new_head = (hx + dx, hy + dy)

        # check wall collision
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over = True
        else:
            # check self collision with set
            tail = snake[-1]
            if new_head in snake_set and not (grow == 0 and new_head == tail):
                game_over = True

        if game_over:
            best_score = max(best_score, score)
            save_best_score(best_score)
        else:
            snake.insert(0, new_head)
            snake_set.add(new_head)

            if new_head == (food_x, food_y):
                food_x, food_y = new_food(snake_set)
                grow += 1
                score += 1
                move_delay = max(60, 200 - score * 5)

            if grow > 0:
                grow -= 1
            else:
                tail = snake.pop()
                snake_set.remove(tail)

    # interpolation for smooth movement
    if paused:
        progress = 1
    else:
        progress = (pygame.time.get_ticks() - last_step_time) / move_delay
        progress = max(0, min(1, progress))

    # drawing
    screen.fill(BG)

    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

    pygame.draw.rect(screen, FOOD, (food_x, food_y, CELL, CELL), border_radius=7)

    for i in range(len(snake)):
        x2, y2 = snake[i]
        x1, y1 = prev_snake[i] if i < len(prev_snake) else (x2, y2)

        x = x1 + (x2 - x1) * progress
        y = y1 + (y2 - y1) * progress

        color = HEAD if i == 0 else SNAKE
        pygame.draw.rect(screen, color, (x, y, CELL, CELL), border_radius=7)

    # render text so it always fits inside the window
    score_surf = font.render(f"Score: {score}", True, TEXT)
    best_surf = font.render(f"Best: {best_score}", True, TEXT)

    # draw score text with right margin
    screen.blit(score_surf, (WIDTH - score_surf.get_width() - 20, 20))
    screen.blit(best_surf, (WIDTH - best_surf.get_width() - 20, 60))

    if paused and not game_over:
        screen.blit(big_font.render("PAUSED", True, TEXT),
                    (WIDTH // 2 - 150, HEIGHT // 2 - 80))

    if game_over:
        screen.blit(big_font.render("GAME OVER", True, TEXT),
                    (WIDTH // 2 - 260, HEIGHT // 2 - 90))
        screen.blit(font.render("R - restart   ESC - exit", True, SUBTEXT),
                    (WIDTH // 2 - 220, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
