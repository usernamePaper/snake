import pygame
import random

# Определяем константы
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# Определяем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Инициализируем Pygame
pygame.init()

# Создаем поверхность игры
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Змейка')

# Определяем функцию отрисовки змеи
def draw_snake(snake_list):
    for i in range(len(snake_list)):
        x = snake_list[i][0]
        y = snake_list[i][1]
        pygame.draw.rect(game_display, GREEN, [x, y, CELL_SIZE, CELL_SIZE])

# Определяем функцию вывода текста на экран
def text_display(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    game_display.blit(text_surface, text_rect)

# Определяем функцию игрового цикла
def game_loop(level):
    # Инициализируем переменные
    snake_list = []
    snake_length = 1
    direction = 'up'
    score = 0
    eat_score = 0

    # Создаем змею и еду
    x = random.randrange(0, WINDOW_WIDTH - CELL_SIZE, CELL_SIZE)
    y = random.randrange(0, WINDOW_HEIGHT - CELL_SIZE, CELL_SIZE)
    snake_list.append([x, y])
    food_x = random.randrange(0, WINDOW_WIDTH - CELL_SIZE, CELL_SIZE)
    food_y = random.randrange(0, WINDOW_HEIGHT - CELL_SIZE, CELL_SIZE)

    # Запускаем игровой цикл
    game_exit = False
    clock = pygame.time.Clock()

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                elif event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'

        # Двигаем змею
        if direction == 'up':
            head = [snake_list[0][0], snake_list[0][1] - CELL_SIZE]
        elif direction == 'down':
            head = [snake_list[0][0], snake_list[0][1] + CELL_SIZE]
        elif direction == 'left':
            head = [snake_list[0][0] - CELL_SIZE, snake_list[0][1]]
        elif direction == 'right':
            head = [snake_list[0][0] + CELL_SIZE, snake_list[0][1]]

        # Проверяем столкновение со стеной
        if head[0] < 0 or head[0] >= WINDOW_WIDTH or head[1] < 0 or head[1] >= WINDOW_HEIGHT:
            death_menu()

        # Проверяем столкновение с телом змеи
        for i in range(1, len(snake_list)):
            if head == snake_list[i]:
                death_menu()

        # Добавляем голову змеи в список
        snake_list.insert(0, head)

        # Удаляем хвост змеи
        if len(snake_list) > snake_length:
            del snake_list[-1]

        # Рисуем фон и еду
        game_display.fill(BLACK)
        pygame.draw.rect(game_display, RED, [food_x, food_y, CELL_SIZE, CELL_SIZE])

        # Определяем условия поедания еды
        if head[0] == food_x and head[1] == food_y:
            food_x = random.randrange(0, WINDOW_WIDTH - CELL_SIZE, CELL_SIZE)
            food_y = random.randrange(0, WINDOW_HEIGHT - CELL_SIZE, CELL_SIZE)
            snake_length += 1
            score += 10
            eat_score += 1

        # Рисуем змею и еду
        draw_snake(snake_list)
        pygame.draw.rect(game_display, RED, [food_x, food_y, CELL_SIZE, CELL_SIZE])

        # Выводим счет на экран
        text_display(f'Счет: {score}', 20, 50, 20)

        # Выводим количество сьеденной еды на экран
        text_display(f'Сьеденная еда: {eat_score}', 20, 150, 20)

        # Обновляем экран
        text_display('Поддержите автора: https://www.donationalerts.com/r/kebab_', 15, WINDOW_WIDTH // 1.35, WINDOW_HEIGHT // 1.01)
        pygame.display.update()

        # Задаем задержку между кадрами
        clock.tick(FPS + level * 2)

    # Закрываем Pygame
    pygame.quit()
    quit()

# Определяем функцию меню выбора уровня сложности
def level_menu():
    # Инициализируем переменные
    menu_exit = False
    level = 1

    while not menu_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 1
                    menu_exit = True
                elif event.key == pygame.K_2:
                    level = 2
                    menu_exit = True
                elif event.key == pygame.K_3:
                    level = 3
                    menu_exit = True
                elif event.key == pygame.K_F9:
                    debug_menu()

        # Рисуем фон и текст меню
        game_display.fill(BLACK)
        text_display('Выберите уровень сложности:', 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        text_display('1 - Легкий', 25, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        text_display('2 - Средний', 25, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
        text_display('3 - Тяжелый', 25, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
        text_display('Поддержите автора: https://www.donationalerts.com/r/kebab_', 15, WINDOW_WIDTH // 1.35, WINDOW_HEIGHT // 1.01)

        # Обновляем экран
        pygame.display.update()

    # Запускаем игровой цикл с выбранным уровнем сложности
    game_loop(level)

# Определяем функцию главного меню
def main_menu():
    # Инициализируем переменные
    menu_exit = False

    while not menu_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level_menu()
                elif event.key == pygame.K_F9:
                    debug_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Рисуем фон и текст меню
        game_display.fill(BLACK)
        text_display('Нажмите Пробел, чтобы начать игру', 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        text_display('ESC - выход', 20, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        text_display('Поддержите автора: https://www.donationalerts.com/r/kebab_', 15, WINDOW_WIDTH // 1.35, WINDOW_HEIGHT // 1.01)

        # Обновляем экран
        pygame.display.update()

 # Определяем функцию меню проигрыша
def death_menu():
    # Инициализируем переменные
    menu_exit = False

    while not menu_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level_menu()
                elif event.key == pygame.K_F9:
                    debug_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Рисуем фон и текст меню
        game_display.fill(BLACK)
        text_display('Нажмите Пробел, чтобы перезапустить игру', 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        text_display('ESC - выход', 20, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        text_display('Поддержите автора: https://www.donationalerts.com/r/kebab_', 15, WINDOW_WIDTH // 1.35, WINDOW_HEIGHT // 1.01)

        # Обновляем экран
        pygame.display.update()

# Определяем дебаг меню
def debug_menu():
    # Инициализируем переменные
    menu_exit = False

    while not menu_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main_menu()
                elif event.key == pygame.K_2:
                    level_menu()
                elif event.key == pygame.K_3:
                    death_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Рисуем фон и текст меню
        game_display.fill(BLACK)
        text_display('Данное меню недоработанно!', 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        text_display('1 - main menu', 25, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        text_display('2 - level menu', 25, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
        text_display('3 - death menu', 25, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
        text_display('ESC - выход', 20, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90                    )
        text_display('Поддержите автора: https://www.donationalerts.com/r/kebab_', 15, WINDOW_WIDTH // 1.35, WINDOW_HEIGHT // 1.01)

        # Обновляем экран
        pygame.display.update()
 
# Запускаем главное меню
main_menu()
