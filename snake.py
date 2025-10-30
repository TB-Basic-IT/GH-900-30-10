import pygame
import sys
import random

# Kleuren
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Scherm instellingen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

class Snake:
    def __init__(self):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        if (new_dir[0] == -self.direction[0] and new_dir[0] != 0) or (new_dir[1] == -self.direction[1] and new_dir[1] != 0):
            return  # 180 graden draaien niet toegestaan
        self.direction = new_dir

    def collides_with_self(self):
        return self.positions[0] in self.positions[1:]

    def collides_with_wall(self):
        head_x, head_y = self.positions[0]
        return not (0 <= head_x < SCREEN_WIDTH and 0 <= head_y < SCREEN_HEIGHT)

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randrange(0, SCREEN_WIDTH, CELL_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT, CELL_SIZE)
        return (x, y)

    def respawn(self, snake_positions):
        while True:
            self.position = self.random_position()
            if self.position not in snake_positions:
                break

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    score = 0
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((CELL_SIZE, 0))

        snake.move()

        # Checken of slang eet
        if snake.positions[0] == food.position:
            snake.grow = True
            food.respawn(snake.positions)
            score += 1

        # Checken op botsingen
        if snake.collides_with_self() or snake.collides_with_wall():
            running = False

        # Scherm tekenen
        screen.fill(BLACK)
        for pos in snake.positions:
            pygame.draw.rect(screen, GREEN, (*pos, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food.position, CELL_SIZE, CELL_SIZE))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    print(f"Eindscore: {score}")

if __name__ == "__main__":
    main()
