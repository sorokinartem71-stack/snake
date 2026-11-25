import pygame
import random


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
FPS = 20

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position):
        self.position = position
        self.body_color = None  

    def draw(self, surface):
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Задаёт цвет яблока и случайную начальную позицию."""
        super().__init__(position=None)  # Позиция будет установлена в randomize_position
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        max_x = (SCREEN_WIDTH // CELL_SIZE) - 1
        max_y = (SCREEN_HEIGHT // CELL_SIZE) - 1
        self.position = (
            random.randint(0, max_x) * CELL_SIZE,
            random.randint(0, max_y) * CELL_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """начальное состояние змейки."""
        start_x = (SCREEN_WIDTH // 2 // CELL_SIZE) * CELL_SIZE
        start_y = (SCREEN_HEIGHT // 2 // CELL_SIZE) * CELL_SIZE

        super().__init__(position=(start_x, start_y))
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = (1, 0)  # Вправо
        self.next_direction = None
        self.body_color = GREEN

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки, если оно не противоположно текущему."""
        if self.next_direction:
            # Проверяем, что новое направление не противоположно текущему
            if (self.next_direction[0] != -self.direction[0] or
                    self.next_direction[1] != -self.direction[1]):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction

        new_head_x = (head_x + dx * CELL_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * CELL_SIZE) % SCREEN_HEIGHT

        self.positions.insert(0, (new_head_x, new_head_y))

        # Если длина не увеличилась, удаляем последний сегмент
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

        # Затираем след от удалённого хвоста
        if len(self.positions) < self.length:
            pass

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__()


def handle_keys(snake):
    """Управление"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.next_direction = (1, 0)


def main():
    """Основной игровой цикл"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения змейки с самой собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
