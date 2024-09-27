import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define basic parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Color definitions
WHITE = (255, 255, 255)  # RGB for white color
BLACK = (0, 0, 0)  # RGB for black color
RED = (255, 0, 0)  # RGB for red color
BLUE = (0, 0, 255)  # RGB for blue color
GREEN = (0, 255, 0)  # RGB for green color

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Runner Game")

# Clock object
clock = pygame.time.Clock()

# Load player image
player_img = pygame.image.load("assassin-stand-on-the-church-with-a-shirt-like-ass.png")
player_img = pygame.transform.scale(player_img, (50, 50))  # Resize the player image to fit within 50x50

# Create obstacle placeholder
obstacle_img = pygame.Surface((50, 50))
obstacle_img.fill(RED)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img  # Use loaded player image
        self.rect = self.image.get_rect()  # Get the rectangle object for image positioning
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.speed_y = 0  # Vertical speed
        self.jump_power = -15  # Jump power
        self.gravity = 1  # Gravity factor

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == SCREEN_HEIGHT:
            self.speed_y = self.jump_power  # Jump
        self.speed_y += self.gravity  # Gravity effect
        self.rect.y += self.speed_y  # Apply vertical speed to the player's Y position
        if self.rect.bottom > SCREEN_HEIGHT:  # Prevent player from falling below the screen
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img  # Use obstacle image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 50

    def update(self):
        self.rect.x -= 10  # Move obstacle to the left
        if self.rect.right < 0:  # If the obstacle goes out of the screen
            self.kill()  # Remove this obstacle instance
            new_obstacle = Obstacle()  # Create a new obstacle
            all_sprites.add(new_obstacle)  # Add new obstacle to all_sprites group
            obstacles.add(new_obstacle)  # Add new obstacle to obstacles group

# Function to draw text on the screen
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Function to display start screen
def show_start_screen():
    screen.fill(WHITE)
    draw_text(screen, "Simple Runner Game", 48, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    start_button_color = GREEN
    pygame.draw.rect(screen, start_button_color, start_button)
    draw_text(screen, "Start", 30, BLACK, start_button.centerx, start_button.centery - 15)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    waiting = False

# Function to start a new game
def new_game():
    global player, all_sprites, obstacles
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    obstacles = pygame.sprite.Group()
    for _ in range(3):
        obstacle = Obstacle()
        obstacle.rect.x = SCREEN_WIDTH + random.randint(0, 300) * _
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

# Define start button dimensions
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_start_screen()
        new_game()
        game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Collision detection
    if pygame.sprite.spritecollide(player, obstacles, False):
        game_over = True

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
