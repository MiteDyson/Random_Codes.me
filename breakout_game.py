import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SIZE = 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 20

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Atari Breakout')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Paddle position
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 30

# Ball position and speed
ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
ball_speed_x, ball_speed_y = 4, -4

# Bricks
bricks = []
for i in range(8):
    for j in range(5):
        bricks.append(pygame.Rect(70 + i * (BRICK_WIDTH + 10), 50 + j * (BRICK_HEIGHT + 10), BRICK_WIDTH, BRICK_HEIGHT))

# Score
score = 0

def draw_paddle(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), BALL_SIZE)

def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= 6
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x += 6

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_x <= BALL_SIZE or ball_x >= SCREEN_WIDTH - BALL_SIZE:
        ball_speed_x = -ball_speed_x
    if ball_y <= BALL_SIZE:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    if ball_y >= paddle_y - BALL_SIZE and paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH:
        ball_speed_y = -ball_speed_y

    # Ball collision with bricks
    ball_rect = pygame.Rect(ball_x - BALL_SIZE, ball_y - BALL_SIZE, BALL_SIZE * 2, BALL_SIZE * 2)
    for brick in bricks[:]:
        if ball_rect.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            score += 10
            break

    # Ball out of bounds
    if ball_y >= SCREEN_HEIGHT:
        print("Game Over! Final Score:", score)
        running = False

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw the paddle
    draw_paddle(paddle_x, paddle_y)

    # Draw the ball
    draw_ball(ball_x, ball_y)

    # Draw the bricks
    draw_bricks()

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
