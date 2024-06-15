import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
PACMAN_SIZE = 20
PACMAN_SPEED = 5
GHOST_SIZE = 20
GHOST_SPEED = 3
PELLET_SIZE = 5
CHERRY_SIZE = 10
CHERRY_POINTS = 50

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Pac-Man starting position
pacman_x, pacman_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Ghosts starting positions
ghosts = [
    {'x': 100, 'y': 100, 'direction': (GHOST_SPEED, 0)},
    {'x': 500, 'y': 100, 'direction': (-GHOST_SPEED, 0)},
    {'x': 100, 'y': 300, 'direction': (0, GHOST_SPEED)},
    {'x': 500, 'y': 300, 'direction': (0, -GHOST_SPEED)}
]

# Pellets
pellets = [(x, y) for x in range(70, SCREEN_WIDTH-30, 40) for y in range(70, SCREEN_HEIGHT-30, 40)]

# Cherry power-up
cherry = (random.randint(60, SCREEN_WIDTH-60), random.randint(60, SCREEN_HEIGHT-60))

# Maze walls
walls = [
    pygame.Rect(50, 50, 500, 10),
    pygame.Rect(50, 50, 10, 300),
    pygame.Rect(50, 350, 500, 10),
    pygame.Rect(540, 50, 10, 300),
    pygame.Rect(150, 150, 300, 10),
    pygame.Rect(150, 250, 300, 10),
]

# Score
score = 0

def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), PACMAN_SIZE)

def draw_ghost(x, y):
    pygame.draw.rect(screen, RED, (x - GHOST_SIZE // 2, y - GHOST_SIZE // 2, GHOST_SIZE, GHOST_SIZE))

def draw_pellets():
    for pellet in pellets:
        pygame.draw.circle(screen, WHITE, pellet, PELLET_SIZE)

def draw_cherry():
    pygame.draw.circle(screen, PINK, cherry, CHERRY_SIZE)

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall)

def move_ghosts():
    for ghost in ghosts:
        ghost['x'] += ghost['direction'][0]
        ghost['y'] += ghost['direction'][1]
        if ghost['x'] < GHOST_SIZE or ghost['x'] > SCREEN_WIDTH - GHOST_SIZE:
            ghost['direction'] = (-ghost['direction'][0], ghost['direction'][1])
        if ghost['y'] < GHOST_SIZE or ghost['y'] > SCREEN_HEIGHT - GHOST_SIZE:
            ghost['direction'] = (ghost['direction'][0], -ghost['direction'][1])

def check_collision(x, y, size):
    pacman_rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
    if any(wall.colliderect(pacman_rect) for wall in walls):
        return True
    return False

def check_pellet_collision(x, y):
    global score
    pacman_rect = pygame.Rect(x - PACMAN_SIZE, y - PACMAN_SIZE, PACMAN_SIZE * 2, PACMAN_SIZE * 2)
    for pellet in pellets[:]:
        pellet_rect = pygame.Rect(pellet[0] - PELLET_SIZE, pellet[1] - PELLET_SIZE, PELLET_SIZE * 2, PELLET_SIZE * 2)
        if pacman_rect.colliderect(pellet_rect):
            pellets.remove(pellet)
            score += 10

def check_cherry_collision(x, y):
    global score, cherry
    pacman_rect = pygame.Rect(x - PACMAN_SIZE, y - PACMAN_SIZE, PACMAN_SIZE * 2, PACMAN_SIZE * 2)
    cherry_rect = pygame.Rect(cherry[0] - CHERRY_SIZE, cherry[1] - CHERRY_SIZE, CHERRY_SIZE * 2, CHERRY_SIZE * 2)
    if pacman_rect.colliderect(cherry_rect):
        score += CHERRY_POINTS
        cherry = (random.randint(60, SCREEN_WIDTH-60), random.randint(60, SCREEN_HEIGHT-60))

def check_ghost_collision(x, y):
    pacman_rect = pygame.Rect(x - PACMAN_SIZE, y - PACMAN_SIZE, PACMAN_SIZE * 2, PACMAN_SIZE * 2)
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost['x'] - GHOST_SIZE // 2, ghost['y'] - GHOST_SIZE // 2, GHOST_SIZE, GHOST_SIZE)
        if pacman_rect.colliderect(ghost_rect):
            return True
    return False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = pacman_x, pacman_y
    if keys[pygame.K_LEFT]:
        new_x -= PACMAN_SPEED
    if keys[pygame.K_RIGHT]:
        new_x += PACMAN_SPEED
    if keys[pygame.K_UP]:
        new_y -= PACMAN_SPEED
    if keys[pygame.K_DOWN]:
        new_y += PACMAN_SPEED

    if not check_collision(new_x, new_y, PACMAN_SIZE):
        pacman_x, pacman_y = new_x, new_y

    check_pellet_collision(pacman_x, pacman_y)
    check_cherry_collision(pacman_x, pacman_y)
    if check_ghost_collision(pacman_x, pacman_y):
        print("Game Over! Final Score:", score)
        running = False

    move_ghosts()

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw the walls
    draw_walls()

    # Draw the pellets
    draw_pellets()

    # Draw the cherry
    draw_cherry()

    # Draw Pac-Man
    draw_pacman(pacman_x, pacman_y)

    # Draw the ghosts
    for ghost in ghosts:
        draw_ghost(ghost['x'], ghost['y'])

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit pygame
pygame.quit()
sys.exit()
