import pygame
import sys
import random

# Ініціалізуємо Pygame
pygame.init()

# Встановлюємо параметри екрану
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dinosaur T-Rex Jump")

# Встановлюємо кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Завантажуємо спрайт динозавра
# dino = pygame.image.load('dino1.png')
# http://vkm.ltd.ua/img/dino/dino1.png
dino_images = [pygame.image.load(f'img/dino{i}.png') for i in range(1, 3)]
dino_index = 0
dino = dino_images[dino_index]
dino_rect = dino.get_rect()
dino_rect.x = 150
dino_rect.y = screen_height - dino_rect.height -20

# Параметри стрибка
jumping = False
jump_speed = 15
gravity = 1
jump_height = 0

# Параметри перешкод
obstacle_speed = 10
obstacle_frequency = 1500  # частота створення перешкод (в мілісекундах)
last_obstacle_time = pygame.time.get_ticks()

# Перемінні для гри
obstacles = []
game_over = False
score = 0
jump = 0
start_time = 0

# Шрифт для відображення тексту
font = pygame.font.Font(None, 36)

# Функція для створення перешкод
def create_obstacle():
    obstacle = pygame.Rect(screen_width, screen_height - 50, 50, 50)
    # obstacle = pygame.image.load('dino1.png')
    obstacles.append(obstacle)

# Функція для обробки перезапуску гри
def restart_game():
    global dino_rect, obstacles, game_over, score, start_time, jumping, jump_height, dino_index
    dino_rect.x = 50
    dino_rect.y = screen_height - dino_rect.height
    obstacles = []
    game_over = False
    score = 0
    start_time = pygame.time.get_ticks()
    jumping = False
    jump_height = 0

# Основний цикл гри
clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()
animation_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping and not game_over:
                jumping = True
                jump_height = jump_speed
                jump += 1
            if event.key == pygame.K_RETURN and game_over:
                restart_game()

    if not game_over:
        # Обробляємо стрибок
        if jumping:
            dino_rect.y -= jump_height
            jump_height -= gravity

            if jump_height < -jump_speed:
                jumping = False

        # Створюємо нові перешкоди
        current_time = pygame.time.get_ticks()
        if current_time - last_obstacle_time > obstacle_frequency:
            create_obstacle()
            last_obstacle_time = current_time

        # Рухаємо перешкоди
        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            # print(obstacle.x)

        # Перевіряємо зіткнення
        for obstacle in obstacles:
            if dino_rect.colliderect(obstacle):
                game_over = True
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000

        # Підраховуємо кількість перепригнутих перешкод
        # score = len([obstacle for obstacle in obstacles if obstacle.x < 0])
        # if obstacle.x == 50:
        # if obstacle.x + obstacle.width < dino_rect.x:
        # if obstacles.x == 50:
        #     score = score+1

        # Перевіряємо, чи динозавр успішно перепригнув перешкоду
        new_obstacles = []
        for obstacle in obstacles:
            if obstacle.x + obstacle.width < dino_rect.x:
                if not hasattr(obstacle, 'counted'):
                    score += 1
                    # obstacle.counted = True
            new_obstacles.append(obstacle)
        obstacles = new_obstacles


        # Видаляємо перешкоди, які вийшли за екран
        obstacles = [obstacle for obstacle in obstacles if obstacle.x > -50]
        # score = score + score

        # Оновлюємо спрайт динозавра для анімації
        if current_time - animation_time > 100:  # змінюємо кадр кожні 100 мс
            dino_index = (dino_index + 1) % len(dino_images)
            dino = dino_images[dino_index]
            animation_time = current_time

    # score = score + score2

    # Оновлюємо екран
    screen.fill(WHITE)
    screen.blit(dino, dino_rect)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

    # Відображаємо рахунок та час
    if game_over:
        game_over_text = font.render(f"Game Over! Time: {elapsed_time:.2f}s, Jump: {jump}, Score: {score}", True, BLACK)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        restart_text = font.render("Press Enter to restart", True, BLACK)
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 30))
    else:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
        screen.blit(time_text, (10, 10))
        jump_text = font.render(f"Jump: {jump}", True, BLACK)
        screen.blit(jump_text, (10, 50))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 90))
    pygame.display.flip()

    # Обмежуємо кількість кадрів
    clock.tick(30)

# Закриваємо Pygame
pygame.quit()
sys.exit()
