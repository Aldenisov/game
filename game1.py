import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INITIAL_PLAYER_SIZE = 50
BALL_SIZE = 30
TRAP_SIZE = 30
INITIAL_BALL_FALL_SPEED = 3  # Начальная скорость падения
FPS = 30

# Настройки экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Собирай Мячи")

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
        pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Синий цвет игрока

    def increase_size(self):
        self.size += 5  # Увеличиваем размер игрока

    def decrease_size(self):
        self.size = max(10, self.size - 5)  # Уменьшаем размер игрока
        self.rect.height = self.size  # Обновляем высоту прямоугольника

# Класс мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - BALL_SIZE), 0, BALL_SIZE, BALL_SIZE)

    def fall(self, speed):
        self.rect.y += speed

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Красный цвет мяча

# Класс ловушки
class Trap:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - TRAP_SIZE), 0, TRAP_SIZE, TRAP_SIZE)

    def fall(self, speed):
        self.rect.y += speed

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Зеленый цвет ловушки

def main():
    clock = pygame.time.Clock()
    player = Player()
    balls = []
    traps = []
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

        # Создание мячей и ловушек
        if random.randint(1, 50) == 1:  # Увеличиваем интервал создания мячей и ловушек
            balls.append(Ball())

        if random.randint(1, 100) == 1:  # Ловушки появляются реже
            traps.append(Trap())

        # Обновление мячей
        for ball in balls:
            ball.fall(speed)
            if ball.rect.y > SCREEN_HEIGHT:
                print("Пропущен мяч!")  # Конец игры при пропуске мяча
                running = False  # Завершаем внутренний цикл игры
                break
            if player.rect.colliderect(ball.rect):
                player.increase_size()  # Увеличиваем размер игрока
                balls.remove(ball)
                score += 1  # Увеличиваем счёт

        # Обновление ловушек
        for trap in traps:
            trap.fall(speed)
            if player.rect.colliderect(trap.rect):
                print("Столкновение с ловушкой!")  # Конец игры при столкновении с ловушкой
                running = False  # Завершаем внутренний цикл игры
                break

        # Отрисовка
        screen.fill((255, 255, 255))  # Белый фон
        player.draw()
        for ball in balls:
            ball.draw()
        for trap in traps:
            trap.draw()

        # Отображение счёта
        score_text = pygame.font.Font(None, 36).render(f"Счёт: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Отображение счёта в верхнем левом углу
        pygame.display.flip()

        clock.tick(FPS)

    print(f"Игра окончена! Ваш счёт: {score}")

if __name__ == "__main__":
    main()
    pygame.quit()