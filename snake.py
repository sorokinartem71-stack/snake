"""Игра «Изгиб Питона»."""
import random
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
FPS = 20

GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
CENTER_POS = (
    (GRID_WIDTH // 2) * CELL_SIZE,
    (GRID_HEIGHT // 2) * CELL_SIZE,
)

ALL_CELLS = set(
    (x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

DIRECTIONS = {
    (pygame.K_UP, (0, 1)): (0, -1),
    (pygame.K_DOWN, (0, -1)): (0, 1),
    (pygame.K_LEFT, (1, 0)): (-1, 0),
    (pygame.K_RIGHT, (-1, 0)): (1, 0),
}


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = None

    def draw_cell(self, surface, pos, color):
        """Рисует одну ячейку на игровой поверхности."""
        rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, color, rect)

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализирует яблоко случайной позицией."""
        super().__init__(position=(0, 0))
        self.body_color = RED

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока."""
        occupied = set(snake_positions)
        free_cells = list(ALL_CELLS - occupied)

        if not free_cells:
            return

        cell_x, cell_y = random.choice(free_cells)
        self.position = (cell_x * CELL_SIZE, cell_y * CELL_SIZE)

    def draw(self, surface):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(position=CENTER_POS)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POS]
        self.direction = (1, 0)
        self.next_direction = None
        self.body_color = GREEN

    def update_direction(self, event_key):
        """Обновляет направление движения змейки."""
        new_dir = DIRECTIONS.get((event_key, self.direction))
        if new_dir:
            self.next_direction = new_dir

    def move(self):
        """Двигает змейку на одну ячейку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        new_head_x = (
            (head_x + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        )
        new_head_y = (
            (head_y + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        )
        new_head = (new_head_x, new_head_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def check_self_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        head = self.positions[0]
        if head in self.positions[1:]:
            self.length = 1
            self.positions = [head]
            return True
        return False

    def draw(self, surface):
        """Отрисовывает голову змейки."""
        self.draw_cell(surface, self.positions[0], self.body_color)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                snake.update_direction(event.key)

        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.check_self_collision()

        screen.fill(BLACK)
        for pos in snake.positions:
            snake.draw_cell(screen, pos, snake.body_color)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
