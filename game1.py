import pygame
import random
import sqlite3

# Инициализация Pygame и базы данных
pygame.init()
conn = sqlite3.connect('scores.db')
cursor = conn.cursor()

# Создание таблицы для рекордов, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL
)
''')
conn.commit()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INITIAL_PLAYER_SIZE = 50
BALL_SIZE = 30
INITIAL_BALL_FALL_SPEED = 3  # Начальная скорость падения
MAX_BALL_FALL_SPEED = 10  # Максимальная скорость падения
WHITE = (255, 255, 255)
FPS = 30

# Настройки экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Собирай Мячи")

# Шрифты
font = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Загрузка изображений
player_image = pygame.image.load('player.jpg')
player_image = pygame.transform.scale(player_image, (INITIAL_PLAYER_SIZE, INITIAL_PLAYER_SIZE))

# Загрузка нескольких изображений мячей
ball_images = [
    pygame.image.load('block.jpg'),
    pygame.image.load('ball2.jpg'),
    pygame.image.load('ball3.jpg')
]
ball_images = [pygame.transform.scale(img, (BALL_SIZE, BALL_SIZE)) for img in ball_images]

background_start = pygame.image.load('background_start.png')
background_end = pygame.image.load('background_end.jpg')
background_scores = pygame.image.load('background_scores.jpg')  # Фон для рекордов
game_background = pygame.image.load('game_background.jpg')  # Фоновое изображение для игры
background_start = pygame.transform.scale(background_start, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_end = pygame.transform.scale(background_end, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_scores = pygame.transform.scale(background_scores, (
SCREEN_WIDTH, SCREEN_HEIGHT))  # Масштабируем фоновое изображение для рекордов
game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Класс игрока
class Player:
    def __init__(self):
        self.size = INITIAL_PLAYER_SIZE
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - self.size, self.size, self.size)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.size:
            self.rect.x = SCREEN_WIDTH - self.size

    def draw(self):
        scaled_image = pygame.transform.scale(player_image, (self.size, self.size))
        screen.blit(scaled_image, self.rect.topleft)

    def increase_size(self):
        self.size += 5  # Увеличиваем размер игрока


# Класс мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - BALL_SIZE), 0, BALL_SIZE, BALL_SIZE)
        self.image = random.choice(ball_images)  # Случайное изображение мяча

    def fall(self, speed):
        self.rect.y += speed

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


# Функция для отображения рекордов
def show_scores():
    screen.blit(background_scores, (0, 0))  # Отображаем фон для рекордов
    title_text = font.render("Рекорды", True, (0, 0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    cursor.execute("SELECT score FROM scores ORDER BY score DESC")
    scores = cursor.fetchall()

    if scores:
        for i, (score,) in enumerate(scores):
            score_text = font_small.render(f"{i + 1}. {score}", True, (0, 0, 0))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 100 + i * 40))
    else:
        no_scores_text = font_small.render("Нет рекордов", True, (0, 0, 0))
        screen.blit(no_scores_text, (SCREEN_WIDTH // 2 - no_scores_text.get_width() // 2, 100))

    back_text = font_small.render("Нажмите любую клавишу, чтобы вернуться", True, (0, 0, 0))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# Функция для отрисовки кнопки
def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, (0, 0, 255), (x, y, width, height))  # Кнопка синего цвета
    button_text = font_small.render(text, True, WHITE)
    screen.blit(button_text, (x + width // 2 - button_text.get_width() // 2,
                              y + height // 2 - button_text.get_height() // 2))


# Функция для отображения поздравления
def show_congratulations(score):
    message = f"Поздравляем! Вы набрали {score} очков!"
    text = font_small.render(message, True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Задержка для отображения сообщения


# Начальная заставка
def show_start_screen():
    while True:
        screen.blit(background_start, (0, 0))
        title_text = font.render("Собирай Мячи", True, (0, 0, 0))
        screen.blit(title_text, (
        SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2))

        # Отрисовать кнопку "Начать"
        draw_button("Начать", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        # Отрисовать кнопку "Рекорды"
        draw_button("Рекорды", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100:
                    if SCREEN_HEIGHT // 2 + 50 < mouse_y < SCREEN_HEIGHT // 2 + 100:
                        return  # Начать игру
                    if SCREEN_HEIGHT // 2 + 120 < mouse_y < SCREEN_HEIGHT // 2 + 170:
                        show_scores()  # Показать рекорды


# Конечная заставка
def show_end_screen(score):
    cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()

    screen.blit(background_end, (0, 0))
    game_over_text = font.render("Игра Окончена!", True, (0, 0, 0))
    screen.blit(game_over_text, (
    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    score_text = font_small.render(f"Ваш счёт: {score}", True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    restart_text = font_small.render("Нажмите любую клавишу, чтобы сыграть снова", True, (0, 0, 0))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# Главная функция игры
def main():
    clock = pygame.time.Clock()
    player = Player()
    balls = []
    score = 0
    speed = INITIAL_BALL_FALL_SPEED
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5)
        if keys[pygame.K_RIGHT]:
            player.move(5)

        # Уменьшение количества мячей, которые падают
        if random.randint(1, 50) == 1:  # Увеличиваем интервал создания мячей
            balls.append(Ball())

        # Обновление мячей
        for ball in balls:
            ball.fall(speed)
            if ball.rect.y > SCREEN_HEIGHT:
                show_end_screen(score)  # Конец игры при пропуске мяча
                return  # Вернуться в главное меню
            if player.rect.colliderect(ball.rect):
                balls.remove(ball)
                score += 1
                player.increase_size()  # Увеличиваем размер игрока

                # Увеличиваем скорость падения мячей после достижения определенных очков
                if score % 10 == 0 and score != 0:
                    speed = min(speed + 1, MAX_BALL_FALL_SPEED)  # Ограничиваем максимальную скорость

                # Поздравляем игрока, если он достиг 10 или 100 очков
                if score == 10 or score == 100:
                    show_congratulations(score)

        # Отрисовка
        screen.blit(game_background, (0, 0))  # Отрисовка фонового изображения для игры
        player.draw()
        for ball in balls:
            ball.draw()
        score_text = font_small.render(f"Счёт: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Отображение счёта в верхнем левом углу
        pygame.display.flip()

        clock.tick(FPS)

    show_end_screen(score)

if __name__ == "__main__":
    show_start_screen()
    main()

# Закрытие базы данных
conn.close()
