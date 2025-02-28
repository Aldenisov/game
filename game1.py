import pygame
import random
import sqlite3

# Инициализация Pygame и базы данных
pygame.init()
conn = sqlite3.connect('../scores.db')
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
PLAYER_SIZE = 50
BALL_SIZE = 30
BALL_FALL_SPEED = 5
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
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

ball_image = pygame.image.load('block.jpg')
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))

background_start = pygame.image.load('background_start.png')
background_end = pygame.image.load('background_end.jpg')
background_start = pygame.transform.scale(background_start, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_end = pygame.transform.scale(background_end, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Класс игрока
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_SIZE:
            self.rect.x = SCREEN_WIDTH - PLAYER_SIZE

    def draw(self):
        screen.blit(player_image, self.rect.topleft)

# Класс мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - BALL_SIZE), 0, BALL_SIZE, BALL_SIZE)

    def fall(self, speed):
        self.rect.y += speed

    def draw(self):
        screen.blit(ball_image, self.rect.topleft)

# Функция для отображения рекордов
def show_scores():
    screen.fill(WHITE)
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

# Начальная заставка
def show_start_screen():
    while True:
        screen.blit(background_start, (0, 0))
        title_text = font.render("Собирай Мячи", True, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2))
        instructions_text = font_small.render("Нажмите 'П', чтобы начать, или 'Р', чтобы посмотреть рекорды", True, (0, 0, 0))
        screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return  # Начать игру
                elif event.key == pygame.K_r:
                    show_scores()  # Показать рекорды

# Конечная заставка
def show_end_screen(score):
    cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()

    screen.blit(background_end, (0, 0))
    game_over_text = font.render("Игра Окончена!", True, (0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
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
    speed = BALL_FALL_SPEED
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

        # Создание мяча
        if random.randint(1, 20) == 1:
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
                speed += 0.5  # Увеличиваем скорость падения мяча с каждым собранным

        # Отрисовка
        screen.fill(WHITE)
        player.draw()
        for ball in balls:
            ball.draw()
        pygame.display.flip()

        clock.tick(FPS)

    show_end_screen(score)

if __name__ == "__main__":
    show_start_screen()
    main()

# Закрытие базы данных
conn.close()
